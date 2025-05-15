from flask import Blueprint, request, jsonify
import json
import os
import random
from rapidfuzz import process, fuzz

bp = Blueprint("autocomplete", __name__)

# ✅ Load ticker data at module level
data_path = os.path.join(os.path.dirname(__file__), "..", "static", "data", "tickers.json")
with open(os.path.abspath(data_path)) as f:
    TICKER_DATA = json.load(f)

def assign_strategy():
    """Randomly assign an A/B strategy."""
    return random.choice(["exact", "fuzzy-low", "fuzzy-aggressive"])

@bp.route("/api/autocomplete")
def autocomplete():
    q = request.args.get("q", "").strip().upper()
    mode = request.args.get("mode", "symbol")
    strategy = assign_strategy()

    if not q:
        print(f"✨ No query. Default results returned. Strategy: {strategy}", flush=True)
        return jsonify(TICKER_DATA[:100])

    if mode == "name":
        name_lookup = {
            t["name"].upper(): t
            for t in TICKER_DATA
            if isinstance(t.get("name"), str)
        }
        names = list(name_lookup.keys())

        # Strategy-dependent cutoff
        if strategy == "exact":
            score_cutoff = 90
        elif strategy == "fuzzy-low":
            score_cutoff = 40
        else:  # fuzzy-aggressive
            score_cutoff = 20 if len(q) <= 4 else 1

        matches = process.extract(
            q,
            names,
            scorer=fuzz.WRatio,
            limit=20,
            score_cutoff=score_cutoff
        )

        print("\n" + "=" * 60, flush=True)
        print(f"🔎 Autocomplete Strategy: {strategy}", flush=True)
        print(f"🔤 Query: '{q}' | Score Cutoff: {score_cutoff}", flush=True)
        print(f"🎯 Matches ({len(matches)}):", flush=True)
        print("-" * 60, flush=True)
        for name, score, _ in matches:
            symbol = name_lookup[name]["symbol"]
            print(f"{symbol:<6} | {name:<40} | Score: {score}", flush=True)
        print("=" * 60 + "\n", flush=True)

        results = [name_lookup[match[0]] for match in matches]
        return jsonify(results)

    else:  # mode == "symbol"
        matches = [
            t for t in TICKER_DATA
            if isinstance(t.get("symbol"), str) and t["symbol"].startswith(q)
        ]
        print(f"🔠 Symbol match for '{q}' → {len(matches)} results", flush=True)
        return jsonify(matches[:100])
