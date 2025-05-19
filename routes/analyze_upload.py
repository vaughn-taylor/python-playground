from flask import Blueprint, request, jsonify, current_app
import os

bp = Blueprint("analyze_upload", __name__)

@bp.route("/api/upload-earnings", methods=["POST"])
def upload_earnings():
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files["file"]
    if not file or not file.filename:
        return jsonify({"error": "No selected file"}), 400
    if not file.filename.lower().endswith(".csv"):
        return jsonify({"error": "Only CSV files are allowed"}), 400

    try:
        upload_dir = os.path.join(current_app.root_path, "static", "data", "uploads")
        os.makedirs(upload_dir, exist_ok=True)

        safe_filename = file.filename.replace(" ", "_")
        save_path = os.path.join(upload_dir, safe_filename)
        file.save(save_path)

        print(f"[UPLOAD] Saved CSV to: {save_path}")
        return jsonify({"message": f"Uploaded as '{safe_filename}'"})

    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500
    
@bp.route("/api/list-uploads", methods=["GET"])
def list_uploaded_csvs():
    try:
        upload_dir = os.path.join(current_app.root_path, "static", "data", "uploads")
        if not os.path.exists(upload_dir):
            return jsonify([])

        files = [
            f for f in os.listdir(upload_dir)
            if f.endswith(".csv") and os.path.isfile(os.path.join(upload_dir, f))
        ]
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": f"Could not list uploads: {str(e)}"}), 500
