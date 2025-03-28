from flask import Blueprint, render_template, request, send_from_directory
from datetime import datetime
import os

from src.backend.utils.assets import get_asset_path

logs_bp = Blueprint("logs", __name__)
ARCHIVE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'logs', 'archive'))

@logs_bp.route("/")
def index():
    log_type = request.args.get("type")
    files = []

    try:
        all_files = sorted(os.listdir(ARCHIVE_DIR))
    except FileNotFoundError:
        all_files = []
        print(f"⚠️ Archive directory not found: {ARCHIVE_DIR}")

    for filename in all_files:
        full_path = os.path.join(ARCHIVE_DIR, filename)
        try:
            modified = os.path.getmtime(full_path)
            size = os.path.getsize(full_path)

            files.append({
                "name": filename,
                "modified": datetime.fromtimestamp(modified),
                "size_kb": round(size / 1024, 1),
                "type": (
                    "ERROR" if filename.startswith("errors_only_") else
                    "SUMMARY" if filename.startswith("log_summary_") else
                    "OTHER"
                )
            })
        except Exception as e:
            print(f"⚠️ Skipping unreadable file '{filename}': {e}")

    if log_type == "errors":
        files = [f for f in files if f["type"] == "ERROR"]
    elif log_type == "summaries":
        files = [f for f in files if f["type"] == "SUMMARY"]

    return render_template("index.html", files=files, log_type=log_type, get_asset_path=get_asset_path)

@logs_bp.route("/view/<filename>")
def view_file(filename):
    file_path = os.path.join(ARCHIVE_DIR, filename)
    if not os.path.exists(file_path):
        return f"<h2>🚫 File not found: {filename}</h2>", 404

    with open(file_path, "r") as f:
        content = f.read()

    return render_template("view.html", filename=filename, content=content, get_asset_path=get_asset_path)

@logs_bp.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(ARCHIVE_DIR, filename, as_attachment=True)
