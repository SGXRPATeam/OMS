import uuid
from datetime import datetime
from typing import Optional, Dict
from sqlalchemy import (
    String, Text, Integer, Boolean, DateTime, Float,
    BigInteger, Index, func
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from app.chatbot.db.session import Base


def gen_uuid() -> str:
    return str(uuid.uuid4())


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    tenant_id: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    trace_id: Mapped[str] = mapped_column(String(80), nullable=False, index=True)

    role: Mapped[str] = mapped_column(String(20), nullable=False)
    question: Mapped[Optional[str]] = mapped_column(Text)
    response: Mapped[Optional[str]] = mapped_column(Text)
    intent_detected: Mapped[Optional[str]] = mapped_column(String(100))
    use_case_tag: Mapped[Optional[str]] = mapped_column(String(100))

    prompt_version: Mapped[str] = mapped_column(String(20), default="v1.0")
    model_version: Mapped[str] = mapped_column(String(80), nullable=False)
    response_mode: Mapped[Optional[str]] = mapped_column(String(40))

    feedback_score: Mapped[Optional[int]] = mapped_column(Integer)
    feedback_comment: Mapped[Optional[str]] = mapped_column(Text)

    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)


class AiDecisionAudit(Base):
    __tablename__ = "ai_decision_audit"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    trace_id: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    session_id: Mapped[str] = mapped_column(String(40), nullable=False)
    tenant_id: Mapped[str] = mapped_column(String(40), nullable=False)

    agent_name: Mapped[str] = mapped_column(String(100), nullable=False)
    input_summary: Mapped[Optional[str]] = mapped_column(Text)
    evidence_refs: Mapped[Optional[Dict]] = mapped_column(JSONB)
    decision: Mapped[Optional[str]] = mapped_column(Text)
    confidence: Mapped[Optional[float]] = mapped_column(Float)
    approver: Mapped[Optional[str]] = mapped_column(String(80))
    requires_human_review: Mapped[bool] = mapped_column(Boolean, default=False)

    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class AiEvalResults(Base):
    __tablename__ = "ai_eval_results"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    trace_id: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    session_id: Mapped[str] = mapped_column(String(40), nullable=False)

    groundedness_score: Mapped[Optional[float]] = mapped_column(Float)
    relevance_score: Mapped[Optional[float]] = mapped_column(Float)
    hallucination_flag: Mapped[bool] = mapped_column(Boolean, default=False)
    pii_flag: Mapped[bool] = mapped_column(Boolean, default=False)
    toxicity_flag: Mapped[bool] = mapped_column(Boolean, default=False)
    prompt_injection_flag: Mapped[bool] = mapped_column(Boolean, default=False)
    latency_ms: Mapped[Optional[int]] = mapped_column(Integer)
    result_status: Mapped[str] = mapped_column(String(40), default="pass")
    guardrail_detail: Mapped[Optional[Dict]] = mapped_column(JSONB)

    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class TokenUsageCost(Base):
    __tablename__ = "token_usage_cost"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    trace_id: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    session_id: Mapped[str] = mapped_column(String(40), nullable=False)
    tenant_id: Mapped[str] = mapped_column(String(40), nullable=False)

    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    prompt_tokens: Mapped[int] = mapped_column(Integer, default=0)
    completion_tokens: Mapped[int] = mapped_column(Integer, default=0)
    total_tokens: Mapped[int] = mapped_column(Integer, default=0)
    cost_estimate: Mapped[float] = mapped_column(Float, default=0.0)
    business_unit: Mapped[Optional[str]] = mapped_column(String(80))
    use_case_tag: Mapped[Optional[str]] = mapped_column(String(100))

    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class IncidentRemediation(Base):
    __tablename__ = "incident_remediation"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    incident_id: Mapped[str] = mapped_column(String(40), unique=True, default=gen_uuid, index=True)
    trace_id: Mapped[Optional[str]] = mapped_column(String(80), index=True)
    source_system: Mapped[str] = mapped_column(String(80), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), default="medium")
    root_cause: Mapped[Optional[str]] = mapped_column(Text)
    action_taken: Mapped[Optional[str]] = mapped_column(Text)
    closed_status: Mapped[bool] = mapped_column(Boolean, default=False)
    closed_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class PromptRegistry(Base):
    __tablename__ = "prompt_registry"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    prompt_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    prompt_version: Mapped[str] = mapped_column(String(20), nullable=False)
    use_case_tag: Mapped[Optional[str]] = mapped_column(String(100))
    template_text: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    approved_by: Mapped[Optional[str]] = mapped_column(String(80))
    approved_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    notes: Mapped[Optional[str]] = mapped_column(Text)

    created_by: Mapped[Optional[str]] = mapped_column(String(80))
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index("ix_prompt_name_version", "prompt_name", "prompt_version", unique=True),
    )


class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunk"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    chunk_id: Mapped[str] = mapped_column(String(40), unique=True, default=gen_uuid)
    source_doc: Mapped[str] = mapped_column(String(255), nullable=False)
    source_type: Mapped[str] = mapped_column(String(40), default="document")
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, default=0)
    metadata_json: Mapped[Optional[Dict]] = mapped_column(JSONB)

    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (
        Index("ix_knowledge_source", "source_doc", "source_type"),
    )


class StatusSequence(Base):
    __tablename__ = "status_sequence"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    entity_id: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(40), nullable=False)
    previous_status: Mapped[Optional[str]] = mapped_column(String(40))
    current_status: Mapped[str] = mapped_column(String(40), nullable=False)
    changed_by: Mapped[str] = mapped_column(String(80), nullable=False)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    trace_id: Mapped[str] = mapped_column(String(80), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text)
