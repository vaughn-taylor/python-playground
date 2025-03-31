from flask import Blueprint, render_template, jsonify, request
from src.backend.utils.assets import get_asset_path
from datetime import datetime
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
    start = request.args.get("start")
    end = request.args.get("end")

    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'sales.csv'))

    try:
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                date_str = row["date"]
                total = int(row["total"])

                # Robust date filter using datetime objects
                if start and end:
                    try:
                        start_dt = datetime.strptime(start, "%Y-%m-%d")
                        end_dt = datetime.strptime(end, "%Y-%m-%d")
                        row_dt = datetime.strptime(date_str, "%Y-%m-%d")

                        if not (start_dt <= row_dt <= end_dt):
                            continue
                    except ValueError:
                        continue  # skip rows with invalid dates

                sales_data.append({"date": date_str, "total": total})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(sales_data)
