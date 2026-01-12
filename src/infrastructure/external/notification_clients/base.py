"""
通知客户端基类
定义通知客户端的统一接口
"""
from abc import ABC, abstractmethod
from typing import Dict


class NotificationClient(ABC):
    """通知客户端抽象基类"""

    def __init__(self, enabled: bool = False):
        self._enabled = enabled

    def is_enabled(self) -> bool:
        """检查客户端是否启用"""
        return self._enabled

    @abstractmethod
    async def send(self, product_data: Dict, reason: str) -> bool:
        """
        发送通知

        Args:
            product_data: 商品数据
            reason: 推荐原因

        Returns:
            是否发送成功
        """
        pass

    def _format_message(self, product_data: Dict, reason: str) -> Dict[str, str]:
        """格式化消息内容"""
        title = product_data.get('商品标题', 'N/A')
        price = product_data.get('当前售价', 'N/A')
        link = product_data.get('商品链接', '#')

        return {
            'title': title,
            'price': price,
            'link': link,
            'reason': reason
        }
