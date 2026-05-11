import time
import json
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.chatbot.core.config import chatbot_settings
from app.chatbot.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class OMSAPIResult:
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    status_code: int = 0
    latency_ms: int = 0
    endpoint: str = ""

    @property
    def formatted(self) -> str:
        if not self.success:
            return f"[OMS API Error on {self.endpoint}: {self.error}]"
        if not self.data:
            return f"[OMS API {self.endpoint}: success, no data returned]"
        return json.dumps(self.data, indent=2, default=str)


class OMSBackendClient:

    def __init__(self):
        self._client = httpx.AsyncClient(
            base_url=chatbot_settings.oms_backend_url,
            timeout=httpx.Timeout(30.0),
            headers={
                "Content-Type": "application/json",
                "X-API-Key": chatbot_settings.oms_api_key,
            },
        )

    def _headers(self, tenant_id: str, trace_id: str) -> Dict[str, str]:
        return {
            "X-Tenant-ID": tenant_id,
            "X-Trace-ID": trace_id,
            "X-Source": "oms-chatbot",
        }

    async def _get(self, path, tenant_id, trace_id, params=None) -> OMSAPIResult:
        start = time.monotonic()
        try:
            resp = await self._client.get(
                path, headers=self._headers(tenant_id, trace_id), params=params or {}
            )
            latency_ms = int((time.monotonic() - start) * 1000)
            logger.info("oms_api_get", path=path, status=resp.status_code, trace_id=trace_id)
            if resp.status_code == 200:
                return OMSAPIResult(success=True, data=resp.json(),
                                    status_code=resp.status_code, latency_ms=latency_ms, endpoint=path)
            return OMSAPIResult(success=False, error=f"HTTP {resp.status_code}: {resp.text[:200]}",
                                status_code=resp.status_code, latency_ms=latency_ms, endpoint=path)
        except Exception as e:
            latency_ms = int((time.monotonic() - start) * 1000)
            logger.error("oms_api_get_failed", path=path, error=str(e), trace_id=trace_id)
            return OMSAPIResult(success=False, error=str(e), latency_ms=latency_ms, endpoint=path)

    async def _post(self, path, tenant_id, trace_id, body=None) -> OMSAPIResult:
        start = time.monotonic()
        try:
            resp = await self._client.post(
                path, headers=self._headers(tenant_id, trace_id), json=body or {}
            )
            latency_ms = int((time.monotonic() - start) * 1000)
            logger.info("oms_api_post", path=path, status=resp.status_code, trace_id=trace_id)
            if resp.status_code in (200, 201):
                return OMSAPIResult(success=True, data=resp.json(),
                                    status_code=resp.status_code, latency_ms=latency_ms, endpoint=path)
            return OMSAPIResult(success=False, error=f"HTTP {resp.status_code}: {resp.text[:200]}",
                                status_code=resp.status_code, latency_ms=latency_ms, endpoint=path)
        except Exception as e:
            latency_ms = int((time.monotonic() - start) * 1000)
            logger.error("oms_api_post_failed", path=path, error=str(e), trace_id=trace_id)
            return OMSAPIResult(success=False, error=str(e), latency_ms=latency_ms, endpoint=path)

    async def _patch(self, path, tenant_id, trace_id, body=None) -> OMSAPIResult:
        start = time.monotonic()
        try:
            resp = await self._client.patch(
                path, headers=self._headers(tenant_id, trace_id), json=body or {}
            )
            latency_ms = int((time.monotonic() - start) * 1000)
            if resp.status_code in (200, 204):
                try:
                    data = resp.json()
                except Exception:
                    data = {"status": "updated"}
                return OMSAPIResult(success=True, data=data,
                                    status_code=resp.status_code, latency_ms=latency_ms, endpoint=path)
            return OMSAPIResult(success=False, error=f"HTTP {resp.status_code}: {resp.text[:200]}",
                                status_code=resp.status_code, latency_ms=latency_ms, endpoint=path)
        except Exception as e:
            latency_ms = int((time.monotonic() - start) * 1000)
            logger.error("oms_api_patch_failed", path=path, error=str(e), trace_id=trace_id)
            return OMSAPIResult(success=False, error=str(e), latency_ms=latency_ms, endpoint=path)

    async def _delete(self, path, tenant_id, trace_id) -> OMSAPIResult:
        start = time.monotonic()
        try:
            resp = await self._client.delete(path, headers=self._headers(tenant_id, trace_id))
            latency_ms = int((time.monotonic() - start) * 1000)
            return OMSAPIResult(
                success=resp.status_code in (200, 204),
                data={"deleted": True} if resp.status_code in (200, 204) else None,
                error=None if resp.status_code in (200, 204) else resp.text[:200],
                status_code=resp.status_code, latency_ms=latency_ms, endpoint=path
            )
        except Exception as e:
            latency_ms = int((time.monotonic() - start) * 1000)
            logger.error("oms_api_delete_failed", path=path, error=str(e), trace_id=trace_id)
            return OMSAPIResult(success=False, error=str(e), latency_ms=latency_ms, endpoint=path)

    async def get_dashboard_worklist(self, tenant_id, user_id, trace_id) -> OMSAPIResult:
        return await self._get("/dashboard/worklist", tenant_id=tenant_id, trace_id=trace_id,
                               params={"user_id": user_id})

    async def start_order_draft(self, tenant_id, user_id, trace_id, product, quantity,
                                delivery_date=None) -> OMSAPIResult:
        return await self._post("/orders/draft/start", tenant_id=tenant_id, trace_id=trace_id,
                                body={"user_id": user_id, "product": product,
                                      "quantity": quantity, "delivery_date": delivery_date})

    async def classify_order(self, tenant_id, trace_id, order_payload) -> OMSAPIResult:
        return await self._post("/orders/classify", tenant_id=tenant_id, trace_id=trace_id,
                                body=order_payload)

    async def submit_order(self, tenant_id, user_id, trace_id, order_id) -> OMSAPIResult:
        return await self._post("/orders", tenant_id=tenant_id, trace_id=trace_id,
                                body={"order_id": order_id, "user_id": user_id})

    async def cancel_order_draft(self, tenant_id, trace_id, draft_id) -> OMSAPIResult:
        return await self._delete(f"/orders/draft/{draft_id}", tenant_id=tenant_id, trace_id=trace_id)

    async def get_order_status(self, tenant_id, trace_id, order_id) -> OMSAPIResult:
        return await self._get(f"/orders/{order_id}/status", tenant_id=tenant_id, trace_id=trace_id)

    async def check_order_eligibility(self, tenant_id, trace_id, order_id) -> OMSAPIResult:
        return await self._get(f"/orders/{order_id}/eligibility", tenant_id=tenant_id, trace_id=trace_id)

    async def update_order(self, tenant_id, user_id, trace_id, order_id, updates) -> OMSAPIResult:
        return await self._patch(f"/orders/{order_id}", tenant_id=tenant_id, trace_id=trace_id,
                                 body={"user_id": user_id, **updates})

    async def raise_inquiry(self, tenant_id, user_id, trace_id, inquiry_subject,
                            inquiry_type, order_id=None, priority="medium") -> OMSAPIResult:
        return await self._post("/inquiries", tenant_id=tenant_id, trace_id=trace_id,
                                body={"user_id": user_id, "inquiry_subject": inquiry_subject,
                                      "inquiry_type": inquiry_type, "order_id": order_id,
                                      "priority": priority})

    async def get_inquiry_status(self, tenant_id, trace_id, inquiry_id) -> OMSAPIResult:
        return await self._get(f"/inquiries/{inquiry_id}", tenant_id=tenant_id, trace_id=trace_id)

    async def raise_case(self, tenant_id, user_id, trace_id, case_subject, case_type,
                         case_category, order_id=None, priority="medium", details=None) -> OMSAPIResult:
        return await self._post("/cases", tenant_id=tenant_id, trace_id=trace_id,
                                body={"user_id": user_id, "case_subject": case_subject,
                                      "case_type": case_type, "case_category": case_category,
                                      "order_id": order_id, "priority": priority,
                                      "case_details": details})

    async def get_case_status(self, tenant_id, trace_id, case_id) -> OMSAPIResult:
        return await self._get(f"/cases/{case_id}", tenant_id=tenant_id, trace_id=trace_id)

    async def create_handoff(self, tenant_id, user_id, trace_id, session_id,
                             reason, conversation_summary) -> OMSAPIResult:
        return await self._post("/handoff", tenant_id=tenant_id, trace_id=trace_id,
                                body={"user_id": user_id, "session_id": session_id,
                                      "reason": reason, "conversation_summary": conversation_summary})

    async def health_check(self) -> bool:
        try:
            resp = await self._client.get("/", timeout=5.0)
            return resp.status_code == 200
        except Exception:
            return False

    async def close(self):
        await self._client.aclose()


oms_client = OMSBackendClient()
