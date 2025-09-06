import os
import requests
import json
from typing import Any

class DeepSeekAIClient:
    """
    Provider para usar a API do DeepSeek.
    Requer: AI_PROVIDER=deepseek e DEEPSEEK_API_KEY no .env
    """

    def __init__(self) -> None:
        self.api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise RuntimeError("DEEPSEEK_API_KEY não configurada.")
        self.model = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
        self.base_url = "https://api.deepseek.com/chat/completions"

    def classify_and_reply(self, email_text: str, classifications: dict[str, str], company_context: dict[str, Any]) -> dict[str, str]:
        prompt = f"""
            Você é um assistente que ajuda a classificar emails recebidos por uma empresa com o seguinte contexto (JSON):

            {company_context}

            As possíveis classificações para o e-mail estão detalhadas a seguir (JSON):

            {classifications}
            
            Sua tarefa é analisar o conteúdo do email e responder em formato JSON com duas chaves:

            "classification": opção de classificação mais adequada.
            "reply_suggestion": uma resposta curta, polida e adequada para enviar ao remetente.

            Email recebido:

            {email_text}  

            Responda apenas no formato JSON, por exemplo:

            {{
                "classification": "produtivo",
                "reply_suggestion": "Olá, recebemos sua solicitação e estamos verificando. Em breve retornaremos com mais informações."
            }}
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        body = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }

        resp = requests.post(self.base_url, headers=headers, json=body, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        raw_text = data["choices"][0]["message"]["content"]

        result = json.loads(raw_text)

        return result
