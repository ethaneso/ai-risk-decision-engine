from openai import OpenAI

from src.app.config import settings
from src.services.llm.ollama_client import OllamaClient


class Generator:

    def __init__(self):
        self.ollama = OllamaClient(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
        )

    def generate(
        self,
        question: str,
        context: str,
        mode: str,
        model: str | None = None,
    ):

        system_prompt = """
You are a document-grounded assistant.

Answer the user's question using only
the supplied evidence.

Rules:

1. Do not invent facts.
2. If the evidence is insufficient,
   say that the evidence is insufficient.
3. Cite the supplied SOURCE numbers.
"""

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": f"""
Evidence:

{context}

Question:

{question}
""",
            },
        ]

        if mode == "offline":
            selected_model = model or settings.ollama_model
            answer = self.ollama.chat(messages, model=selected_model)
            return {
                "answer": answer,
                "provider": "ollama",
                "model": selected_model,
            }

        if mode == "online":
            if not settings.openai_api_key:
                raise RuntimeError(
                    "OPENAI_API_KEY is required for online queries"
                )

            selected_model = model or settings.llm_model
            client = OpenAI(
                api_key=settings.openai_api_key,
                base_url=settings.llm_base_url,
            )
            response = client.chat.completions.create(
                model=selected_model,
                temperature=0,
                messages=messages,
            )
            return {
                "answer": response.choices[0].message.content,
                "provider": "openai",
                "model": selected_model,
            }

        raise ValueError("mode must be either 'offline' or 'online'")
