import uuid
import time
from typing import List, Dict, Optional, AsyncGenerator
from dataclasses import dataclass, field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.chatbot.guardrails.safety import guardrail_service
from app.chatbot.agents.intent_classifier import intent_classifier, IntentResult
from app.chatbot.agents.slot_extractor import slot_extractor
from app.chatbot.agents.action_executor import action_executor
from app.chatbot.rag.pipeline import rag_pipeline
from app.chatbot.prompts.manager import prompt_manager
from app.chatbot.llm.gateway import llm_gateway
from app.chatbot.db.models import (
    ChatHistory, AiDecisionAudit, AiEvalResults,
    TokenUsageCost, StatusSequence,
)
from app.chatbot.observability.telemetry import AISpanBuilder
from app.chatbot.core.config import chatbot_settings
from app.chatbot.core.logging import get_logger

logger = get_logger(__name__)

GREETING_KEYWORDS = {
    "hello", "hi", "hey", "good morning", "good afternoon",
    "good evening", "howdy", "greetings", "sup", "whats up",
    "start", "begin", "help me", "help",
}

GREETING_RESPONSE = (
    "Hello! I'm your OMS AI assistant. Here's what I can help you with:\n\n"
    "- **Track an order** — e.g. 'Where is my order ORD-2024-1847?'\n"
    "- **Place a new order** — e.g. 'I want to place a new order'\n"
    "- **Update an order** — e.g. 'Change the quantity on my order'\n"
    "- **Raise an enquiry** — e.g. 'I have a billing question'\n"
    "- **File a complaint or dispute** — e.g. 'I want to raise a complaint'\n"
    "- **Check case or ticket status** — e.g. 'What is the status of CASE-001?'\n"
    "- **Get policy information** — e.g. 'What is the return policy?'\n\n"
    "How can I assist you today?"
)

DEGRADED_RESPONSE = (
    "I'm sorry, I'm temporarily unable to process your request as the AI service "
    "is unavailable right now. Please try again in a moment, or contact our "
    "support team directly for immediate assistance."
)


@dataclass
class ChatRequest:
    user_message: str
    session_id: str
    tenant_id: str
    user_id: str
    conversation_history: List[Dict] = field(default_factory=list)


@dataclass
class ChatResponse:
    response: str
    session_id: str
    trace_id: str
    intent_code: str
    intent_label: str
    response_mode: str
    confidence: float
    suggested_action: Optional[str] = None
    slot_requirements: list = field(default_factory=list)
    suggestions: list = field(default_factory=list)
    requires_human_review: bool = False
    guardrail_blocked: bool = False
    blocked_reason: Optional[str] = None
    sources: list = field(default_factory=list)
    latency_ms: int = 0


