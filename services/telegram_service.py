import asyncio
import requests
from config import Config
from utils.logger import get_logger

logger = get_logger(__name__)

class TelegramService:
    def __init__(self):
        self.token = Config.TELEGRAM_BOT_TOKEN
        self.chat_id = Config.TELEGRAM_CHAT_ID
        self.base = f'https://api.telegram.org/bot{self.token}'

    def _post(self, text):
        resp = requests.post(
            self.base + '/sendMessage',
            json={'chat_id': self.chat_id, 'text': text},
            timeout=10,
        )
        if resp.status_code != 200:
            logger.error(f"Telegram API error {resp.status_code}: {resp.text}")
        return resp

    async def send_message(self, text):
        try:
            # requests is blocking; run it off the event loop so polling isn't stalled
            await asyncio.to_thread(self._post, text)
        except requests.RequestException as e:
            logger.error(f"Failed to send Telegram message: {e}")
