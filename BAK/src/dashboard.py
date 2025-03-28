from flask import Flask, render_template, request, send_from_directory
import os
import json
from datetime import datetime

# ✅ Define this before Flask uses it
def get_asset_path(logical_name):
    manifest_path = os.path.join(STATIC_DIR, "manifest.json")
    try:
        with open(manifest_path) as f:
            manifest = json.load(f)
        return "/static/" + manifest[logical_name]["file"]
    except Exception as e:
        print(f"⚠️ Error loading Vite asset: {e}")
        return "/static/" + logical_name  # fallback (e.g., during dev)

# 🔍 Set up directories
BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'static'))
TEMPLATE_DIR = os.path.abspath(os.path.join(BASE_DIR, 'templates'))
ARCHIVE_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'logs', 'archive'))

# ✅ Initialize Flask app
app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATE_DIR)

# 🏠 Home: list log files
@app.route("/")
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

    # Filter
    if log_type == "errors":
        files = [f for f in files if f["type"] == "ERROR"]
    elif log_type == "summaries":
        files = [f for f in files if f["type"] == "SUMMARY"]

    return render_template("index.html", files=files, log_type=log_type, get_asset_path=get_asset_path)

# 📄 View a file
@app.route("/view/<filename>")
def view_file(filename):
    file_path = os.path.join(ARCHIVE_DIR, filename)
    if not os.path.exists(file_path):
        return f"<h2>🚫 File not found: {filename}</h2>", 404

    with open(file_path, "r") as f:
        content = f.read()

    return render_template("view.html", filename=filename, content=content, get_asset_path=get_asset_path)

# 📦 Download a file
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(ARCHIVE_DIR, filename, as_attachment=True)

# 🧪 Run it locally
if __name__ == "__main__":
    print("📁 Template folder:", app.template_folder)
    print("📂 Archive folder:", ARCHIVE_DIR)
    app.run(debug=True)
