# rag/retriever.py

from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
import numpy as np

EMBED_MODEL = "all-MiniLM-L6-v2"
CHROMA_DIR = "./rag/chroma_db"

embedder = SentenceTransformer(EMBED_MODEL)
client = PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection("docs")

# 🔁 Load all chunks and vectors into memory
data = collection.get(include=["documents", "embeddings", "metadatas"])
chunks = data["documents"]
embeddings = data["embeddings"]
metadatas = data["metadatas"]

# ✅ Clean out invalid entries
valid_data = [
    (chunk, emb, meta)
    for chunk, emb, meta in zip(chunks, embeddings, metadatas)
    if chunk and emb is not None
]

if not valid_data:
    print("⚠️ Warning: No valid data found in retriever.")
else:
    print(f"✅ Loaded {len(valid_data)} valid entries into memory.")

chunks, embeddings, metadatas = zip(*valid_data) if valid_data else ([], [], [])

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def query(user_text, top_k=5):
    if not chunks:
        return []

    query_emb = embedder.encode([user_text])[0]
    scores = [cosine_similarity(query_emb, emb) for emb in embeddings]
    top_indices = np.argsort(scores)[-top_k:][::-1]
    return [(chunks[i], metadatas[i]) for i in top_indices]
