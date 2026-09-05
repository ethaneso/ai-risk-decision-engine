from openai import OpenAI

from src.app.config import settings


class Generator:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.llm_base_url
        )

    def generate(
        self,
        question: str,
        context: str
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

        response = self.client.chat.completions.create(
            model=settings.llm_model,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"""
Evidence:

{context}

Question:

{question}
"""
                }
            ]
        )

        return response.choices[0].message.content