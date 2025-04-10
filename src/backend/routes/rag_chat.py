from flask import Blueprint, request, jsonify, render_template
from sentence_transformers import SentenceTransformer
import requests
import time
import os

from rag.retriever import query as retrieve_chunks

rag_chat_bp = Blueprint('rag_chat', __name__)
EMBED_MODEL = "all-MiniLM-L6-v2"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "mistral")

embedder = SentenceTransformer(EMBED_MODEL)

def estimate_tokens(text):
    return int(len(text.split()) * 1.3)

def trim(text, word_limit=200):
    return " ".join(text.split()[:word_limit])

def format_chunk(source, chunk, max_items=20):
    try:
        lines = chunk.splitlines()
        values = []

        for line in lines:
            parts = line.split()
            nums = [p for p in parts if p.replace(",", "").isdigit()]
            values.extend(nums)

        preview = values[:max_items]
        if preview:
            bullets = "\n".join(f"  - {val}" for val in preview)
            return f"[Source: {source}]\n{bullets}"
        else:
            return f"[Source: {source}]\n{trim(chunk)}"
    except Exception as e:
        print("❌ Chunk formatting failed:", e)
        return f"[Source: {source}]\n{trim(chunk)}"

@rag_chat_bp.route("/api/rag-chat", methods=["POST"])
def rag_chat():
    user_input = request.json.get("message", "")
    if not user_input.strip():
        return jsonify({"error": "Empty message"}), 400

    print("🔹 Step 1: Embedding user input...", flush=True)
    start_embed = time.time()

    print(f"✅ Embedding done in {time.time() - start_embed:.2f}s")

    print("🔹 Step 2: In-memory retrieval...", flush=True)
    start_query = time.time()
    top_chunks = retrieve_chunks(user_input, top_k=2)
    print(f"✅ Retrieved {len(top_chunks)} chunks in {time.time() - start_query:.2f}s", flush=True)

    if not top_chunks:
        return jsonify({
            "response": "Sorry, I couldn't find any relevant information.",
            "duration": 0.0
        })

    # Prompt construction
    context = "\n\n".join(
        format_chunk(meta.get('source', 'unknown'), chunk)
        for chunk, meta in top_chunks
    )

    prompt = f"""Answer the question using the context below.

Context:
{context}

Question:
{user_input}

Answer:"""

    token_est = estimate_tokens(prompt)
    print("📝 Final Prompt:\n" + prompt, flush=True)
    print(f"[FLASK] 📏 Estimated prompt token count: {token_est}", flush=True)
    print(f"🧠 Prompt ready. Total prep time: {time.time() - start_embed:.2f}s", flush=True)
    print("🚀 Sending prompt to Ollama...", flush=True)

    # Request Ollama
    start_ollama = time.time()
    try:
        res = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        })

        duration = time.time() - start_ollama
        print(f"[FLASK] 📬 Ollama response in {duration:.2f}s", flush=True)

        data = res.json()
        return jsonify({
            "response": data.get("response", ""),
            "duration": round(duration, 2)
        })

    except requests.exceptions.RequestException as e:
        print("❌ Request to Ollama failed:", e)
        return jsonify({
            "response": "Error: LLM request failed.",
            "duration": 0.0
        })

@rag_chat_bp.route("/rag-chat", methods=["GET"])
def rag_chat_page():
    return render_template(
        "frontend/rag-chat.html",
        page_title="Ask My Data",
        page_id="rag-chat",
        current_model=OLLAMA_MODEL
    )

@rag_chat_bp.route("/api/quick-test", methods=["POST"])
def quick_test():
    prompt = "Summarize homicide.csv in 1 sentence."
    print(f"[TEST] 🚀 Sending quick prompt to Ollama ({OLLAMA_MODEL})", flush=True)
    start = time.time()

    try:
        res = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        })

        elapsed = time.time() - start
        print(f"[TEST] ✅ Ollama responded in {elapsed:.2f}s", flush=True)

        data = res.json()
        return jsonify({
            "response": data.get("response", ""),
            "time": round(elapsed, 2)
        })

    except Exception as e:
        print("[TEST] ❌ Error during quick test:", e)
        return jsonify({"error": str(e)}), 500
