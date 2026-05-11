from typing import Optional, Dict, Any
from jinja2 import Environment, BaseLoader, TemplateError, StrictUndefined
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.chatbot.db.models import PromptRegistry
from app.chatbot.core.config import chatbot_settings
from app.chatbot.core.logging import get_logger

logger = get_logger(__name__)

_prompt_cache: Dict[str, str] = {}

JINJA_ENV = Environment(loader=BaseLoader(), undefined=StrictUndefined)


class PromptManager:

    async def get_prompt(
        self,
        db: AsyncSession,
        prompt_name: str,
        version: Optional[str] = None,
    ) -> Optional[str]:
        version = version or chatbot_settings.prompt_version
        cache_key = f"{prompt_name}:{version}"

        if cache_key in _prompt_cache:
            return _prompt_cache[cache_key]

        stmt = (
            select(PromptRegistry)
            .where(
                PromptRegistry.prompt_name == prompt_name,
                PromptRegistry.prompt_version == version,
                PromptRegistry.is_active == True,
            )
        )
        result = await db.execute(stmt)
        record = result.scalar_one_or_none()

        if not record:
            logger.warning("prompt_not_found", prompt_name=prompt_name, version=version)
            return None

        _prompt_cache[cache_key] = record.template_text
        return record.template_text

    def render(self, template_text: str, context: Dict[str, Any]) -> str:
        try:
            tmpl = JINJA_ENV.from_string(template_text)
            return tmpl.render(**context)
        except TemplateError as e:
            logger.error("prompt_render_failed", error=str(e))
            return template_text

    async def build_messages(
        self,
        db: AsyncSession,
        user_message: str,
        rag_context: str,
        chat_history: list,
        tenant_id: str,
        user_id: str,
        session_id: str,
        intent: str = "",
    ) -> list:
        template = await self.get_prompt(db, chatbot_settings.system_prompt_name)

        if not template:
            rendered_system = (
                "You are the OMS AI assistant. Help users with orders, cases, and inquiries. "
                "Be concise, accurate, and never fabricate data."
            )
        else:
            rendered_system = self.render(template, {
                "tenant_id": tenant_id,
                "user_id": user_id,
                "session_id": session_id,
                "rag_context": rag_context or "No additional context retrieved.",
                "chat_history": self._format_history(chat_history),
                "user_message": user_message,
            })

        messages = [{"role": "system", "content": rendered_system}]

        for turn in chat_history[-6:]:
            messages.append({"role": turn["role"], "content": turn["content"]})

        messages.append({"role": "user", "content": user_message})
        return messages

    @staticmethod
    def _format_history(history: list) -> str:
        if not history:
            return "No prior conversation."
        lines = []
        for h in history[-4:]:
            role = h.get("role", "user").capitalize()
            content = h.get("content", "")[:300]
            lines.append(f"{role}: {content}")
        return "\n".join(lines)

    def invalidate_cache(self, prompt_name: str, version: str):
        _prompt_cache.pop(f"{prompt_name}:{version}", None)


prompt_manager = PromptManager()
