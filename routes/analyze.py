from flask import Blueprint, request, jsonify, render_template, current_app, Response
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from typing import Union
import pandas as pd
import os

bp = Blueprint("analyze", __name__)

# 🔒 System message to prevent plotting libraries
system_prompt = SystemMessage(
    content=(
        "You are a financial data assistant. "
        "Never import or use matplotlib, seaborn, or any plotting libraries. "
        "Do not generate visualizations yourself. "
        "Only return structured data summaries or calculations that can be charted externally."
    )
)

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
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

        # 🔍 Analyze via LangChain agent
        # 🧠 Create LangChain agent with safe prompt
        agent = create_pandas_dataframe_agent(
            llm,
            df,
            verbose=True,
            max_iterations=20,
            early_stopping_method="generate",
            handle_parsing_errors=True,
            prefix=(
                "You are a financial data assistant. "
                "Do not import or use matplotlib, seaborn, or any plotting libraries. "
                "Do not generate plots. Only return summaries or structured data that can be charted by the frontend."
            )
        )

        print("[DEBUG] DataFrame preview:", df.head(3).to_string())
        print("[DEBUG] DataFrame columns:", df.columns.tolist())

        response = agent.invoke(query)
        answer = response.get("output", "No result returned.")

        # 📈 Try to build chart data if user requests visualization
        chart_data = None
        chart_type = data.get("chart_type", "bar")  # 🆕 Get from request

        if any(keyword in query.lower() for keyword in ["chart", "plot", "graph", "visualize"]):
            try:
                df_chart = df.copy()
                df_chart["year"] = pd.to_datetime(df_chart["date"]).dt.year
                df_chart["quarter"] = pd.to_datetime(df_chart["date"]).dt.to_period("Q").astype(str)

                if "revenue" in query.lower() or "eps" in query.lower():
                    target_col = "revenue" if "revenue" in query.lower() else "eps"

                    if "year" in query.lower():
                        grouped = df_chart.groupby("year")[target_col].sum()
                        chart_data = {
                            "labels": [str(label) for label in grouped.index],
                            "values": [int(v) for v in grouped.values]
                        }

                    elif "quarter" in query.lower():
                        grouped = df_chart.groupby("quarter")[target_col].sum()
                        chart_data = {
                            "labels": [str(label) for label in grouped.index],
                            "values": [int(v) for v in grouped.values]
                        }

            except Exception as chart_err:
                print(f"[DEBUG] Chart extraction failed: {chart_err}")

        return jsonify({
            "result": answer,
            "chart": chart_data,
            "chart_type": chart_type  # 🆕 Echo back to frontend if needed
        })

    except Exception as e:
        return jsonify({"error": f"Agent error: {str(e)}"}), 500
