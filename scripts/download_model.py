import os
from sentence_transformers import SentenceTransformer

# Define where to store the model inside your project
model_dir = "./models/all-MiniLM-L6-v2"

# Download from Hugging Face and save locally
print("Downloading model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
model.save(model_dir)
print(f"Model successfully saved to {model_dir}")