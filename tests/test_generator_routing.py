from types import SimpleNamespace

import pytest

from src.app.generation import generator as generator_module
from src.app.generation.generator import Generator


def test_offline_query_uses_ollama(monkeypatch):
    generator = Generator()
    calls = []

    def fake_ollama_chat(messages, model):
        calls.append((messages, model))
        return "local answer"

    monkeypatch.setattr(generator.ollama, "chat", fake_ollama_chat)

    result = generator.generate(
        question="question",
        context="private context",
        mode="offline",
    )

    assert result == {
        "answer": "local answer",
        "provider": "ollama",
        "model": generator_module.settings.ollama_model,
    }
    assert len(calls) == 1


def test_online_query_uses_openai(monkeypatch):
    calls = []

    class FakeCompletions:
        def create(self, **kwargs):
            calls.append(kwargs)
            message = SimpleNamespace(content="cloud answer")
            choice = SimpleNamespace(message=message)
            return SimpleNamespace(choices=[choice])

    class FakeOpenAI:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(completions=FakeCompletions())

    monkeypatch.setattr(generator_module, "OpenAI", FakeOpenAI)
    monkeypatch.setattr(
        generator_module.settings,
        "openai_api_key",
        "test-key",
    )

    generator = Generator()
    monkeypatch.setattr(
        generator.ollama,
        "chat",
        lambda *args, **kwargs: pytest.fail("Ollama must not be called"),
    )

    result = generator.generate(
        question="question",
        context="approved cloud context",
        mode="online",
    )

    assert result == {
        "answer": "cloud answer",
        "provider": "openai",
        "model": generator_module.settings.llm_model,
    }
    assert len(calls) == 1


def test_invalid_mode_does_not_call_either_provider(monkeypatch):
    generator = Generator()
    monkeypatch.setattr(
        generator.ollama,
        "chat",
        lambda *args, **kwargs: pytest.fail("Ollama must not be called"),
    )
    monkeypatch.setattr(
        generator_module,
        "OpenAI",
        lambda *args, **kwargs: pytest.fail("OpenAI must not be called"),
    )

    with pytest.raises(ValueError, match="offline.*online"):
        generator.generate("question", "context", mode="invalid")
