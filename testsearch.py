import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
from sklearn.preprocessing import normalize

# Load FAISS index and metadata
index = faiss.read_index("/Users/walid/Desktop/Senior_Project/Faiss_Index/catalog_index.faiss")
with open("/Users/walid/Desktop/Senior_Project/Faiss_Index/chunk_metadata.json") as f:
    file_paths = json.load(f)

print(f"✅ Loaded FAISS index with {index.ntotal} vectors.")
print(f"✅ Loaded {len(file_paths)} metadata entries.\n")

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

while True:
    query = input("🔎 Enter your query (or type 'exit' to quit): ").strip()
    if query.lower() in ["exit", "quit", "q"]:
        print("👋 Exiting.")
        break

    # Encode and normalize query
    query_vector = model.encode([query])
    query_vector = normalize(query_vector, axis=1)

    # Search FAISS index
    D, I = index.search(query_vector.astype('float32'), k=3)

    # Gather content for prompt
    retrieved_chunks = []
    print("\n🔍 Top results:\n")
    for rank, idx in enumerate(I[0]):
        file_path = file_paths[idx]
        print(f"Result {rank+1}:\nFile path: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read(3000)
                cleaned = content.strip().replace("\n", " ").replace("  ", " ")
                print("Preview:", cleaned[:300] + "...")
                retrieved_chunks.append(f"Source {rank+1}:\n{cleaned}")
        except Exception as e:
            print(f"❌ Could not read file: {e}")

        print("\n" + "-" * 80 + "\n")

    # Build LLM prompt
    if retrieved_chunks:
        print("🧠 Suggested Prompt for LLM:\n")
        context = "\n\n".join(retrieved_chunks)
        prompt = (
            "You are an AI assistant that helps answer student questions strictly based on official university registrar information. "
            "This includes rules about registration, class schedules, attendance, grading, withdrawals, exams, and academic policies.\n\n"
            "Before answering, check that the following question is related to the registrar domain. "
            "If it is not, politely respond that this question falls outside the registrar's scope.\n\n"
            "Then, use the documents below to answer the question accurately and clearly. "
            "Only use information that is directly supported by the retrieved content.\n\n"
            "Retrieved documents:\n\n"
            f"{context}\n\n"
            f"Student's question:\n{query}\n\n"
            "Answer:"
        )
        print(prompt)
