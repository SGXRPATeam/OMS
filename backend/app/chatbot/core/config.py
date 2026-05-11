import os
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class ChatbotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env")
        ),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────────────
    chatbot_app_version: str = "1.0.0"
    chatbot_app_env: str = "development"
    chatbot_debug: bool = True
    chatbot_log_level: str = "INFO"

    # ── Chatbot DB (async) – defaults to same server as OMS ──────
    chatbot_db_host: str = "localhost"
    chatbot_db_port: int = 5432
    chatbot_db_name: str = "OMS"
    chatbot_db_user: str = "postgres"
    chatbot_db_password: str = "1234"

    @property
    def chatbot_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.chatbot_db_user}:{self.chatbot_db_password}"
            f"@{self.chatbot_db_host}:{self.chatbot_db_port}/{self.chatbot_db_name}"
        )

    # ── Ollama ───────────────────────────────────────────────────
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"
    ollama_embedding_model: str = "nomic-embed-text"
    ollama_timeout: int = 120
    ollama_max_retries: int = 3

    # ── RAG ──────────────────────────────────────────────────────
    chunk_size: int = 512
    chunk_overlap: int = 64
    top_k_retrieval: int = 5
    reranker_top_n: int = 3
    embedding_dim: int = 768

    # ── Guardrails ───────────────────────────────────────────────
    enable_pii_detection: bool = True
    enable_prompt_injection_detection: bool = True
    enable_toxicity_check: bool = True
    max_input_tokens: int = 2000

    # ── Prompt Registry ──────────────────────────────────────────
    prompt_version: str = "v1.0"
    system_prompt_name: str = "oms_chatbot_main"

    # ── Observability ────────────────────────────────────────────
    otel_enabled: bool = False
    otel_service_name: str = "oms-chatbot-service"
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"
    enable_prometheus: bool = False
    cloud_provider: str = "local"
    k8s_cluster_name: str = "local-dev"
    k8s_namespace: str = "oms-chatbot"
    otel_export_target: str = "console"

    # ── Confidence Thresholds ────────────────────────────────────
    min_confidence_for_action: float = 0.75
    min_confidence_for_handoff: float = 0.40

    # ── OMS Backend (self-referencing when integrated) ───────────
    oms_backend_url: str = "http://localhost:8000"
    oms_api_key: str = "CHANGE_ME"

    # ── App metadata (used by telemetry) ─────────────────────────
    app_name: str = "OMS Backend"
    app_version: str = "1.0.0"
    app_env: str = "development"


@lru_cache()
def get_chatbot_settings() -> ChatbotSettings:
    return ChatbotSettings()


chatbot_settings = get_chatbot_settings()
