import os
import json
import csv
from typing import List, Dict, Tuple


class DataManager:
    """
    Manages data storage and retrieval for crypto price tracking.
    """
    def __init__(self, symbol: str, data_dir: str = None):
        """
        Initialize the DataManager with a filename for storage.
        """
        self.data_dir = data_dir or os.getcwd()
        self.symbol = symbol.lower()
        self.json_path = os.path.join(self.data_dir, f"{self.symbol}_history.json")
        self.csv_path = os.path.join(self.data_dir, f"{self.symbol}_history.csv")

    def save_history(self, history: List [Tuple[str, float]]) -> None:
        """
        Write history to JSON file.

        """
        try:
            with open(self.json_path, "w") as f:
                json.dump(history, f, indent=2)
        except OSError as e:
            raise OSError(f"Failed to save history to {self.json_path}: {e}")
    
    def load_history(self) -> List [Tuple[str, float]]:
        """
         Read the JSON history file and return a list of (timestamp, price).
        If the file doesn’t exist, returns an empty list.

        """
        if not os.path.exists(self.json_path):
            return[]
        try:
            with open(self.json_path, "r") as f:
                data = json.load(f)
                # Expecting a list of tuples (timestamp, price)
                return [tuple(item) for item in data]
        except (OSError, json.JSONDecodeError) as e:
            raise IOError(f"Failed to load history from: {e}")

    def export_csv(self, history: List [Tuple[str, float]]) -> None:
        """
        Export the given history to a CSV file with headers.
        """
        try:
            with open(self.csv_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Price"])
                writer.writerows(history)
        except OSError as e:
            raise OSError(f"Failed to export history to: {e}")
    
   
