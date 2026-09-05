from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # =========================================================
    # Application
    # =========================================================

    app_name: str = "AI Risk Decision Engine"
    app_version: str = "0.1.0"
    environment: str = "development"


    # =========================================================
    # PostgreSQL
    # =========================================================

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "airisk"
    postgres_password: str = "airisk_dev_password"
    postgres_db: str = "airisk"

    database_url: str | None = None


    # =========================================================
    # Vector Database
    # =========================================================

    # Current architecture:
    # PostgreSQL + pgvector
    #
    # Qdrant is NOT required for the current implementation.

    vector_db: str = "pgvector"


    # =========================================================
    # Embedding Model
    # =========================================================

    embedding_model: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    embedding_dimension: int = 384


    # =========================================================
    # RAG
    # =========================================================

    top_k: int = 10

    rerank_top_k: int = 5

    chunk_size: int = 1000

    chunk_overlap: int = 200


    # =========================================================
    # LLM
    # =========================================================

    llm_provider: str = "ollama"


    # =========================================================
    # Ollama / Local LLM
    # =========================================================

    ollama_base_url: str = "http://localhost:11434"

    ollama_model: str = "llama3.1:8b"


    # =========================================================
    # Online LLM
    # =========================================================

    openai_api_key: str | None = None

    llm_model: str = "gpt-4o"

    llm_base_url: str = "https://api.openai.com/v1"  # Sets default if not in .env

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


    # =========================================================
    # Configuration
    # =========================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()