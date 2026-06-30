import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
    WATCH_WALLET = os.getenv("WATCH_WALLET")
    MARKETCAP_LIMIT = float(os.getenv("MARKETCAP_LIMIT", 5000))
    MIN_LIQUIDITY = float(os.getenv("MIN_LIQUIDITY", 1000))
    POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 30))

    @classmethod
    def validate(cls):
        required = {
            "TELEGRAM_BOT_TOKEN": cls.TELEGRAM_BOT_TOKEN,
            "TELEGRAM_CHAT_ID": cls.TELEGRAM_CHAT_ID,
            "HELIUS_API_KEY": cls.HELIUS_API_KEY,
            "WATCH_WALLET": cls.WATCH_WALLET,
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise RuntimeError(
                f"Missing required environment variable(s): {', '.join(missing)}. "
                "Set them in your .env file or hosting provider's env settings."
            )
