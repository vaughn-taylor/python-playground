# src/backend/routes/logs.py
from flask import Blueprint, render_template, request, send_from_directory
from src.backend.utils.assets import get_asset_path
from src.backend.utils.log_utils import get_log_files, load_file_content, LOGS_DIR
from datetime import datetime
import os

logs_bp = Blueprint("logs", __name__)
ARCHIVE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'logs', 'archive'))

@logs_bp.route("/")
def index():
    log_type = request.args.get("type")
    files = get_log_files(log_type)

    return render_template(
        "frontend/logs.html",
        files=files,
        log_type=log_type,
        get_asset_path=get_asset_path,
        page_title="Logs",
        page_icon="📁"
    )

@logs_bp.route("/view/<filename>")
def view_file(filename):
    content = load_file_content(filename)

    return render_template(
        "frontend/view.html",
        filename=filename,
        content=content,
        get_asset_path=get_asset_path,
        page_title="View File",
        page_icon="📄"
    )

@logs_bp.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(
        LOGS_DIR,
        filename,
        as_attachment=True
    )

@logs_bp.route("/archive/<filename>")
def download_archive(filename):
    return send_from_directory(
        ARCHIVE_DIR,
        filename,
        as_attachment=True
    )

@logs_bp.route("/archive")
def archive_index():
    archived_files = []
    try:
        for filename in os.listdir(ARCHIVE_DIR):
            path = os.path.join(ARCHIVE_DIR, filename)
            if os.path.isfile(path):
                stat = os.stat(path)
                archived_files.append({
                    "name": filename,
                    "type": _detect_type(filename),
                    "size_kb": round(stat.st_size / 1024, 2),
                    "modified": datetime.fromtimestamp(stat.st_mtime)
                })
    except Exception as e:
        print(f"Error loading archived logs: {e}")

    return render_template(
        "frontend/archive.html",
        files=sorted(archived_files, key=lambda f: f["modified"], reverse=True),
        get_asset_path=get_asset_path,
        page_title="Archived Logs",
        page_icon="🗃️"
    )

def _detect_type(filename):
    if "error" in filename.lower():
        return "ERROR"
    elif "summary" in filename.lower():
        return "SUMMARY"
    else:
        return "LOG"
