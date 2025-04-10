# rag/retriever.py

from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
import numpy as np

EMBED_MODEL = "all-MiniLM-L6-v2"
CHROMA_DIR = "./rag/chroma_db"
SIMILARITY_THRESHOLD = 0.5  # Tune if needed

embedder = SentenceTransformer(EMBED_MODEL)
client = PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection("docs")

print("[RETRIEVER] 🔍 Loading embeddings into memory...")

data = collection.get(include=["documents", "embeddings", "metadatas"])
raw_chunks = data.get("documents", [])
raw_embeddings = data.get("embeddings", [])
raw_metadatas = data.get("metadatas", [])

valid_data = [
    (chunk, emb, meta)
    for chunk, emb, meta in zip(raw_chunks, raw_embeddings, raw_metadatas)
    if chunk and emb is not None
]

if not valid_data:
    print("⚠️ Warning: No valid entries found in ChromaDB.")
    chunks, embeddings, metadatas, emb_matrix = [], [], [], np.array([])
    source_lookup = {}
    source_embeddings = np.array([])
else:
    chunks, embeddings, metadatas = zip(*valid_data)
    emb_matrix = np.array(embeddings)

    sources = sorted(set(meta.get("source", "unknown") for meta in metadatas))
    source_lookup = {src: [] for src in sources}
    for chunk, meta in zip(chunks, metadatas):
        source_lookup[meta.get("source", "unknown")].append((chunk, meta))

    source_embeddings = embedder.encode(sources)
    print(f"✅ Loaded {len(chunks)} chunks from {len(sources)} source files.")

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10)

def query(user_text, top_k=5):
    if not chunks or emb_matrix.size == 0:
        print("⚠️ No data available for retrieval.")
        return []

    query_vec = embedder.encode([user_text])[0]

    # 🔍 Match the query against source filenames
    source_scores = [cosine_similarity(query_vec, vec) for vec in source_embeddings]
    matched_sources = [
        source for source, score in zip(source_lookup.keys(), source_scores)
        if score >= SIMILARITY_THRESHOLD
    ]
    print(f"[RETRIEVER] 🧠 Matched sources: {matched_sources}")

    filtered_chunks, filtered_embeddings, filtered_metadatas = [], [], []
    for src in matched_sources:
        for chunk, meta in source_lookup[src]:
            idx = chunks.index(chunk)
            filtered_chunks.append(chunk)
            filtered_embeddings.append(embeddings[idx])
            filtered_metadatas.append(meta)

    if not filtered_chunks:
        return []

    matrix = np.array(filtered_embeddings)
    query_norm = np.linalg.norm(query_vec)
    scores = np.dot(matrix, query_vec) / (np.linalg.norm(matrix, axis=1) * query_norm + 1e-10)
    top_indices = np.argsort(scores)[-top_k:][::-1]

    return [(filtered_chunks[i], filtered_metadatas[i]) for i in top_indices]
