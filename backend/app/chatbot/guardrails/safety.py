import re
import time
from dataclasses import dataclass, field
from typing import Optional
from app.chatbot.core.config import chatbot_settings
from app.chatbot.core.logging import get_logger

logger = get_logger(__name__)

PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(previous|all|above)\s+instructions?",
    r"disregard\s+your\s+(system|previous)\s+prompt",
    r"you\s+are\s+now\s+(a|an)\s+",
    r"act\s+as\s+if\s+you\s+(are|were)",
    r"pretend\s+(you\s+are|to\s+be)",
    r"forget\s+(everything|all)\s+(you|I)",
    r"jailbreak",
    r"DAN\s+mode",
    r"override\s+(safety|guidelines|rules)",
]

PII_PATTERNS = {
    "credit_card": r"\b(?:\d[ -]?){13,16}\b",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "email": r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
    "phone": r"\b(?:\+?\d{1,3}[\s\-]?)?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4}\b",
    "passport": r"\b[A-Z]{1,2}\d{6,9}\b",
}

TOXIC_KEYWORDS = [
    "kill", "murder", "bomb", "hack", "exploit", "destroy", "attack",
    "threaten", "harm", "illegal", "fraud", "scam",
]


@dataclass
class GuardrailResult:
    passed: bool = True
    blocked_reason: Optional[str] = None
    pii_detected: bool = False
    pii_types: list = field(default_factory=list)
    prompt_injection_detected: bool = False
    toxicity_detected: bool = False
    sanitised_text: Optional[str] = None
    latency_ms: int = 0


class GuardrailService:

    def __init__(self):
        self._injection_regexes = [
            re.compile(p, re.IGNORECASE) for p in PROMPT_INJECTION_PATTERNS
        ]
        self._pii_regexes = {
            k: re.compile(v) for k, v in PII_PATTERNS.items()
        }

    def check_input(self, text: str, trace_id: str) -> GuardrailResult:
        start = time.monotonic()
        result = GuardrailResult()

        if not text or not text.strip():
            result.passed = False
            result.blocked_reason = "Empty input"
            result.latency_ms = self._ms(start)
            return result

        word_count = len(text.split())
        if word_count > chatbot_settings.max_input_tokens:
            result.passed = False
            result.blocked_reason = f"Input exceeds maximum length ({word_count} words)"
            result.latency_ms = self._ms(start)
            logger.warning("guardrail_input_too_long", trace_id=trace_id, word_count=word_count)
            return result

        if chatbot_settings.enable_prompt_injection_detection:
            for pattern in self._injection_regexes:
                if pattern.search(text):
                    result.passed = False
                    result.prompt_injection_detected = True
                    result.blocked_reason = "Potential prompt injection detected"
                    result.latency_ms = self._ms(start)
                    logger.warning("guardrail_injection_detected", trace_id=trace_id)
                    return result

        if chatbot_settings.enable_toxicity_check:
            lower = text.lower()
            for kw in TOXIC_KEYWORDS:
                if kw in lower:
                    result.toxicity_detected = True
                    result.passed = False
                    result.blocked_reason = "Input contains potentially harmful content"
                    result.latency_ms = self._ms(start)
                    logger.warning("guardrail_toxicity_detected", trace_id=trace_id, keyword=kw)
                    return result

        if chatbot_settings.enable_pii_detection:
            detected_pii = []
            sanitised = text
            for pii_type, regex in self._pii_regexes.items():
                if regex.search(text):
                    detected_pii.append(pii_type)
                    sanitised = regex.sub(f"[{pii_type.upper()}_REDACTED]", sanitised)

            if detected_pii:
                result.pii_detected = True
                result.pii_types = detected_pii
                result.sanitised_text = sanitised
                logger.info("guardrail_pii_masked", trace_id=trace_id, pii_types=detected_pii)

        result.latency_ms = self._ms(start)
        return result

    def check_output(self, text: str, trace_id: str) -> GuardrailResult:
        start = time.monotonic()
        result = GuardrailResult()

        if not text:
            result.latency_ms = self._ms(start)
            return result

        if chatbot_settings.enable_pii_detection:
            detected_pii = []
            sanitised = text
            for pii_type, regex in self._pii_regexes.items():
                if regex.search(text):
                    detected_pii.append(pii_type)
                    sanitised = regex.sub(f"[{pii_type.upper()}_REDACTED]", sanitised)

            if detected_pii:
                result.pii_detected = True
                result.pii_types = detected_pii
                result.sanitised_text = sanitised
                logger.warning(
                    "guardrail_output_pii_redacted",
                    trace_id=trace_id,
                    pii_types=detected_pii,
                )

        result.latency_ms = self._ms(start)
        return result

    @staticmethod
    def _ms(start: float) -> int:
        return int((time.monotonic() - start) * 1000)


guardrail_service = GuardrailService()
