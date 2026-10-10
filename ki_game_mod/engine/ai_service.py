from .provider import TemplateProvider

class AIService:
    """Safe offline AI provider; does not execute generated code."""
    def __init__(self): self.provider = TemplateProvider()
    def generate(self, prompt, context=None):
        return {"reply": self.provider.generate(prompt, context), "provider": "offline-template", "requires_review": True}
