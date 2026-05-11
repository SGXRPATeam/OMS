from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
import uuid


class MessageIn(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str


class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = Field(..., min_length=1, max_length=40)
    user_id: str = Field(..., min_length=1, max_length=80)
    message: str = Field(..., min_length=1, max_length=4000)
    conversation_history: Optional[List[MessageIn]] = Field(default_factory=list)

    @field_validator("message")
    @classmethod
    def strip_message(cls, v: str) -> str:
        return v.strip()


class ChatResponse(BaseModel):
    response: str
    session_id: str
    trace_id: str
    intent_code: str
    intent_label: str
    response_mode: str
    confidence: float
    suggested_action: Optional[str] = None
    slot_requirements: Optional[List[str]] = None
    suggestions: Optional[List[str]] = None
    requires_human_review: bool = False
    guardrail_blocked: bool = False
    blocked_reason: Optional[str] = None
    sources: Optional[List[str]] = None
    latency_ms: int


class FeedbackRequest(BaseModel):
    session_id: str
    trace_id: str
    score: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=1000)


class FeedbackResponse(BaseModel):
    status: str = "recorded"
    trace_id: str


class IngestRequest(BaseModel):
    content: str = Field(..., min_length=10)
    source_doc: str = Field(..., min_length=1, max_length=255)
    source_type: str = Field(default="document", pattern="^(document|faq|policy|order_data)$")
    metadata: Optional[Dict[str, Any]] = None


class IngestResponse(BaseModel):
    status: str
    source_doc: str
    chunks_stored: int


class HealthResponse(BaseModel):
    status: str
    db_connected: bool
    llm_connected: bool
    version: str
    model: str


class ChatHistoryItem(BaseModel):
    id: int
    role: str
    question: Optional[str]
    response: Optional[str]
    intent_detected: Optional[str]
    response_mode: Optional[str]
    created_date: datetime

    model_config = {"from_attributes": True}


class ChatHistoryResponse(BaseModel):
    session_id: str
    items: List[ChatHistoryItem]
    total: int
