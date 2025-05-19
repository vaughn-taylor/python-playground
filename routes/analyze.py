from flask import Blueprint, request, jsonify, render_template, current_app, Response
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from typing import Union
import pandas as pd
import os

bp = Blueprint("analyze", __name__)

# 🔑 Create LLM instance
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")  # type: ignore
)

# 🎯 Analysis UI page
@bp.route("/analyze", methods=["GET"])
def analyze_page() -> str:
    return render_template("analyze.html", page_id="analyze")

# 🧠 Analysis API endpoint
@bp.route("/api/analyze", methods=["POST"])
def analyze() -> Union[Response, tuple[Response, int]]:
    data = request.get_json() or {}
    query = data.get("query", "").strip()
    selected_file = data.get("selected_file", "").strip()

    if not query:
        return jsonify({"error": "No query provided"}), 400
    if not selected_file:
        return jsonify({"error": "No CSV file selected"}), 400

    try:
        uploads_dir = os.path.join(current_app.root_path, "static", "data", "uploads")
        csv_path = os.path.join(uploads_dir, selected_file)

        print(f"[DEBUG] Attempting to load CSV at: {csv_path}")

        if not os.path.exists(csv_path):
            return jsonify({"error": f"File not found: {selected_file}"}), 404

        df = pd.read_csv(csv_path)
        if df.empty:
            return jsonify({"error": "CSV is empty"}), 500

        agent = create_pandas_dataframe_agent(
            llm,  # type: ignore
            df,
            verbose=True
        )

        response = agent.run(query)
        return jsonify({"result": response})

    except Exception as e:
        return jsonify({"error": f"Agent error: {str(e)}"}), 500