class ChatbotOrchestrator:

    SUGGESTIONS_MAP: Dict[str, List[str]] = {
        "UC-04-I-04": ["Track another order", "Raise a complaint", "Speak to an agent"],
        "UC-03-I-01": ["Check order status", "Cancel this order", "Track delivery"],
        "UC-03-I-06": ["Track my order", "Raise an enquiry", "Go back to dashboard"],
        "UC-05-I-01": ["Check inquiry status", "Add more details", "Escalate to agent"],
        "UC-06-I-01": ["Track complaint status", "Speak to an agent", "View my cases"],
        "UC-06-I-02": ["Track dispute status", "Speak to an agent", "Check my orders"],
        "UC-02-I-08": ["Place a new order", "View delayed orders", "Raise an inquiry"],
        "UC-14-I-01": ["Go back to chat", "Check order status", "View my cases"],
        "UC-07":      ["Return policy", "Delivery SLA", "Speak to an agent"],
    }

    def _get_suggestions(self, intent_code: str) -> List[str]:
        return self.SUGGESTIONS_MAP.get(
            intent_code,
            self.SUGGESTIONS_MAP.get(intent_code[:5], []),
        )

    def _is_greeting(self, message: str) -> bool:
        lower = message.lower().strip().rstrip("!?.").strip()
        return lower in GREETING_KEYWORDS or (
            len(lower.split()) <= 2 and any(kw in lower for kw in GREETING_KEYWORDS)
        )

    async def _load_session_history(
        self, session_id: str, db: AsyncSession, max_turns: int = 10
    ) -> List[Dict]:
        try:
            stmt = (
                select(ChatHistory)
                .where(
                    ChatHistory.session_id == session_id,
                    ChatHistory.is_deleted == False,
                    ChatHistory.role.in_(["user", "assistant"]),
                )
                .order_by(ChatHistory.created_date.desc())
                .limit(max_turns)
            )
            result = await db.execute(stmt)
            records = result.scalars().all()
            history = []
            for r in reversed(records):
                content = r.question if r.role == "user" else r.response
                if content:
                    history.append({"role": r.role, "content": content})
            if history:
                logger.info("session_history_loaded", session_id=session_id, turns=len(history))
            return history
        except Exception as e:
            logger.warning("session_history_load_failed", session_id=session_id, error=str(e))
            return []

    async def process(self, request: ChatRequest, db: AsyncSession) -> ChatResponse:
        trace_id = str(uuid.uuid4())
        request_id = f"req_{trace_id[:8]}"
        start = time.monotonic()

        otel_span = AISpanBuilder()
        otel_span.start(
            event_name="ai_oms_request",
            trace_id=trace_id,
            request_id=request_id,
            user_id=request.user_id,
            tenant_id=request.tenant_id,
        )

        # Step 1: Greeting fast-path
        if self._is_greeting(request.user_message):
            otel_span.set_guardrail(True, False, [])
            otel_span.set_workflow("UC-00-GREET", "Greeting", "descriptive", 1.0, steps_count=1)
            otel_span.finish(
                gateway_latency_ms=int((time.monotonic() - start) * 1000),
                total_latency_ms=int((time.monotonic() - start) * 1000),
            )
            db.add(ChatHistory(
                session_id=request.session_id, tenant_id=request.tenant_id,
                user_id=request.user_id, trace_id=trace_id, role="assistant",
                response=GREETING_RESPONSE, model_version=chatbot_settings.ollama_model,
                prompt_version=chatbot_settings.prompt_version,
                intent_detected="UC-00-GREET", response_mode="descriptive",
            ))
            return ChatResponse(
                response=GREETING_RESPONSE, session_id=request.session_id,
                trace_id=trace_id, intent_code="UC-00-GREET", intent_label="Greeting",
                response_mode="descriptive", confidence=1.0,
                suggestions=["Track my order", "Place a new order", "Raise an inquiry"],
                latency_ms=int((time.monotonic() - start) * 1000),
            )

        # Step 2: Input guardrails
        guard = guardrail_service.check_input(request.user_message, trace_id)
        otel_span.set_guardrail(
            passed=guard.passed, pii_detected=guard.pii_detected,
            pii_types=guard.pii_types,
            injection_detected=guard.prompt_injection_detected,
            toxicity_detected=guard.toxicity_detected,
        )

        if not guard.passed:
            response = self._blocked_response(guard.blocked_reason)
            otel_span.set_workflow("BLOCKED", "Guardrail Block", "handoff", 0.0, steps_count=2, status="blocked")
            otel_span.finish(
                gateway_latency_ms=int((time.monotonic() - start) * 1000),
                total_latency_ms=int((time.monotonic() - start) * 1000),
            )
            db.add(ChatHistory(
                session_id=request.session_id, tenant_id=request.tenant_id,
                user_id=request.user_id, trace_id=trace_id, role="assistant",
                response=response, model_version=chatbot_settings.ollama_model,
                prompt_version=chatbot_settings.prompt_version,
                intent_detected="BLOCKED", response_mode="handoff",
            ))
            return ChatResponse(
                response=response, session_id=request.session_id,
                trace_id=trace_id, intent_code="BLOCKED", intent_label="Guardrail Block",
                response_mode="handoff", confidence=0.0,
                guardrail_blocked=True, blocked_reason=guard.blocked_reason,
                latency_ms=int((time.monotonic() - start) * 1000),
            )

        clean_message = guard.sanitised_text or request.user_message

        # Step 3: Session history
        history = request.conversation_history or []
        if not history:
            history = await self._load_session_history(request.session_id, db)

        # Step 4: Intent classification
        intent: IntentResult = intent_classifier.classify(clean_message, trace_id)
        logger.info(
            "orchestrator_intent", trace_id=trace_id,
            intent_code=intent.intent_code, response_mode=intent.response_mode,
            confidence=intent.confidence,
        )

        # Step 5: RAG retrieval
        rag_start = time.monotonic()
        chunks = await rag_pipeline.retrieve(db=db, query=clean_message, trace_id=trace_id)
        rag_latency_ms = int((time.monotonic() - rag_start) * 1000)
        rag_context = rag_pipeline.format_context(chunks)
        sources = [c.get("source_doc", "") for c in chunks]

        top_score = max((c.get("similarity", 0.0) for c in chunks), default=0.0)
        lowest_score = min((c.get("similarity", 0.0) for c in chunks), default=0.0)
        otel_span.set_rag(
            query=clean_message, docs_retrieved=len(chunks),
            docs_used=min(len(chunks), chatbot_settings.reranker_top_n),
            top_score=top_score, lowest_used_score=lowest_score,
            retrieval_latency_ms=rag_latency_ms,
        )

        # Step 6: Action execution
        action = await action_executor.execute(
            intent=intent, user_message=clean_message,
            conversation_history=history, tenant_id=request.tenant_id,
            user_id=request.user_id, session_id=request.session_id, trace_id=trace_id,
        )

        if action.needs_clarification:
            otel_span.set_workflow(intent.intent_code, intent.intent_label, "action",
                                   intent.confidence, steps_count=6, status="awaiting_slots")
            otel_span.finish(
                gateway_latency_ms=int((time.monotonic() - start) * 1000),
                total_latency_ms=int((time.monotonic() - start) * 1000),
            )
            db.add(ChatHistory(
                session_id=request.session_id, tenant_id=request.tenant_id,
                user_id=request.user_id, trace_id=trace_id, role="assistant",
                response=action.clarification_prompt, model_version=chatbot_settings.ollama_model,
                prompt_version=chatbot_settings.prompt_version,
                intent_detected=intent.intent_code, response_mode="action",
            ))
            return ChatResponse(
                response=action.clarification_prompt, session_id=request.session_id,
                trace_id=trace_id, intent_code=intent.intent_code,
                intent_label=intent.intent_label, response_mode="action",
                confidence=intent.confidence, suggested_action=intent.suggested_api,
                slot_requirements=action.slot_result.missing if action.slot_result else [],
                sources=sources,
                latency_ms=int((time.monotonic() - start) * 1000),
            )

        combined_context = "\n\n".join(filter(None, [rag_context, action.context_for_llm]))

        # Step 7: Prompt build
        messages = await prompt_manager.build_messages(
            db=db, user_message=clean_message, rag_context=combined_context,
            chat_history=history, tenant_id=request.tenant_id,
            user_id=request.user_id, session_id=request.session_id,
            intent=intent.intent_label,
        )

        # Step 8: LLM invocation
        llm_start = time.monotonic()
        try:
            llm_resp = await llm_gateway.generate(
                messages=messages, trace_id=trace_id,
                use_case_tag=intent.use_case, prompt_version=chatbot_settings.prompt_version,
                tenant_id=request.tenant_id, user_id=request.user_id,
            )
            llm_latency_ms = int((time.monotonic() - llm_start) * 1000)
            llm_content = llm_resp.content
            prompt_tokens = llm_resp.prompt_tokens
            completion_tokens = llm_resp.completion_tokens
            total_tokens = llm_resp.total_tokens
        except Exception as e:
            llm_latency_ms = int((time.monotonic() - llm_start) * 1000)
            otel_span.set_llm(chatbot_settings.ollama_model, llm_latency_ms=llm_latency_ms)
            otel_span.set_workflow(intent.intent_code, intent.intent_label, "handoff", 0.0, status="llm_error")
            otel_span.finish(
                gateway_latency_ms=0,
                total_latency_ms=int((time.monotonic() - start) * 1000),
                error=e,
            )
            logger.error("llm_unavailable", trace_id=trace_id, error=str(e))
            db.add(ChatHistory(
                session_id=request.session_id, tenant_id=request.tenant_id,
                user_id=request.user_id, trace_id=trace_id, role="assistant",
                response=DEGRADED_RESPONSE, model_version=chatbot_settings.ollama_model,
                prompt_version=chatbot_settings.prompt_version,
                intent_detected=intent.intent_code, response_mode="handoff",
            ))
            return ChatResponse(
                response=DEGRADED_RESPONSE, session_id=request.session_id,
                trace_id=trace_id, intent_code=intent.intent_code,
                intent_label=intent.intent_label, response_mode="handoff",
                confidence=0.0, requires_human_review=True,
                latency_ms=int((time.monotonic() - start) * 1000),
            )

        # Step 9: Output guardrails
        out_guard = guardrail_service.check_output(llm_content, trace_id)
        final_response = out_guard.sanitised_text or llm_content

        requires_human = (
            action.requires_human_review
            or intent.response_mode == "handoff"
            or (intent.requires_action and intent.confidence < chatbot_settings.min_confidence_for_action)
        )
        if requires_human:
            final_response += (
                "\n\n⚠️ *This request has been flagged for human agent review. "
                "A support agent will follow up shortly.*"
            )

        # Step 10: Eval + Persist
        groundedness = self._score_groundedness(final_response, combined_context)
        hallucination_flag = groundedness < 0.3 and bool(combined_context)
        gateway_latency_ms = max(int((time.monotonic() - start) * 1000) - llm_latency_ms - rag_latency_ms, 0)
        total_ms = int((time.monotonic() - start) * 1000)

        otel_span.set_workflow(
            intent.intent_code, intent.intent_label,
            intent.response_mode, intent.confidence, steps_count=9,
        )
        otel_span.set_llm(
            model=chatbot_settings.ollama_model, provider="ollama", temperature=0.1,
            prompt_tokens=prompt_tokens, completion_tokens=completion_tokens,
            total_tokens=total_tokens, llm_latency_ms=llm_latency_ms,
            prompt_version=chatbot_settings.prompt_version,
            prompt_template_id=chatbot_settings.system_prompt_name,
        )
        otel_span.set_quality(
            groundedness_score=groundedness, hallucination_flag=hallucination_flag,
            pii_flag=guard.pii_detected or out_guard.pii_detected,
        )
        otel_span.set_cost(total_tokens=total_tokens, model=chatbot_settings.ollama_model)
        otel_span.finish(
            gateway_latency_ms=gateway_latency_ms,
            total_latency_ms=total_ms,
            requires_human=requires_human,
        )

        self._add_all_records(
            db=db, request=request, trace_id=trace_id,
            user_message=clean_message, response=final_response,
            intent=intent,
            prompt_tokens=prompt_tokens, completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            requires_human=requires_human,
            groundedness=groundedness, hallucination_flag=hallucination_flag,
            pii_input=guard.pii_detected, pii_output=out_guard.pii_detected,
            latency_ms=total_ms,
            action_taken=action.action_taken,
            action_description=action.action_description,
        )

        return ChatResponse(
            response=final_response, session_id=request.session_id,
            trace_id=trace_id, intent_code=intent.intent_code,
            intent_label=intent.intent_label, response_mode=intent.response_mode,
            confidence=intent.confidence, suggested_action=intent.suggested_api,
            slot_requirements=intent.slot_requirements or [],
            suggestions=self._get_suggestions(intent.intent_code),
            requires_human_review=requires_human,
            sources=sources, latency_ms=total_ms,
        )

    def _add_all_records(
        self, db, request, trace_id, user_message, response,
        intent, prompt_tokens, completion_tokens, total_tokens,
        requires_human, groundedness, hallucination_flag,
        pii_input, pii_output, latency_ms,
        action_taken: bool = False, action_description: str = "",
    ):
        db.add(ChatHistory(
            session_id=request.session_id, tenant_id=request.tenant_id,
            user_id=request.user_id, trace_id=trace_id, role="user",
            question=user_message, model_version=chatbot_settings.ollama_model,
            prompt_version=chatbot_settings.prompt_version,
            intent_detected=intent.intent_code, use_case_tag=intent.use_case,
            response_mode=intent.response_mode,
        ))

        db.add(ChatHistory(
            session_id=request.session_id, tenant_id=request.tenant_id,
            user_id=request.user_id, trace_id=trace_id, role="assistant",
            response=response, model_version=chatbot_settings.ollama_model,
            prompt_version=chatbot_settings.prompt_version,
            intent_detected=intent.intent_code, use_case_tag=intent.use_case,
            response_mode=intent.response_mode,
        ))

        db.add(AiDecisionAudit(
            trace_id=trace_id, session_id=request.session_id, tenant_id=request.tenant_id,
            agent_name="chatbot_orchestrator",
            input_summary=user_message[:500],
            evidence_refs={"intent": intent.intent_code, "action_taken": action_taken},
            decision=f"mode={intent.response_mode}, confidence={intent.confidence:.2f}",
            confidence=intent.confidence,
            requires_human_review=requires_human,
        ))

        db.add(AiEvalResults(
            trace_id=trace_id, session_id=request.session_id,
            groundedness_score=round(groundedness, 4),
            hallucination_flag=hallucination_flag,
            pii_flag=bool(pii_input or pii_output),
            latency_ms=latency_ms,
            result_status="warn" if hallucination_flag else "pass",
            guardrail_detail={
                "pii_in_input": pii_input,
                "pii_in_output": pii_output,
                "groundedness": round(groundedness, 4),
            },
        ))

        db.add(TokenUsageCost(
            trace_id=trace_id, session_id=request.session_id, tenant_id=request.tenant_id,
            model_name=chatbot_settings.ollama_model,
            prompt_tokens=prompt_tokens or 0,
            completion_tokens=completion_tokens or 0,
            total_tokens=total_tokens or 0,
            cost_estimate=0.0, use_case_tag=intent.use_case,
        ))

        if action_taken and action_description:
            db.add(StatusSequence(
                entity_id=request.session_id, entity_type="chat_session",
                previous_status="in_progress", current_status="action_executed",
                changed_by=request.user_id, trace_id=trace_id,
                notes=action_description[:500],
            ))

        logger.info(
            "db_records_staged",
            trace_id=trace_id,
            intent=intent.intent_code,
        )

    async def stream_process(self, request: ChatRequest, db: AsyncSession) -> AsyncGenerator[str, None]:
        trace_id = str(uuid.uuid4())

        if self._is_greeting(request.user_message):
            for chunk in GREETING_RESPONSE.split(" "):
                yield f"data: {chunk} \n\n"
            yield "data: [DONE]\n\n"
            return

        guard = guardrail_service.check_input(request.user_message, trace_id)
        if not guard.passed:
            yield f"data: {self._blocked_response(guard.blocked_reason)}\n\n"
            yield "data: [DONE]\n\n"
            return

        clean_message = guard.sanitised_text or request.user_message
        history = request.conversation_history or []
        if not history:
            history = await self._load_session_history(request.session_id, db)

        intent = intent_classifier.classify(clean_message, trace_id)
        chunks = await rag_pipeline.retrieve(db=db, query=clean_message, trace_id=trace_id)
        rag_context = rag_pipeline.format_context(chunks)

        action = await action_executor.execute(
            intent=intent, user_message=clean_message,
            conversation_history=history, tenant_id=request.tenant_id,
            user_id=request.user_id, session_id=request.session_id, trace_id=trace_id,
        )
        if action.needs_clarification:
            yield f"data: {action.clarification_prompt}\n\n"
            yield "data: [DONE]\n\n"
            return

        combined_context = "\n\n".join(filter(None, [rag_context, action.context_for_llm]))
        messages = await prompt_manager.build_messages(
            db=db, user_message=clean_message, rag_context=combined_context,
            chat_history=history, tenant_id=request.tenant_id,
            user_id=request.user_id, session_id=request.session_id,
        )

        yield "data: __THINKING__\n\n"

        full_response = ""
        try:
            async for token in llm_gateway.stream_generate(
                messages=messages, trace_id=trace_id, use_case_tag=intent.use_case,
            ):
                full_response += token
                yield f"data: {token}\n\n"
        except Exception as e:
            logger.error("llm_stream_unavailable", trace_id=trace_id, error=str(e))
            yield f"data: {DEGRADED_RESPONSE}\n\n"
            yield "data: [DONE]\n\n"
            return

        yield "data: [DONE]\n\n"

        out_guard = guardrail_service.check_output(full_response, trace_id)
        final = out_guard.sanitised_text or full_response
        groundedness = self._score_groundedness(final, combined_context)
        hallucination_flag = groundedness < 0.3 and bool(combined_context)

        self._add_all_records(
            db=db, request=request, trace_id=trace_id,
            user_message=clean_message, response=final,
            intent=intent, prompt_tokens=0, completion_tokens=0, total_tokens=0,
            requires_human=False, groundedness=groundedness,
            hallucination_flag=hallucination_flag,
            pii_input=guard.pii_detected, pii_output=out_guard.pii_detected,
            latency_ms=0,
        )

    @staticmethod
    def _blocked_response(reason: str) -> str:
        return (
            f"I'm unable to process this request. {reason}. "
            "Please rephrase your message or contact support for assistance."
        )

    @staticmethod
    def _score_groundedness(response: str, context: str) -> float:
        if not context or not response:
            return 1.0
        context_words = set(context.lower().split())
        sentences = [s.strip() for s in response.split(".") if s.strip()]
        if not sentences:
            return 1.0
        grounded = sum(1 for s in sentences if set(s.lower().split()) & context_words)
        return grounded / len(sentences)


orchestrator = ChatbotOrchestrator()
