# src/backend/routes/logs.py
from flask import Blueprint, render_template, request
from src.backend.utils.assets import get_asset_path
from src.backend.utils.log_utils import get_log_files, load_file_content
import os


logs_bp = Blueprint("logs", __name__)
ARCHIVE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'logs', 'archive'))

@logs_bp.route("/")
def index():
    log_type = request.args.get("type")
    files = get_log_files(log_type)  # You’ll need to use your actual file loader

    return render_template(
        "logs.html",
        files=files,
        log_type=log_type,
        get_asset_path=get_asset_path,
        page_title="Logs",
        page_icon="📁"
    )

@logs_bp.route("/view/<filename>")
def view_file(filename):
    content = load_file_content(filename)  # Use your actual loader here

    return render_template(
        "view.html",
        filename=filename,
        content=content,
        get_asset_path=get_asset_path,
        page_title="View File",
        page_icon="📄"
    )
