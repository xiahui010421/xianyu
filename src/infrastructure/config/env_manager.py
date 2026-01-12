"""
环境变量管理器
负责读取和更新 .env 文件
"""
import os
from typing import Dict, List, Optional
from pathlib import Path


class EnvManager:
    """环境变量管理器"""

    def __init__(self, env_file: str = ".env"):
        self.env_file = Path(env_file)
        self._ensure_env_file_exists()

    def _ensure_env_file_exists(self):
        """确保 .env 文件存在"""
        if not self.env_file.exists():
            self.env_file.touch()

    def read_env(self) -> Dict[str, str]:
        """读取所有环境变量"""
        env_vars = {}
        if not self.env_file.exists():
            return env_vars

        with open(self.env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释
                if not line or line.startswith('#'):
                    continue

                # 解析键值对
                if '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()

        return env_vars

    def get_value(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """获取单个环境变量的值"""
        env_vars = self.read_env()
        return env_vars.get(key, default)

    def update_values(self, updates: Dict[str, str]) -> bool:
        """批量更新环境变量"""
        try:
            # 读取现有配置
            existing_vars = self.read_env()

            # 更新值
            existing_vars.update(updates)

            # 写回文件
            return self._write_env(existing_vars)
        except Exception as e:
            print(f"更新环境变量失败: {e}")
            return False

    def set_value(self, key: str, value: str) -> bool:
        """设置单个环境变量"""
        return self.update_values({key: value})

    def delete_keys(self, keys: List[str]) -> bool:
        """删除指定的环境变量"""
        try:
            existing_vars = self.read_env()
            for key in keys:
                existing_vars.pop(key, None)
            return self._write_env(existing_vars)
        except Exception as e:
            print(f"删除环境变量失败: {e}")
            return False

    def _write_env(self, env_vars: Dict[str, str]) -> bool:
        """写入环境变量到文件"""
        try:
            with open(self.env_file, 'w', encoding='utf-8') as f:
                for key, value in env_vars.items():
                    f.write(f"{key}={value}\n")
            return True
        except Exception as e:
            print(f"写入 .env 文件失败: {e}")
            return False


# 全局实例
env_manager = EnvManager()
