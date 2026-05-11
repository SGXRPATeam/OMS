from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from app.chatbot.agents.intent_classifier import IntentResult
from app.chatbot.agents.slot_extractor import slot_extractor, SlotExtractionResult
from app.chatbot.agents.oms_client import oms_client, OMSAPIResult
from app.chatbot.core.config import chatbot_settings
from app.chatbot.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ActionResult:
    action_taken: bool = False
    api_result: Optional[OMSAPIResult] = None
    slot_result: Optional[SlotExtractionResult] = None
    needs_clarification: bool = False
    clarification_prompt: Optional[str] = None
    requires_human_review: bool = False
    context_for_llm: str = ""
    action_description: str = ""


class ActionExecutor:

    async def execute(
        self,
        intent: IntentResult,
        user_message: str,
        conversation_history: List[Dict],
        tenant_id: str,
        user_id: str,
        session_id: str,
        trace_id: str,
    ) -> ActionResult:
        if intent.response_mode in ("descriptive", "handoff"):
            return ActionResult(action_taken=False)

        is_write = self._is_write_action(intent.intent_code)
        if is_write and intent.confidence < chatbot_settings.min_confidence_for_action:
            logger.warning(
                "action_confidence_too_low",
                trace_id=trace_id,
                intent=intent.intent_code,
                confidence=intent.confidence,
            )
            return ActionResult(
                action_taken=False,
                requires_human_review=True,
                context_for_llm=(
                    "[SYSTEM NOTE: This action requires human review due to low confidence. "
                    "Inform the user a support agent will follow up.]"
                ),
                action_description=f"Write action {intent.intent_code} blocked: confidence {intent.confidence:.2f}",
            )

        required_slots = intent.slot_requirements or []
        if required_slots:
            extracted = slot_extractor.extract(
                user_message=user_message,
                required_slots=required_slots,
                intent_code=intent.intent_code,
                trace_id=trace_id,
            )
            if not extracted.is_complete:
                merged = slot_extractor.merge_with_history(
                    current_extracted=extracted.extracted,
                    conversation_history=conversation_history,
                    required_slots=required_slots,
                )
                missing_after_merge = [s for s in required_slots if s not in merged]
                if missing_after_merge:
                    first_missing = missing_after_merge[0]
                    clarification = slot_extractor.CLARIFICATION_QUESTIONS.get(
                        first_missing,
                        f"Please provide your **{first_missing.replace('_', ' ')}**.",
                    )
                    return ActionResult(
                        action_taken=False,
                        slot_result=extracted,
                        needs_clarification=True,
                        clarification_prompt=clarification,
                        context_for_llm=(
                            f"[SLOT COLLECTION IN PROGRESS for {intent.intent_code}]\n"
                            f"Still needed: {', '.join(missing_after_merge)}\n"
                            f"Ask the user: {clarification}"
                        ),
                        action_description=f"Awaiting slot: {first_missing}",
                    )
                extracted.extracted = merged
                extracted.missing = []
                extracted.is_complete = True
        else:
            extracted = SlotExtractionResult(extracted={}, missing=[], is_complete=True)

        result = await self._route(
            intent=intent, slots=extracted.extracted,
            tenant_id=tenant_id, user_id=user_id,
            session_id=session_id, trace_id=trace_id,
        )

        slot_ctx = slot_extractor.build_slot_context(extracted.extracted)
        if result.success:
            ctx = (
                f"[OMS LIVE DATA — {intent.intent_code}]\n"
                f"{slot_ctx}\n"
                f"API Response:\n{result.formatted}"
            )
        else:
            ctx = (
                f"[OMS API UNAVAILABLE — {intent.intent_code}]\n"
                f"{slot_ctx}\n"
                f"Error: {result.error}\n"
                "[SYSTEM NOTE: Inform the user the system is temporarily unavailable.]"
            )

        return ActionResult(
            action_taken=True,
            api_result=result,
            slot_result=extracted,
            needs_clarification=False,
            context_for_llm=ctx,
            action_description=f"Executed {result.endpoint}",
        )

    async def _route(self, intent, slots, tenant_id, user_id, session_id, trace_id) -> OMSAPIResult:
        code = intent.intent_code

        if code == "UC-02-I-08":
            return await oms_client.get_dashboard_worklist(
                tenant_id=tenant_id, user_id=user_id, trace_id=trace_id)

        if code == "UC-03-I-01":
            return await oms_client.start_order_draft(
                tenant_id=tenant_id, user_id=user_id, trace_id=trace_id,
                product=slots.get("product", ""), quantity=slots.get("quantity", ""),
                delivery_date=slots.get("delivery_date"))

        if code == "UC-03-I-02":
            return await oms_client.classify_order(
                tenant_id=tenant_id, trace_id=trace_id, order_payload=slots)

        if code == "UC-03-I-06":
            return await oms_client.submit_order(
                tenant_id=tenant_id, user_id=user_id, trace_id=trace_id,
                order_id=slots.get("order_id", ""))

        if code == "UC-03-I-08":
            return await oms_client.cancel_order_draft(
                tenant_id=tenant_id, trace_id=trace_id, draft_id=slots.get("draft_id", ""))

        if code == "UC-04-I-04":
            return await oms_client.get_order_status(
                tenant_id=tenant_id, trace_id=trace_id, order_id=slots.get("order_id", ""))

        if code == "UC-04-I-01":
            eligibility = await oms_client.check_order_eligibility(
                tenant_id=tenant_id, trace_id=trace_id, order_id=slots.get("order_id", ""))
            if not eligibility.success:
                return eligibility
            update_payload = {k: v for k, v in slots.items() if k != "order_id"}
            return await oms_client.update_order(
                tenant_id=tenant_id, user_id=user_id, trace_id=trace_id,
                order_id=slots.get("order_id", ""), updates=update_payload)

        if code == "UC-05-I-01":
            return await oms_client.raise_inquiry(
                tenant_id=tenant_id, user_id=user_id, trace_id=trace_id,
                inquiry_subject=slots.get("inquiry_subject", ""),
                inquiry_type=slots.get("inquiry_type", "general"),
                order_id=slots.get("order_id"), priority=slots.get("priority", "medium"))

        if code == "UC-05-I-03":
            return await oms_client.get_inquiry_status(
                tenant_id=tenant_id, trace_id=trace_id, inquiry_id=slots.get("inquiry_id", ""))

        if code in ("UC-06-I-01", "UC-06-I-02"):
            case_type = "dispute" if code == "UC-06-I-02" else "complaint"
            subject_key = "dispute_subject" if code == "UC-06-I-02" else "complaint_subject"
            return await oms_client.raise_case(
                tenant_id=tenant_id, user_id=user_id, trace_id=trace_id,
                case_subject=slots.get(subject_key, slots.get("inquiry_subject", "")),
                case_type=case_type, case_category="customer_service",
                order_id=slots.get("order_id"), priority=slots.get("priority", "medium"),
                details=slots.get("dispute_amount", ""))

        if code == "UC-14-I-01":
            return await oms_client.create_handoff(
                tenant_id=tenant_id, user_id=user_id, trace_id=trace_id,
                session_id=session_id, reason="Customer requested human agent",
                conversation_summary="[Auto-generated from session history]")

        logger.warning("action_executor_no_route", trace_id=trace_id, intent_code=code)
        return OMSAPIResult(
            success=False, error=f"No API route defined for intent {code}", endpoint="unknown")

    @staticmethod
    def _is_write_action(intent_code: str) -> bool:
        write_codes = {
            "UC-03-I-01", "UC-03-I-06", "UC-03-I-08",
            "UC-04-I-01", "UC-05-I-01",
            "UC-06-I-01", "UC-06-I-02",
            "UC-14-I-01",
        }
        return intent_code in write_codes


action_executor = ActionExecutor()
