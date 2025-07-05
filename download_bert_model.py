from sentence_transformers import SentenceTransformer
import os

# Target directory
model_path = "models/bert_model"

# Create directory if not exists
os.makedirs(model_path, exist_ok=True)

# Model name - You can change to another SentenceTransformer model if needed
model_name = "sentence-transformers/all-MiniLM-L6-v2"

print(f"Downloading model: {model_name} ...")
model = SentenceTransformer(model_name)

print(f"Saving model to {model_path} ...")
model.save(model_path)

print("✅ BERT model downloaded and saved successfully.")
