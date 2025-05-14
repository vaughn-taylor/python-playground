# src/routes/finance_chat.py

from flask import Blueprint, render_template, request, jsonify

finance_chat_bp = Blueprint("finance_chat", __name__)

@finance_chat_bp.route("/")
def finance_chat_index():
    """Render the finance chat homepage."""
    return render_template("index.html", page_id="finance-chat")

@finance_chat_bp.route("/api/finance-chat", methods=["POST"])
def finance_chat_query():
    """Process finance chat queries from the frontend."""
    query = request.json.get("query", "").strip()
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Placeholder logic for testing
    return jsonify({"response": f"You asked: {query}"})
