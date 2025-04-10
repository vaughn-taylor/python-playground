# rag/ask.py

import sys
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb import PersistentClient
import requests

CHROMA_DIR = "./rag/chroma_db"
OLLAMA_URL = "http://localhost:11434/api/generate"
EMBED_MODEL = "all-MiniLM-L6-v2"

# 🧠 Init embedding + vector DB
print("📦 Loading vector store and embedding model...")
client = PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection("docs")
embedder = SentenceTransformer(EMBED_MODEL)

# 📥 Get user question
if len(sys.argv) < 2:
    print("❓ Usage: python rag/ask.py \"your question here\"")
    sys.exit(1)

question = sys.argv[1]
print(f"\n🧠 Question: {question}")

# 📐 Embed and retrieve context
print("🔎 Embedding question and retrieving relevant context...")
query_embedding = embedder.encode([question]).tolist()[0]
results = collection.query(query_embeddings=[query_embedding], n_results=5)

chunks = results.get("documents", [[]])[0]
metadatas = results.get("metadatas", [[]])[0]

if not chunks:
    print("⚠️ No relevant documents found. Try re-running embedder or checking /data/docs.")
    sys.exit(1)

# 🧩 Annotate each chunk with its source
context = "\n\n".join(
    f"[Source: {meta['source'] if isinstance(meta, dict) and 'source' in meta else 'unknown'}]\n{doc}"
    for doc, meta in zip(chunks, metadatas)
)

print(f"📄 Retrieved {len(chunks)} chunk(s) from ChromaDB.")

# 🧪 Preview the context we're sending to LLaMA
print("\n🧾 Preview of context:\n")
print(context[:500] + ("..." if len(context) > 500 else ""))

# 🦙 Ask LLaMA
prompt = f"""Answer the question using the context below.

Context:
{context}

Question:
{question}

Answer:"""

print("\n🚀 Sending prompt to LLaMA 3...")

try:
    response = requests.post(OLLAMA_URL, json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })

    if response.status_code != 200:
        print("❌ Error from LLaMA:", response.text)
    else:
        print("\n🧠 Response:\n")
        print(response.json()["response"])

except requests.exceptions.ConnectionError:
    print("❌ Could not connect to Ollama. Is it running?")
