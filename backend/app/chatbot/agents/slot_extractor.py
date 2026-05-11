import re
from dataclasses import dataclass, field
from typing import Dict, Optional, List, Any
from app.chatbot.core.logging import get_logger

logger = get_logger(__name__)

PATTERNS: Dict[str, re.Pattern] = {
    "order_id":    re.compile(
        r"\b(ORD[-\s]?\d{4}[-\s]?\d{1,6}|ORDER[-\s]?\d+)\b", re.IGNORECASE
    ),
    "case_id":     re.compile(
        r"\b(CASE[-\s]?\d{4,10}|CAS[-\s]?\d+)\b", re.IGNORECASE
    ),
    "inquiry_id":  re.compile(
        r"\b(INQ[-\s]?\d{4,10}|INQUIRY[-\s]?\d+)\b", re.IGNORECASE
    ),
    "draft_id":    re.compile(
        r"\b(DRAFT[-\s]?\d{4,10})\b", re.IGNORECASE
    ),
    "quantity":    re.compile(
        r"\b(\d{1,6})\s*(units?|pcs?|pieces?|items?|qty|quantity|nos?\.?)\b",
        re.IGNORECASE
    ),
    "dispute_amount": re.compile(
        r"[$£€¥]\s*(\d[\d,]*\.?\d*)|(\d[\d,]*\.?\d*)\s*[$£€¥]|"
        r"\b(\d[\d,]*\.?\d*)\s*(dollars?|USD|GBP|EUR|INR)\b",
        re.IGNORECASE
    ),
    "delivery_date": re.compile(
        r"\b(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}|"
        r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+\d{1,2}(?:st|nd|rd|th)?,?\s*\d{4}|"
        r"\d{4}[\/\-\.]\d{1,2}[\/\-\.]\d{1,2})\b",
        re.IGNORECASE
    ),
    "inquiry_type": re.compile(
        r"\b(billing|invoice|delivery|shipping|product|technical|general|"
        r"payment|refund|warranty|returns?|complaint|dispute)\b",
        re.IGNORECASE
    ),
    "priority":    re.compile(
        r"\b(urgent|critical|high|medium|low)\s*(priority|issue|problem)?\b",
        re.IGNORECASE
    ),
    "product":     re.compile(
        r"(?:order|buy|purchase|get|for|product[:\s]+)\s+([A-Za-z0-9][A-Za-z0-9\s\-_/]{1,60}?)(?:\s*[-,.]|$)",
        re.IGNORECASE
    ),
    "complaint_subject": re.compile(
        r"(?:about|regarding|for|on)\s+(.{5,120}?)(?:\.|,|$)",
        re.IGNORECASE
    ),
    "dispute_subject": re.compile(
        r"(?:about|regarding|for|on|dispute)\s+(.{5,120}?)(?:\.|,|$)",
        re.IGNORECASE
    ),
    "inquiry_subject": re.compile(
        r"(?:about|regarding|for|on|inquiry about|enquiry about)\s+(.{5,120}?)(?:\.|,|$)",
        re.IGNORECASE
    ),
}


@dataclass
class SlotExtractionResult:
    extracted: Dict[str, Any] = field(default_factory=dict)
    missing: List[str] = field(default_factory=list)
    is_complete: bool = False
    clarification_prompt: Optional[str] = None


class SlotExtractor:

    CLARIFICATION_QUESTIONS: Dict[str, str] = {
        "order_id":          "Could you please provide your **Order ID** (e.g. ORD-2024-1847)?",
        "case_id":           "Could you please share the **Case ID** for this request?",
        "inquiry_id":        "What is the **Inquiry ID** you are referring to?",
        "draft_id":          "Please share the **Draft ID** you want to cancel.",
        "product":           "Which **product** would you like to order?",
        "quantity":          "How many **units** would you like to order?",
        "delivery_date":     "What is your preferred **delivery date**?",
        "dispute_amount":    "What is the **disputed amount** (e.g. $250.00)?",
        "complaint_subject": "Please briefly describe the **nature of your complaint**.",
        "dispute_subject":   "Please briefly describe what the **dispute is about**.",
        "inquiry_subject":   "What is your **inquiry about**?",
        "inquiry_type":      "What **type of inquiry** is this? (e.g. billing, delivery, technical, general)",
        "priority":          "How would you rate the **priority**? (urgent / high / medium / low)",
    }

    def extract(
        self,
        user_message: str,
        required_slots: List[str],
        intent_code: str,
        trace_id: str = "",
    ) -> SlotExtractionResult:
        extracted: Dict[str, Any] = {}

        for slot in required_slots:
            value = self._extract_slot(slot, user_message)
            if value is not None:
                extracted[slot] = value

        missing = [s for s in required_slots if s not in extracted]
        is_complete = len(missing) == 0

        clarification = None
        if not is_complete:
            first_missing = missing[0]
            clarification = self.CLARIFICATION_QUESTIONS.get(
                first_missing,
                f"Please provide your **{first_missing.replace('_', ' ')}**."
            )

        logger.info(
            "slot_extraction",
            trace_id=trace_id,
            intent_code=intent_code,
            required=required_slots,
            extracted=list(extracted.keys()),
            missing=missing,
            complete=is_complete,
        )

        return SlotExtractionResult(
            extracted=extracted,
            missing=missing,
            is_complete=is_complete,
            clarification_prompt=clarification,
        )

    def _extract_slot(self, slot: str, text: str) -> Optional[Any]:
        pattern = PATTERNS.get(slot)
        if not pattern:
            return None

        match = pattern.search(text)
        if not match:
            return None

        for group in match.groups():
            if group is not None:
                return group.strip()
        return match.group(0).strip()

    def build_slot_context(self, extracted: Dict[str, Any]) -> str:
        if not extracted:
            return ""
        lines = ["Extracted context from user message:"]
        for key, val in extracted.items():
            lines.append(f"  - {key.replace('_', ' ').title()}: {val}")
        return "\n".join(lines)

    def merge_with_history(
        self,
        current_extracted: Dict[str, Any],
        conversation_history: List[Dict],
        required_slots: List[str],
    ) -> Dict[str, Any]:
        merged = dict(current_extracted)
        still_missing = [s for s in required_slots if s not in merged]

        if not still_missing:
            return merged

        for turn in reversed(conversation_history[-6:]):
            content = turn.get("content", "")
            for slot in still_missing:
                if slot not in merged:
                    value = self._extract_slot(slot, content)
                    if value:
                        merged[slot] = value

        return merged


slot_extractor = SlotExtractor()
