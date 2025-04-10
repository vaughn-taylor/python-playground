# rag/embedder.py

import os
import fitz  # PyMuPDF
import pandas as pd
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient

DATA_DIR = "./data/docs"
CHROMA_DIR = "./rag/chroma_db"
CHUNK_SIZE = 500
EMBED_MODEL = "all-MiniLM-L6-v2"

client = PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection("docs")
embedder = SentenceTransformer(EMBED_MODEL)

def chunk_text(text, size=CHUNK_SIZE):
    words = text.split()
    return [" ".join(words[i:i + size]) for i in range(0, len(words), size)]

def extract_text_from_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext in [".txt", ".md"]:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    elif ext == ".csv":
        df = pd.read_csv(filepath)
        return df.to_string()
    elif ext == ".pdf":
        doc = fitz.open(filepath)
        return "\n".join(page.get_text() for page in doc)
    else:
        print(f"⚠️ Skipping unsupported file: {filepath}")
        return ""

def is_valid_file(filename):
    return not filename.startswith(".") and os.path.isfile(os.path.join(DATA_DIR, filename))

def embed_all():
    print(f"📁 Scanning {DATA_DIR} for documents...")

    for filename in os.listdir(DATA_DIR):
        if not is_valid_file(filename):
            continue

        path = os.path.join(DATA_DIR, filename)
        print(f"📄 Processing: {filename}")
        text = extract_text_from_file(path)
        if not text.strip():
            continue

        chunks = chunk_text(text)
        print(f"🧩 {filename}: {len(chunks)} chunks")

        embeddings = embedder.encode(chunks).tolist()
        ids = [f"{filename}_{i}" for i in range(len(chunks))]

        collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=[{"source": filename}] * len(chunks)
        )

    print("✅ Embedding complete. Data stored to ChromaDB.")

if __name__ == "__main__":
    embed_all()
