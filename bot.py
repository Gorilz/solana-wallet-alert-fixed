import asyncio
from services.wallet_monitor import WalletMonitor
from services.telegram_service import TelegramService
from config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

async def main():
    Config.validate()
    logger.info("Starting Solana Wallet Alert Bot...")

    telegram = TelegramService()
    monitor = WalletMonitor(telegram)

    await telegram.send_message("🤖 Solana Wallet Alert Bot is now live!")

    while True:
        try:
            await monitor.check_wallet()
            await asyncio.sleep(Config.POLL_INTERVAL)
        except Exception as e:
            logger.error(f"Main loop error: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
