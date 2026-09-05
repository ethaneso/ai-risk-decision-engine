# scripts/download_reranker.py
import os
from sentence_transformers import CrossEncoder

model_dir = "./models/ms-marco-MiniLM-L-6-v2"

print("Downloading reranker model...")
model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
model.save(model_dir)
print(f"Reranker successfully saved to {model_dir}")