import re
from dataclasses import dataclass
from typing import Optional
from app.chatbot.core.config import chatbot_settings
from app.chatbot.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class IntentResult:
    intent_code: str
    intent_label: str
    use_case: str
    response_mode: str
    confidence: float
    requires_action: bool
    suggested_api: Optional[str] = None
    slot_requirements: list = None


INTENT_CATALOGUE = [
    # UC-01 Login & Tenant
    {
        "code": "UC-01-I-01", "label": "Login help", "use_case": "UC-01",
        "mode": "descriptive", "api": None,
        "keywords": ["login", "sign in", "password", "access", "account", "credential"],
    },
    # UC-02 Dashboard
    {
        "code": "UC-02-I-01", "label": "Dashboard navigation", "use_case": "UC-02",
        "mode": "descriptive", "api": None,
        "keywords": ["dashboard", "home", "navigate", "overview", "worklist"],
    },
    {
        "code": "UC-02-I-08", "label": "Summarise dashboard", "use_case": "UC-02",
        "mode": "hybrid", "api": "GET /dashboard/worklist",
        "keywords": ["summarize", "summarise", "priorities", "pending", "worklist", "today items", "attention"],
    },
    # UC-03 Order Initiation
    {
        "code": "UC-03-I-01", "label": "Start new order", "use_case": "UC-03",
        "mode": "action", "api": "POST /orders/draft/start",
        "slots": ["product", "quantity", "delivery_date"],
        "keywords": ["place order", "start order", "new order", "create order", "order now", "want to order"],
    },
    {
        "code": "UC-03-I-02", "label": "Classify order type", "use_case": "UC-03",
        "mode": "hybrid", "api": "POST /orders/classify",
        "keywords": ["standard order", "non-standard", "custom order", "special order", "classify"],
    },
    {
        "code": "UC-03-I-06", "label": "Submit order", "use_case": "UC-03",
        "mode": "action", "api": "POST /orders",
        "slots": ["order_id"],
        "keywords": ["submit order", "confirm order", "finalise order", "place the order"],
    },
    {
        "code": "UC-03-I-08", "label": "Cancel draft order", "use_case": "UC-03",
        "mode": "action", "api": "DELETE /orders/draft/{id}",
        "slots": ["draft_id"],
        "keywords": ["cancel order", "discard draft", "cancel draft", "don't want"],
    },
    # UC-04 Non-Standard / Classification
    {
        "code": "UC-04-I-01", "label": "Non-standard order request", "use_case": "UC-04",
        "mode": "hybrid", "api": "POST /orders/classify/orderable",
        "slots": ["product", "quantity"],
        "keywords": [
            "non-standard order", "non standard order",
            "place a non-standard", "want a non-standard",
            "custom order request", "bespoke order",
            "special order request", "non-catalogue order",
        ],
    },
    {
        "code": "UC-04-I-04", "label": "Track order status", "use_case": "UC-04",
        "mode": "hybrid", "api": "GET /orders/{id}/status",
        "slots": ["order_id"],
        "keywords": ["track order", "order status", "where is my order", "order update", "delivery status"],
    },
    {
        "code": "UC-04-I-01", "label": "Update order quantity", "use_case": "UC-04",
        "mode": "action", "api": "PATCH /orders/{id}",
        "slots": ["order_id", "quantity"],
        "keywords": ["update order", "change quantity", "modify order", "amend order"],
    },
    # UC-05 Inquiry Management
    {
        "code": "UC-05-I-01", "label": "Raise new inquiry", "use_case": "UC-05",
        "mode": "action", "api": "POST /inquiries",
        "slots": ["inquiry_subject", "inquiry_type"],
        "keywords": ["raise inquiry", "new inquiry", "submit inquiry", "ask question", "enquiry"],
    },
    {
        "code": "UC-05-I-03", "label": "Track inquiry status", "use_case": "UC-05",
        "mode": "hybrid", "api": "GET /inquiries/{id}",
        "slots": ["inquiry_id"],
        "keywords": ["inquiry status", "ticket status", "case status", "where is my ticket"],
    },
    # UC-06 Complaint & Dispute
    {
        "code": "UC-06-I-01", "label": "Raise complaint", "use_case": "UC-06",
        "mode": "action", "api": "POST /cases",
        "slots": ["complaint_subject", "order_id"],
        "keywords": ["complaint", "raise complaint", "file complaint", "not satisfied", "issue with order"],
    },
    {
        "code": "UC-06-I-02", "label": "Raise dispute", "use_case": "UC-06",
        "mode": "action", "api": "POST /cases",
        "slots": ["dispute_subject", "order_id", "dispute_amount"],
        "keywords": ["dispute", "raise dispute", "billing issue", "wrong charge", "overcharged"],
    },
    # UC-14 Handoff
    {
        "code": "UC-14-I-01", "label": "Human agent escalation", "use_case": "UC-14",
        "mode": "handoff", "api": None,
        "keywords": ["speak to agent", "talk to human", "escalate", "transfer", "real person", "supervisor"],
    },
    {
        "code": "UC-14-I-05", "label": "Chat logging & audit", "use_case": "UC-14",
        "mode": "descriptive", "api": None,
        "keywords": ["logged", "recorded", "audit", "retention", "stored", "privacy", "consent"],
    },
]


class IntentClassifier:

    def classify(self, user_message: str, trace_id: str = "") -> IntentResult:
        lower = user_message.lower()
        best_match = None
        best_score = 0

        for intent in INTENT_CATALOGUE:
            score = 0
            for kw in intent.get("keywords", []):
                if kw in lower:
                    score += len(kw.split())

            if score > best_score:
                best_score = score
                best_match = intent

        if best_match and best_score > 0:
            confidence = min(0.95, 0.50 + (best_score * 0.05))
            result = IntentResult(
                intent_code=best_match["code"],
                intent_label=best_match["label"],
                use_case=best_match["use_case"],
                response_mode=best_match["mode"],
                confidence=confidence,
                requires_action=best_match["mode"] in ("action", "hybrid"),
                suggested_api=best_match.get("api"),
                slot_requirements=best_match.get("slots", []),
            )
        else:
            result = IntentResult(
                intent_code="UC-00-I-00",
                intent_label="General / Unknown",
                use_case="UC-00",
                response_mode="descriptive",
                confidence=0.35,
                requires_action=False,
            )

        if result.confidence < chatbot_settings.min_confidence_for_handoff:
            result.response_mode = "handoff"

        logger.info(
            "intent_classified",
            trace_id=trace_id,
            intent_code=result.intent_code,
            mode=result.response_mode,
            confidence=result.confidence,
        )
        return result


intent_classifier = IntentClassifier()
