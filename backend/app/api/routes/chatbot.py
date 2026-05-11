from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.chatbot.db.session import get_chatbot_db, check_db_connection
from app.chatbot.db.models import ChatHistory
from app.chatbot.agents.orchestrator import orchestrator, ChatRequest as OrchestratorRequest
from app.chatbot.schemas.chat import (
    ChatRequest, ChatResponse, FeedbackRequest, FeedbackResponse,
    ChatHistoryItem, ChatHistoryResponse,
    IngestRequest, IngestResponse, HealthResponse,
)
from app.chatbot.rag.pipeline import rag_pipeline
from app.chatbot.llm.gateway import llm_gateway
from app.chatbot.core.config import chatbot_settings
from app.chatbot.core.logging import get_logger

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])
logger = get_logger(__name__)


# ── Chat endpoints ────────────────────────────────────────────────

@router.post(
    "/chat/message",
    response_model=ChatResponse,
    summary="Send a chat message to the OMS AI assistant",
)
async def send_message(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_chatbot_db),
) -> ChatResponse:
    try:
        orch_request = OrchestratorRequest(
            user_message=payload.message,
            session_id=payload.session_id,
            tenant_id=payload.tenant_id,
            user_id=payload.user_id,
            conversation_history=[
                {"role": m.role, "content": m.content}
                for m in (payload.conversation_history or [])
            ],
        )
        result = await orchestrator.process(orch_request, db)

        return ChatResponse(
            response=result.response,
            session_id=result.session_id,
            trace_id=result.trace_id,
            intent_code=result.intent_code,
            intent_label=result.intent_label,
            response_mode=result.response_mode,
            confidence=result.confidence,
            suggested_action=result.suggested_action,
            slot_requirements=result.slot_requirements,
            suggestions=result.suggestions,
            requires_human_review=result.requires_human_review,
            guardrail_blocked=result.guardrail_blocked,
            blocked_reason=result.blocked_reason,
            sources=result.sources,
            latency_ms=result.latency_ms,
        )

    except Exception as e:
        logger.error("chat_endpoint_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Chatbot processing error. Please try again.",
        )


@router.post(
    "/chat/stream",
    summary="Streaming chat (Server-Sent Events)",
)
async def stream_message(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_chatbot_db),
):
    orch_request = OrchestratorRequest(
        user_message=payload.message,
        session_id=payload.session_id,
        tenant_id=payload.tenant_id,
        user_id=payload.user_id,
        conversation_history=[
            {"role": m.role, "content": m.content}
            for m in (payload.conversation_history or [])
        ],
    )

    return StreamingResponse(
        orchestrator.stream_process(orch_request, db),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.post(
    "/chat/feedback",
    response_model=FeedbackResponse,
    summary="Submit feedback on a chatbot response",
)
async def submit_feedback(
    payload: FeedbackRequest,
    db: AsyncSession = Depends(get_chatbot_db),
) -> FeedbackResponse:
    stmt_select = (
        select(ChatHistory.id)
        .where(
            ChatHistory.trace_id == payload.trace_id,
            ChatHistory.session_id == payload.session_id,
            ChatHistory.role == "assistant",
        )
        .order_by(ChatHistory.created_date.desc())
        .limit(1)
    )
    result = await db.execute(stmt_select)
    row_id = result.scalar_one_or_none()

    if row_id:
        stmt = (
            update(ChatHistory)
            .where(ChatHistory.id == row_id)
            .values(feedback_score=payload.score, feedback_comment=payload.comment)
        )
        await db.execute(stmt)
        await db.commit()

    logger.info("feedback_recorded", trace_id=payload.trace_id, score=payload.score)
    return FeedbackResponse(trace_id=payload.trace_id)


@router.get(
    "/chat/history/{session_id}",
    response_model=ChatHistoryResponse,
    summary="Retrieve conversation history for a session",
)
async def get_history(
    session_id: str,
    limit: int = 50,
    db: AsyncSession = Depends(get_chatbot_db),
) -> ChatHistoryResponse:
    stmt = (
        select(ChatHistory)
        .where(
            ChatHistory.session_id == session_id,
            ChatHistory.is_deleted == False,
        )
        .order_by(ChatHistory.created_date.asc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    records = result.scalars().all()

    return ChatHistoryResponse(
        session_id=session_id,
        items=[ChatHistoryItem.model_validate(r) for r in records],
        total=len(records),
    )


# ── RAG & Admin endpoints ─────────────────────────────────────────

@router.post(
    "/rag/ingest",
    response_model=IngestResponse,
    summary="Ingest a document into the RAG knowledge base",
)
async def ingest_document(
    payload: IngestRequest,
    db: AsyncSession = Depends(get_chatbot_db),
) -> IngestResponse:
    try:
        chunks = await rag_pipeline.ingest_document(
            db=db,
            content=payload.content,
            source_doc=payload.source_doc,
            source_type=payload.source_type,
            metadata=payload.metadata,
        )
        return IngestResponse(
            status="success",
            source_doc=payload.source_doc,
            chunks_stored=chunks,
        )
    except Exception as e:
        logger.error("ingest_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ingestion failed: {str(e)}",
        )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Chatbot service health check",
)
async def chatbot_health(db: AsyncSession = Depends(get_chatbot_db)) -> HealthResponse:
    from app.chatbot.agents.oms_client import oms_client
    db_ok = await check_db_connection()
    llm_ok = await llm_gateway.health_check()
    oms_ok = await oms_client.health_check()

    overall = "healthy" if (db_ok and llm_ok) else "degraded"
    return HealthResponse(
        status=overall,
        db_connected=db_ok,
        llm_connected=llm_ok,
        version=chatbot_settings.chatbot_app_version,
        model=chatbot_settings.ollama_model,
    )
