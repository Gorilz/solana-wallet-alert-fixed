import json, os
from services.helius import HeliusService
from services.dexscreener import DexScreenerService
from utils.logger import get_logger
from config import Config

logger = get_logger(__name__)

# Solana's native mint placeholder / wrapped SOL — not a "token launch", skip cap filtering for it
NATIVE_SOL_MINT = "So11111111111111111111111111111111111111112"


class WalletMonitor:
    def __init__(self, telegram):
        self.telegram = telegram
        self.helius = HeliusService()
        self.dexscreener = DexScreenerService()
        self.wallet = Config.WATCH_WALLET

        self.file = "data/seen_tokens.json"
        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.file):
            with open(self.file, "w") as f:
                json.dump([], f)

    def load_seen(self):
        with open(self.file) as f:
            return set(json.load(f))

    def save_seen(self, seen):
        with open(self.file, "w") as f:
            json.dump(list(seen), f)

    def _passes_filters(self, mint):
        """
        Returns (passes: bool, stats: dict|None). A token passes if its market cap is at
        or below MARKETCAP_LIMIT and its liquidity is at or above MIN_LIQUIDITY. If no
        market data can be found, the token is excluded (fails) since we can't verify it.
        """
        stats = self.dexscreener.get_token_stats(mint)
        if stats is None:
            return False, None

        passes = (
            stats["market_cap_usd"] <= Config.MARKETCAP_LIMIT
            and stats["liquidity_usd"] >= Config.MIN_LIQUIDITY
        )
        return passes, stats

    def _build_alert(self, sig, tx):
        token_transfers = tx.get("tokenTransfers") or []
        mints = {t.get("mint") for t in token_transfers if t.get("mint") and t.get("mint") != NATIVE_SOL_MINT}

        if not mints:
            # Plain SOL movement / no SPL token involved — no cap/liquidity to filter on
            return f"🚨 New Tx\n{sig}"

        qualifying = []
        for mint in mints:
            passes, stats = self._passes_filters(mint)
            if passes:
                qualifying.append((mint, stats))

        if not qualifying:
            # Tokens were involved but none met the market cap / liquidity thresholds
            return None

        lines = [f"🚨 New Tx\n{sig}"]
        for mint, stats in qualifying:
            lines.append(
                f"• {stats['symbol']} — MC ${stats['market_cap_usd']:,.0f} "
                f"| Liq ${stats['liquidity_usd']:,.0f}\n  {mint}"
            )
        return "\n".join(lines)

    async def check_wallet(self):
        txs = self.helius.get_transactions(self.wallet)
        seen = self.load_seen()

        for tx in txs[:10]:
            sig = tx.get("signature")
            if not sig or sig in seen:
                continue

            seen.add(sig)

            message = self._build_alert(sig, tx)
            if message:
                await self.telegram.send_message(message)

        self.save_seen(seen)
