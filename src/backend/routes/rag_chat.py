# rag_chat.py

from flask import Blueprint, request, stream_with_context, Response, render_template
from sentence_transformers import SentenceTransformer
import requests
import json
import time
import os

from rag.retriever import query as retrieve_chunks  # ✅ In-memory fast path

rag_chat_bp = Blueprint('rag_chat', __name__)

# 🔧 Config
EMBED_MODEL = "all-MiniLM-L6-v2"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3")

# 🔁 Load embedder once
embedder = SentenceTransformer(EMBED_MODEL)

@rag_chat_bp.route("/api/rag-chat", methods=["POST"])
def rag_chat():
    user_input = request.json.get("message", "")
    if not user_input.strip():
        return {"error": "Empty message"}, 400

    print("🔹 Step 1: Embedding user input...", flush=True)
    t0 = time.time()
    # Even though the embedder is inside retriever, we time from here for total duration
    chunks_with_meta = retrieve_chunks(user_input, top_k=5)
    t_retrieve = time.time() - t0
    print(f"✅ Retrieved {len(chunks_with_meta)} chunks in {t_retrieve:.2f}s", flush=True)

    if not chunks_with_meta:
        return {"response": "Sorry, I couldn't find any relevant information."}

    context = "\n\n".join(
        f"[Source: {meta.get('source', 'unknown')}]\n{chunk}"
        for chunk, meta in chunks_with_meta
    )

    prompt = f"""Answer the question using the context below.

Context:
{context}

Question:
{user_input}

Answer:"""

    print(f"🧠 Prompt ready. Total prep time: {t_retrieve:.2f}s", flush=True)
    print("🚀 Sending prompt to Ollama...", flush=True)

    def generate():
        try:
            start_ollama = time.time()
            response = requests.post(OLLAMA_URL, json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": True
            }, stream=True)

            first_token_received = False
            full_output = ""

            for line in response.iter_lines():
                if not line:
                    continue
                try:
                    data = json.loads(line.decode("utf-8"))
                    token = data.get("response", "")
                    if token:
                        if not first_token_received:
                            latency = time.time() - start_ollama
                            print(f"[FLASK] 📬 First token in {latency:.2f}s", flush=True)
                            first_token_received = True
                        full_output += token
                        yield token
                    elif data.get("done", False):
                        yield "\n"
                        print(f"[FLASK] ✅ Stream finished in {time.time() - start_ollama:.2f}s", flush=True)
                except json.JSONDecodeError as e:
                    print("❌ JSON decode error:", e, flush=True)

        except requests.exceptions.RequestException as e:
            print("❌ Request to Ollama failed:", e, flush=True)

    return Response(stream_with_context(generate()), content_type='text/plain')


@rag_chat_bp.route("/rag-chat", methods=["GET"])
def rag_chat_page():
    return render_template(
        "frontend/rag-chat.html",
        page_title="Ask My Data",
        page_id="rag-chat",
        current_model=OLLAMA_MODEL
    )
