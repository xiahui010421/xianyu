"""
通知服务
统一管理所有通知渠道
"""
import asyncio
from typing import Dict, List
from src.infrastructure.external.notification_clients.base import NotificationClient


class NotificationService:
    """通知服务"""

    def __init__(self, clients: List[NotificationClient]):
        self.clients = [client for client in clients if client.is_enabled()]

    async def send_notification(self, product_data: Dict, reason: str) -> Dict[str, bool]:
        """
        发送通知到所有启用的渠道

        Args:
            product_data: 商品数据
            reason: 推荐原因

        Returns:
            各渠道发送结果
        """
        if not self.clients:
            print("警告：未配置任何通知服务")
            return {}

        # 并发发送到所有渠道
        tasks = [client.send(product_data, reason) for client in self.clients]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 统计结果
        result_dict = {}
        for i, result in enumerate(results):
            client_name = self.clients[i].__class__.__name__
            result_dict[client_name] = result if not isinstance(result, Exception) else False

        return result_dict
