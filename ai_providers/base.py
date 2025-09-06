from abc import ABC, abstractmethod
from typing import Any

class AIClient(ABC):
    @abstractmethod
    def classify_and_reply(self, email_text: str, classifications: dict[str, str], company_context: dict[str, Any]) -> dict[str, str]:
        """
        Deve retornar algo como:
        {
          "classification": Opção entre opções de "classifications",
          "reply_suggestion": "Texto sugerido de resposta"
        }
        """
        ...
