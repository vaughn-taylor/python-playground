# src/backend/utils/log_utils.py

import os
from datetime import datetime

LOGS_DIR = os.path.abspath(os.path.join(__file__, "..", "..", "..", "logs"))

def get_log_files(log_type=None):
    try:
        files = []
        for filename in os.listdir(LOGS_DIR):
            filepath = os.path.join(LOGS_DIR, filename)

            if not os.path.isfile(filepath):
                continue

            # 🔍 Normalize log type filtering
            if log_type:
                match_keywords = {
                    "errors": "errors_only",
                    "summaries": "log_summary",
                }
                keyword = match_keywords.get(log_type.lower())
                if keyword and keyword not in filename.lower():
                    continue

            file_stat = os.stat(filepath)
            file_info = {
                "name": filename,
                "type": _detect_type(filename),
                "size_kb": round(file_stat.st_size / 1024, 2),
                "modified": datetime.fromtimestamp(file_stat.st_mtime)
            }
            files.append(file_info)

        return sorted(files, key=lambda f: f["modified"], reverse=True)

    except Exception as e:
        print(f"Error loading logs: {e}")
        return []

def load_file_content(filename):
    try:
        filepath = os.path.join(LOGS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def _detect_type(filename):
    if "error" in filename.lower():
        return "ERROR"
    elif "summary" in filename.lower():
        return "SUMMARY"
    else:
        return "LOG"
