# api/price.py

import json
from urllib.parse import parse_qs

from cryptotracker.tracker import CryptoTracker
from cryptotracker.data_manager import DataManager

def handler(request):
    """
    Query params:
      ?symbol=BTC
    Returns JSON:
      {
        "symbol": "BTC",
        "price": 12345.67,
        "stats": { "min": ..., "max": ..., "avg": ... }
      }
    """
    # Vercel provides the raw URL-encoded body; parse it
    qs = parse_qs(request.environ["QUERY_STRING"])
    symbols = qs.get("symbol", [])
    if not symbols:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing ?symbol= parameter"})
        }

    sym = symbols[0]
    tracker = CryptoTracker(sym)
    dm = DataManager(sym)

    # Load previous history if any
    try:
        tracker.history = dm.load_history()
    except IOError:
        tracker.history = []

    # Fetch current price
    try:
        price = tracker.fetch()
    except Exception as e:
        return {
            "statusCode": 502,
            "body": json.dumps({"error": f"Fetch failed: {e}"})
        }

    # Save history
    try:
        dm.save_history(tracker.history)
    except IOError:
        pass  # non-fatal

    # Build response
    stats = tracker.stats()
    payload = {
        "symbol": sym.upper(),
        "price": price,
        "stats": stats
    }
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(payload)
    }
