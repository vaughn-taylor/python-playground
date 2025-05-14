import os
import json

STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

# Check multiple possible manifest paths
manifest_paths = [
    os.path.join(STATIC_DIR, '.vite', 'manifest.json'),
    os.path.join(STATIC_DIR, 'assets', '.vite', 'manifest.json'),
]

# Use the first one that exists
for path in manifest_paths:
    if os.path.exists(path):
        MANIFEST_PATH = path
        break
else:
    MANIFEST_PATH = None  # fallback behavior will trigger

def get_asset_path(logical_name):
    try:
        if not MANIFEST_PATH:
            raise FileNotFoundError("Vite manifest.json not found in known locations.")

        with open(MANIFEST_PATH) as f:
            manifest = json.load(f)

        # ✅ Lookup for JS
        if logical_name.endswith(".js"):
            entry = manifest.get("assets/" + logical_name) or manifest.get(logical_name)
            if entry and "file" in entry:
                return "/static/assets/" + entry["file"]

        # ✅ Lookup for CSS from main.js
        if logical_name.endswith(".css"):
            js_entry = manifest.get("main.js")
            if js_entry and "css" in js_entry:
                return "/static/assets/" + js_entry["css"][0]

        raise KeyError(f"{logical_name} not found in manifest")

    except Exception as e:
        print(f"⚠️ Error loading Vite asset ({logical_name}): {e}")
        return "/static/" + logical_name  # fallback
