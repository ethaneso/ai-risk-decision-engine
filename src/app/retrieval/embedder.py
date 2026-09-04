import os

from src.app.config import settings

# Prevent huggingface_hub from attempting any HTTP checks
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

from sentence_transformers import SentenceTransformer

class Embedder:

    def __init__(self):
        self.model = SentenceTransformer(
            settings.embedding_model
        )

    def embed_documents(
        self,
        texts: list[str]
    ):
        return self.model.encode(
            texts,
            normalize_embeddings=True
        )

    def embed_query(self, text: str):
        return self.model.encode(
            text,
            normalize_embeddings=True
        )