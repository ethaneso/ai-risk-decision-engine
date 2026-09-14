from langchain_ollama import ChatOllama

from src.app.config import settings


def get_chat_model(
    mode: str | None = None,
    model: str | None = None,
):
    if mode is None:
        provider = settings.llm_provider.lower()
    else:
        provider = {"offline": "ollama", "online": "openai"}.get(mode)
        if provider is None:
            raise ValueError("mode must be either 'offline' or 'online'")

    if provider == "ollama":
        return ChatOllama(
            base_url=settings.ollama_base_url,
            model=model or settings.ollama_model,
            temperature=0,
        )

    if provider == "openai":
        if not settings.openai_api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is required for online agent queries"
            )

        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.llm_base_url,
            model=model or settings.llm_model,
            temperature=0,
        )

    raise RuntimeError(
        f"Unsupported LLM provider: {provider}"
    )
