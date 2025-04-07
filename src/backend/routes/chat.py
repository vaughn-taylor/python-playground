from flask import Blueprint, request, Response, render_template, stream_with_context
import requests
import json  # ✅ This was missing!

chat_bp = Blueprint('chat', __name__)

OLLAMA_URL = 'http://localhost:11434/api/generate'

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    print(f"📥 Received message: {user_message}")

    payload = {
        "model": "mistral",
        "prompt": user_message,
        "stream": True
    }

    def generate():
        with requests.post(OLLAMA_URL, json=payload, stream=True) as r:
            for line in r.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode("utf-8"))
                        yield chunk.get("response", "")
                    except Exception as e:
                        print("❌ Error decoding chunk:", e)
                        continue

    return Response(stream_with_context(generate()), mimetype="text/plain")


@chat_bp.route('/chat', methods=['GET'])
def chat_page():
    return render_template('frontend/chat.html', page_title="Local LLM Chat")
