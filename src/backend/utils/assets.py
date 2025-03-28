import os
import json

STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'static'))

def get_asset_path(logical_name):
    manifest_path = os.path.join(STATIC_DIR, ".vite", "manifest.json")
    try:
        with open(manifest_path) as f:
            manifest = json.load(f)

        # Handle CSS lookups based on manifest values
        if logical_name.endswith(".css"):
            for entry in manifest.values():
                if "css" in entry:
                    for css_file in entry["css"]:
                        if css_file.endswith(".css"):
                            return "/static/" + css_file  # ✅ use full path as written
            raise KeyError("CSS file not found in manifest")

        # JS or other asset direct lookup
        entry = manifest.get(logical_name)
        if entry and "file" in entry:
            return "/static/" + entry["file"]

        raise KeyError(f"{logical_name} not found in manifest")

    except Exception as e:
        print(f"⚠️ Error loading Vite asset ({logical_name}): {e}")
        return "/static/" + logical_name  # fallback
