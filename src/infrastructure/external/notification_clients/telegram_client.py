"""
Telegram 通知客户端
"""
import asyncio
import requests
from typing import Dict
from .base import NotificationClient


class TelegramClient(NotificationClient):
    """Telegram 通知客户端"""

    def __init__(self, bot_token: str = None, chat_id: str = None):
        super().__init__(enabled=bool(bot_token and chat_id))
        self.bot_token = bot_token
        self.chat_id = chat_id

    async def send(self, product_data: Dict, reason: str) -> bool:
        """发送 Telegram 通知"""
        if not self.is_enabled():
            return False

        try:
            msg_data = self._format_message(product_data, reason)

            telegram_message = f"🚨 <b>新推荐!</b>\n\n"
            telegram_message += f"<b>{msg_data['title'][:50]}...</b>\n\n"
            telegram_message += f"💰 价格: {msg_data['price']}\n"
            telegram_message += f"📝 原因: {msg_data['reason']}\n"
            telegram_message += f"💻 <a href='{msg_data['link']}'>查看商品</a>"

            telegram_api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

            telegram_payload = {
                "chat_id": self.chat_id,
                "text": telegram_message,
                "parse_mode": "HTML",
                "disable_web_page_preview": False
            }

            headers = {"Content-Type": "application/json"}
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None,
                lambda: requests.post(
                    telegram_api_url,
                    json=telegram_payload,
                    headers=headers,
                    timeout=10
                )
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Telegram 通知发送失败: {e}")
            return False
