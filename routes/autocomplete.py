from flask import Blueprint, request, jsonify
import json
import os

bp = Blueprint("autocomplete", __name__)

# ✅ Load ticker data at module level
data_path = os.path.join(os.path.dirname(__file__), "..", "static", "data", "tickers.json")
with open(os.path.abspath(data_path)) as f:
    TICKER_DATA = json.load(f)

@bp.route("/api/autocomplete")
def autocomplete():
    q = request.args.get("q", "").strip().upper()
    mode = request.args.get("mode", "symbol")

    if not q:
        # ✅ No query: return top 10 symbols as default
        return jsonify(TICKER_DATA[:100])

    if mode == "name":
        matches = [t for t in TICKER_DATA if q in t["name"].upper()]
    else:  # "symbol"
        matches = [t for t in TICKER_DATA if t["symbol"].startswith(q)]

    return jsonify(matches[:100])
