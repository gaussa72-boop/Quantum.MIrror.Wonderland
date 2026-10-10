from abc import ABC, abstractmethod
from typing import Any

class AIProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, context: dict[str, Any] | None = None) -> str: ...

class TemplateProvider(AIProvider):
    def generate(self, prompt, context=None):
        return f"AI MOD RESPONSE: {str(prompt).strip()}"
