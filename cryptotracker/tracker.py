import requests
from datetime import datetime

class CryptoTracker:
    """
    Fetches and analyzes crypto prices from CoinGecko API.
    """
    API_URL = "https://api.coingecko.com/api/v3"

    def __init__(self, symbol: str):
        """
        Initialize the CryptoTracker with a list of crypto IDs.
        """
        self.symbol = symbol.lower()
        self.history = []

    def fetch(self) -> float:
        """
        Fetch the latest prices."""

        params = {"ids": self.symbol, "vs_currencies": "usd"}
        url = f"{self.API_URL}/simple/price"
        resp = requests.get(url, params=params, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        price = data[self.symbol]["usd"]
        ts = datetime.now().isoformat()
        self.history.append((ts, price))
        return price
    
    def stats(self) -> dict:
        """ Return min, max, avg of tracked prices """
        prices = [p for _, p in self.history]
        return {
            "min": min(prices),
            "max": max(prices),
            "avg": sum(prices) / len(prices) if prices else None
        }
