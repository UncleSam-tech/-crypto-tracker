# cryptotracker/cli.py

import os
import sys
import argparse
import logging
from typing import List

from cryptotracker.tracker import CryptoTracker
from cryptotracker.data_manager import DataManager

# Ensure the logs directory exists
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, "tracker.log")

# Configure logging
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

def fetch_and_report(symbols: List[str], export_csv: bool):
    """Fetch prices for each symbol, save history, print stats, and optionally export CSV."""
    for sym in symbols:
        tracker = CryptoTracker(sym)
        dm = DataManager(sym)

        # Load existing history
        try:
            tracker.history = dm.load_history()
        except IOError as e:
            logging.error(f"[{sym}] Failed to load history: {e}")
            print(f"Warning: Could not load history for {sym}. Starting fresh.")
            tracker.history = []

        # Fetch current price
        try:
            price = tracker.fetch()
            print(f"{sym.upper()}: ${price:.4f}")
            logging.info(f"[{sym}] Fetched price: ${price:.4f}")
        except Exception as e:
            logging.error(f"[{sym}] Fetch error: {e}")
            print(f"Error fetching {sym}: {e}")
            continue

        # Save updated history
        try:
            dm.save_history(tracker.history)
        except IOError as e:
            logging.error(f"[{sym}] Failed to save history: {e}")
            print(f"Warning: Could not save history for {sym}.")

        # Print simple stats
        stats = tracker.stats()
        print(f"  • Min: ${stats['min']:.4f}, Max: ${stats['max']:.4f}, Avg: ${stats['avg']:.4f}")

        # Optional CSV export
        if export_csv:
            try:
                dm.export_csv(tracker.history)
                print(f"  • Exported CSV to {dm.csv_path}")
            except IOError as e:
                logging.error(f"[{sym}] CSV export error: {e}")
                print(f"Warning: Could not export CSV for {sym}.")

def main():
    parser = argparse.ArgumentParser(
        description="Fetch and analyze cryptocurrency prices."
    )
    parser.add_argument(
        "symbols",
        nargs="+",
        help="One or more crypto symbols (e.g. BTC ETH dogecoin)."
    )
    parser.add_argument(
        "-e", "--export",
        action="store_true",
        help="After fetching, export history to CSV."
    )
    args = parser.parse_args()

    fetch_and_report(args.symbols, export_csv=args.export)

if __name__ == "__main__":
    main()
