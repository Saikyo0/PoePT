import langchain
from langchain.llms.base import LLM
from typing import Optional, List, Dict, Any
from .poept import PoePT  # Assuming the provided PoePT code is in a module named poept

class PoeLLM(LLM):
    def __init__(self, email: str, bot: str = "Assistant"):
        super().__init__()
        self.email = email
        self.bot = bot
        self.poe = PoePT()
        self.poe.login(email)

    def close(self):
        self.poe.close()

    def _generate(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> str:
        return self.poe.ask(prompt, bot=self.bot)

    @property
    def _llm_type(self) -> str:
        return "Poe"

    def __del__(self):
        self.close()