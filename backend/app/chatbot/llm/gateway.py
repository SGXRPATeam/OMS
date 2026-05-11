import time
import httpx
from typing import AsyncGenerator, Optional, List, Dict
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.chatbot.core.config import chatbot_settings
from app.chatbot.core.logging import get_logger

logger = get_logger(__name__)


class LLMResponse:
    def __init__(
        self,
        content: str,
        model: str,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        latency_ms: int = 0,
        trace_id: str = "",
    ):
        self.content = content
        self.model = model
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = prompt_tokens + completion_tokens
        self.latency_ms = latency_ms
        self.trace_id = trace_id
        self.cost_estimate = 0.0


class LLMGateway:

    def __init__(self):
        self.base_url = chatbot_settings.ollama_base_url
        self.default_model = chatbot_settings.ollama_model
        self.timeout = chatbot_settings.ollama_timeout
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(self.timeout),
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
        reraise=True,
    )
    async def generate(
        self,
        messages: List[Dict[str, str]],
        trace_id: str,
        use_case_tag: str = "general",
        prompt_version: str = "v1.0",
        model: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 1024,
        tenant_id: str = "",
        user_id: str = "",
    ) -> LLMResponse:
        model = model or self.default_model
        start = time.monotonic()

        logger.info(
            "llm_call_start",
            trace_id=trace_id,
            model=model,
            use_case_tag=use_case_tag,
            prompt_version=prompt_version,
        )

        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        try:
            resp = await self._client.post("/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPStatusError as e:
            logger.error("llm_http_error", trace_id=trace_id, status=e.response.status_code)
            raise
        except Exception as e:
            logger.error("llm_call_failed", trace_id=trace_id, error=str(e))
            raise

        latency_ms = int((time.monotonic() - start) * 1000)
        content = data.get("message", {}).get("content", "")
        eval_count = data.get("eval_count", 0)
        prompt_eval_count = data.get("prompt_eval_count", 0)

        logger.info(
            "llm_call_complete",
            trace_id=trace_id,
            model=model,
            latency_ms=latency_ms,
            prompt_tokens=prompt_eval_count,
            completion_tokens=eval_count,
        )

        return LLMResponse(
            content=content,
            model=model,
            prompt_tokens=prompt_eval_count,
            completion_tokens=eval_count,
            latency_ms=latency_ms,
            trace_id=trace_id,
        )

    async def stream_generate(
        self,
        messages: List[Dict[str, str]],
        trace_id: str,
        use_case_tag: str = "general",
        model: Optional[str] = None,
        temperature: float = 0.1,
    ) -> AsyncGenerator[str, None]:
        model = model or self.default_model
        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            "options": {"temperature": temperature},
        }

        async with self._client.stream("POST", "/api/chat", json=payload) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if line:
                    import json
                    try:
                        chunk = json.loads(line)
                        token = chunk.get("message", {}).get("content", "")
                        if token:
                            yield token
                        if chunk.get("done"):
                            break
                    except json.JSONDecodeError:
                        continue

    async def embed(self, text: str, model: Optional[str] = None) -> List[float]:
        model = model or chatbot_settings.ollama_embedding_model
        payload = {"model": model, "prompt": text}
        resp = await self._client.post("/api/embeddings", json=payload)
        resp.raise_for_status()
        return resp.json().get("embedding", [])

    async def health_check(self) -> bool:
        try:
            resp = await self._client.get("/api/tags")
            return resp.status_code == 200
        except Exception:
            return False

    async def close(self):
        await self._client.aclose()


llm_gateway = LLMGateway()
