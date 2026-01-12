"""
新架构API测试脚本
用于验证新实现的API端点
"""
import asyncio
import httpx
from typing import Dict


BASE_URL = "http://localhost:8000"
AUTH = ("admin", "admin123")  # 默认认证


async def test_health_check():
    """测试健康检查端点"""
    print("\n=== 测试健康检查 ===")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        assert response.status_code == 200
        print("✅ 健康检查通过")


async def test_get_tasks():
    """测试获取任务列表"""
    print("\n=== 测试获取任务列表 ===")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/api/tasks",
            auth=AUTH
        )
        print(f"状态码: {response.status_code}")
        tasks = response.json()
        print(f"任务数量: {len(tasks)}")
        if tasks:
            print(f"第一个任务: {tasks[0].get('task_name')}")
        assert response.status_code == 200
        print("✅ 获取任务列表成功")
        return tasks


async def test_get_logs():
    """测试获取日志"""
    print("\n=== 测试获取日志 ===")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/api/logs",
            auth=AUTH
        )
        print(f"状态码: {response.status_code}")
        data = response.json()
        print(f"日志长度: {len(data.get('new_content', ''))}")
        assert response.status_code == 200
        print("✅ 获取日志成功")


async def test_get_prompts():
    """测试获取Prompt列表"""
    print("\n=== 测试获取Prompt列表 ===")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/api/prompts",
            auth=AUTH
        )
        print(f"状态码: {response.status_code}")
        prompts = response.json()
        print(f"Prompt文件数量: {len(prompts)}")
        assert response.status_code == 200
        print("✅ 获取Prompt列表成功")


async def main():
    """运行所有测试"""
    print("=" * 50)
    print("开始测试新架构API")
    print("=" * 50)

    try:
        await test_health_check()
        await test_get_tasks()
        await test_get_logs()
        await test_get_prompts()

        print("\n" + "=" * 50)
        print("✅ 所有测试通过！")
        print("=" * 50)
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
