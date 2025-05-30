import os
import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from sklearn.preprocessing import normalize

# ✅ Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Load your text chunks
chunks_dir = "/Users/walid/Desktop/Senior_Project/Registrar"
texts = []
file_paths = []

for filename in sorted(os.listdir(chunks_dir)):
    if filename.endswith(".txt"):
        path = os.path.join(chunks_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            texts.append(f.read())
        file_paths.append(path)

# ✅ Create embeddings
embeddings = model.encode(texts, show_progress_bar=True)

# --- Normalize embeddings for cosine similarity ---
embeddings = normalize(embeddings, axis=1)

# ✅ Store in FAISS with IndexFlatIP for inner product (cosine similarity)
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)  # Use IP instead of L2

index.add(np.array(embeddings).astype('float32'))  # Add vectors to the index

# ✅ Save FAISS index and metadata
output_dir = "/Users/walid/Desktop/Senior_Project/Faiss_Index"
os.makedirs(output_dir, exist_ok=True)

faiss.write_index(index, os.path.join(output_dir, "catalog_index.faiss"))

with open(os.path.join(output_dir, "chunk_metadata.json"), "w") as f:
    json.dump(file_paths, f)

print("✅ FAISS index and metadata saved.")
