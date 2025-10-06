from typing import List, Dict, Any
from .models import Message


class ConversationManager:
    def __init__(self, short_context_size: int = 10):
        self.short_context_size = short_context_size
        self.messages: List[Message] = []
        self.short_term_summary: str = ""
        self.long_term_facts: List[Dict[str, Any]] = []

    def add_message(self, role: str, content: str) -> None:
        self.messages.append(Message(role=role, content=content))
        self._maintain_summary()
        self._extract_and_store_facts(content, role)

    def get_context(self) -> Dict[str, Any]:
        recent = self.messages[-self.short_context_size :]
        return {
            "summary": self.short_term_summary,
            "recent": [{"role": m.role, "content": m.content} for m in recent],
            "facts": self.long_term_facts,
        }

    def _maintain_summary(self) -> None:
        if len(self.messages) <= self.short_context_size:
            return
        older = self.messages[: -self.short_context_size]
        bullet_points: List[str] = []
        for msg in older:
            prefix = "U:" if msg.role == "user" else ("A:" if msg.role == "assistant" else "S:")
            snippet = msg.content.strip().replace("\n", " ")
            if len(snippet) > 200:
                snippet = snippet[:197] + "..."
            bullet_points.append(f"- {prefix} {snippet}")
        self.short_term_summary = "\n".join(bullet_points)

    def _extract_and_store_facts(self, content: str, role: str) -> None:
        if role != "user":
            return
        extracted = self._naive_fact_extractor(content)
        if extracted:
            self.long_term_facts.extend(extracted)

    def _naive_fact_extractor(self, text: str) -> List[Dict[str, Any]]:
        text_l = text.lower()
        facts: List[Dict[str, Any]] = []
        if "my name is" in text_l:
            parts = text.split("my name is", 1)
            if len(parts) > 1:
                name = parts[1].strip().split()[0].rstrip(".,!")
                facts.append({"type": "user_name", "value": name})
        if "i prefer" in text_l:
            parts = text.split("i prefer", 1)
            if len(parts) > 1:
                pref = parts[1].strip().rstrip(".,!")
                facts.append({"type": "preference", "value": pref})
        if "timezone" in text_l and ("utc" in text_l or "+" in text_l or "-" in text_l):
            facts.append({"type": "timezone_hint", "value": text})
        return facts


