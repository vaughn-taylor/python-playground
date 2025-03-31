from flask import Blueprint, render_template, jsonify
from src.backend.utils.assets import get_asset_path
import csv
import os

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():
    return render_template(
        "index.html",
        get_asset_path=get_asset_path,
        page_title="Data Dashboard",
        page_icon="📊"
    )

@dashboard_bp.route("/api/sales")
def api_sales():
    sales_data = []
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'sales.csv'))
    try:
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                sales_data.append({
                    "date": row["date"],
                    "total": int(row["total"])
                })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(sales_data)
