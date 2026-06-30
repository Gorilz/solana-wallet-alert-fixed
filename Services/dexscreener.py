import requests
from utils.logger import get_logger

logger = get_logger(__name__)

DEXSCREENER_URL = "https://api.dexscreener.com/latest/dex/tokens/{mint}"


class DexScreenerService:
    """Looks up liquidity and market cap for a token mint via the free DexScreener API."""

    def get_token_stats(self, mint):
        """
        Returns a dict {symbol, liquidity_usd, market_cap_usd} for the token's
        most liquid trading pair, or None if no data is available.
        """
        try:
            r = requests.get(DEXSCREENER_URL.format(mint=mint), timeout=10)
        except requests.RequestException as e:
            logger.error(f"DexScreener request failed for {mint}: {e}")
            return None

        if r.status_code != 200:
            logger.error(f"DexScreener API error {r.status_code} for {mint}")
            return None

        data = r.json()
        pairs = data.get("pairs") or []
        if not pairs:
            return None

        # Use the pair with the most liquidity as the representative price/cap source
        best = max(pairs, key=lambda p: (p.get("liquidity") or {}).get("usd") or 0)

        liquidity = (best.get("liquidity") or {}).get("usd")
        market_cap = best.get("marketCap") or best.get("fdv")
        symbol = (best.get("baseToken") or {}).get("symbol")

        if liquidity is None or market_cap is None:
            return None

        return {
            "symbol": symbol or mint[:4],
            "liquidity_usd": liquidity,
            "market_cap_usd": market_cap,
        }
