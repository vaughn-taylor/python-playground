# src/backend/routes/dashboard.py
from flask import Blueprint, render_template
from src.backend.utils.assets import get_asset_path

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():
    return render_template(
        "index.html",
        get_asset_path=get_asset_path,
        page_title="Data Dashboard",
        page_icon="📊"
    )
