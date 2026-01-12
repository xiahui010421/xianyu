"""
Ntfy 通知客户端
"""
import asyncio
import requests
from typing import Dict
from .base import NotificationClient


class NtfyClient(NotificationClient):
    """Ntfy 通知客户端"""

    def __init__(self, topic_url: str = None):
        super().__init__(enabled=bool(topic_url))
        self.topic_url = topic_url

    async def send(self, product_data: Dict, reason: str) -> bool:
        """发送 Ntfy 通知"""
        if not self.is_enabled():
            return False

        try:
            msg_data = self._format_message(product_data, reason)
            message = f"价格: {msg_data['price']}\n原因: {msg_data['reason']}\n链接: {msg_data['link']}"
            title = f"🚨 新推荐! {msg_data['title'][:30]}..."

            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                lambda: requests.post(
                    self.topic_url,
                    data=message.encode('utf-8'),
                    headers={
                        "Title": title.encode('utf-8'),
                        "Priority": "urgent",
                        "Tags": "bell,vibration"
                    },
                    timeout=10
                )
            )
            return True
        except Exception as e:
            print(f"Ntfy 通知发送失败: {e}")
            return False
