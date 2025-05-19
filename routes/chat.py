from flask import Blueprint, render_template, request, jsonify
from openai import OpenAI
import os
import re

bp = Blueprint("chat", __name__)

# 🧠 Step 1: Symbol extractor helper
def extract_symbol(text: str) -> str | None:
    # Simple regex for ticker-like patterns: 2–5 uppercase letters
    matches = re.findall(r"\b[A-Z]{2,5}\b", text)
    return matches[0] if matches else None

@bp.route("/")
def chat_index():
    return render_template("index.html", page_id="chat")

@bp.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "No query provided"}), 400

    symbol = extract_symbol(query) or "an unspecified company"

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful financial assistant. The user is asking about {symbol}. Provide concise, accurate answers."
                },
                {"role": "user", "content": query}
            ],
            temperature=0.2,
        )

        answer = (response.choices[0].message.content or "").strip()
        return jsonify({"response": answer, "symbol": symbol})

    except Exception as e:
        return jsonify({"error": f"OpenAI error: {str(e)}"}), 500

