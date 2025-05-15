from flask import Blueprint, request, jsonify
import json
import os
from rapidfuzz import process, fuzz

bp = Blueprint("autocomplete", __name__)

# ✅ Load ticker data once at module level
data_path = os.path.join(os.path.dirname(__file__), "..", "static", "data", "tickers.json")
with open(os.path.abspath(data_path)) as f:
    TICKER_DATA = json.load(f)

@bp.route("/api/autocomplete")
def autocomplete():
    q = request.args.get("q", "").strip().upper()
    mode = request.args.get("mode", "symbol")

    if not q:
        return jsonify(TICKER_DATA[:100])

    if mode == "name":
        # Build lookup for names
        name_lookup = {
            t["name"].upper(): t
            for t in TICKER_DATA
            if isinstance(t.get("name"), str)
        }
        names = list(name_lookup.keys())

        # 🎯 Fuzzy matching with aggressive cutoff strategy
        score_cutoff = 20 if len(q) <= 4 else 1

        matches = process.extract(
            q,
            names,
            scorer=fuzz.WRatio,
            limit=20,
            score_cutoff=score_cutoff
        )

        results = [name_lookup[match[0]] for match in matches]
        return jsonify(results)

    # Default: symbol startswith match
    matches = [
        t for t in TICKER_DATA
        if isinstance(t.get("symbol"), str) and t["symbol"].startswith(q)
    ]
    return jsonify(matches[:100])
