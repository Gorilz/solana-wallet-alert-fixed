import requests
from config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

class HeliusService:
    def get_transactions(self, wallet):
        url = f"https://api.helius.xyz/v0/addresses/{wallet}/transactions?api-key={Config.HELIUS_API_KEY}"
        try:
            r = requests.get(url, timeout=10)
        except requests.RequestException as e:
            logger.error(f"Helius request failed: {e}")
            return []

        if r.status_code != 200:
            logger.error(f"Helius API error {r.status_code}: {r.text}")
            return []

        data = r.json()
        if not isinstance(data, list):
            logger.error(f"Unexpected Helius response shape: {data}")
            return []

        return data
