import time
from typing import List, Optional, Dict, Any
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.chatbot.db.models import KnowledgeChunk
from app.chatbot.core.config import chatbot_settings
from app.chatbot.core.logging import get_logger

logger = get_logger(__name__)


class TextChunker:

    def __init__(self, chunk_size: int = 512, overlap: int = 64):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text: str) -> List[str]:
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            if end == len(words):
                break
            start += self.chunk_size - self.overlap
        return chunks


class RAGPipeline:

    def __init__(self):
        self.chunker = TextChunker(
            chunk_size=chatbot_settings.chunk_size,
            overlap=chatbot_settings.chunk_overlap,
        )

    async def ingest_document(
        self,
        db: AsyncSession,
        content: str,
        source_doc: str,
        source_type: str = "document",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> int:
        chunks = self.chunker.split(content)
        stored = 0

        for idx, chunk_text in enumerate(chunks):
            try:
                chunk = KnowledgeChunk(
                    source_doc=source_doc,
                    source_type=source_type,
                    chunk_text=chunk_text,
                    chunk_index=idx,
                    metadata_json=metadata or {},
                )
                db.add(chunk)
                stored += 1
            except Exception as e:
                logger.error(
                    "rag_ingestion_chunk_failed",
                    source_doc=source_doc,
                    chunk_index=idx,
                    error=str(e),
                )

        await db.commit()
        logger.info(
            "rag_ingestion_complete",
            source_doc=source_doc,
            total_chunks=stored,
            mode="keyword_only",
        )
        return stored

    async def retrieve(
        self,
        db: AsyncSession,
        query: str,
        top_k: int = None,
        source_type: Optional[str] = None,
        trace_id: str = "",
    ) -> List[Dict[str, Any]]:
        top_k = top_k or chatbot_settings.top_k_retrieval
        start = time.monotonic()

        stop_words = {
            "a", "an", "the", "is", "it", "in", "on", "at", "to", "do",
            "i", "my", "me", "for", "of", "and", "or", "with", "can",
            "you", "please", "help", "what", "how", "where", "when", "why",
        }
        keywords = [
            w.strip("?.,!").lower()
            for w in query.split()
            if len(w) > 2 and w.lower() not in stop_words
        ]

        if not keywords:
            logger.info("rag_no_keywords", trace_id=trace_id, query=query[:80])
            return []

        ilike_clauses = " OR ".join(
            [f"chunk_text ILIKE :kw{i}" for i in range(len(keywords))]
        )
        type_clause = "AND source_type = :source_type" if source_type else ""

        sql = text(f"""
            SELECT chunk_id, source_doc, source_type, chunk_text, metadata_json
            FROM knowledge_chunk
            WHERE is_deleted = FALSE
              AND ({ilike_clauses})
              {type_clause}
            LIMIT :limit
        """)

        params: Dict[str, Any] = {f"kw{i}": f"%{kw}%" for i, kw in enumerate(keywords)}
        params["limit"] = top_k * 3
        if source_type:
            params["source_type"] = source_type

        try:
            result = await db.execute(sql, params)
            rows = result.fetchall()
        except Exception as e:
            logger.error("rag_retrieval_failed", trace_id=trace_id, error=str(e))
            return []

        scored = self._score_by_keywords(keywords, rows)
        top_results = scored[:top_k]

        latency_ms = int((time.monotonic() - start) * 1000)
        logger.info(
            "rag_retrieval_complete",
            trace_id=trace_id,
            results=len(top_results),
            latency_ms=latency_ms,
        )
        return top_results

    def _score_by_keywords(self, keywords: List[str], rows: list) -> List[Dict[str, Any]]:
        scored = []
        for row in rows:
            chunk_lower = row.chunk_text.lower()
            hits = sum(1 for kw in keywords if kw in chunk_lower)
            density = hits / max(len(keywords), 1)
            scored.append({
                "chunk_id": row.chunk_id,
                "source_doc": row.source_doc,
                "source_type": row.source_type,
                "chunk_text": row.chunk_text,
                "similarity": density,
                "combined_score": density,
                "metadata": row.metadata_json or {},
            })
        scored.sort(key=lambda x: x["combined_score"], reverse=True)
        return scored

    def format_context(self, chunks: List[Dict[str, Any]]) -> str:
        if not chunks:
            return ""
        parts = []
        for i, c in enumerate(chunks, 1):
            source = c.get("source_doc", "Unknown")
            chunk_text = c.get("chunk_text", "")
            parts.append(f"[Source {i} – {source}]\n{chunk_text}")
        return "\n\n".join(parts)


rag_pipeline = RAGPipeline()
