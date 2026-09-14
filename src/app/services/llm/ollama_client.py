import httpx


class OllamaClient:
    def __init__(self, base_url: str, model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    def chat(self, messages: list[dict], model: str | None = None) -> str:
        response = httpx.post(
            f"{self.base_url}/api/chat",
            json={
                "model": model or self.model,
                "messages": messages,
                "stream": False,
                "options": {"temperature": 0},
            },
            timeout=180.0,
        )

        response.raise_for_status()
        payload = response.json()
        return payload["message"]["content"]
