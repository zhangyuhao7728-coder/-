"""
OpenClaw Bridge (Final Version)
桥接 OpenClaw 与 Organization Core - 支持异步任务提交
"""

import requests
import asyncio
from typing import Dict, Any, Optional
import os

# Organization Core API 地址
ORGANIZATION_API = os.environ.get("ORGANIZATION_API", "http://127.0.0.1:8000")


class OpenClawBridge:
    """OpenClaw 到 Organization Core 的桥接器"""
    
    def __init__(self, api_url: str = ORGANIZATION_API):
        self.api_url = api_url
        self.sync_endpoint = f"{api_url}/message/sync"
        self.async_endpoint = f"{api_url}/message"
        self.route_endpoint = f"{api_url}/route"
        self.health_endpoint = f"{api_url}/health"
        self.stats_endpoint = f"{api_url}/stats"
    
    def forward(self, content: str, sender: Optional[str] = None, channel: Optional[str] = None) -> Dict[str, Any]:
        """
        转发消息到 Organization Core (异步 - 推荐)
        不等待结果，立即返回
        
        Args:
            content: 消息内容
            sender: 发送者
            channel: 渠道
            
        Returns:
            API 响应
        """
        payload = {
            "content": content,
        }
        
        if sender:
            payload["sender"] = sender
        if channel:
            payload["channel"] = channel
        
        try:
            response = requests.post(self.async_endpoint, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status": "failed"}
    
    def forward_sync(self, content: str, sender: Optional[str] = None, channel: Optional[str] = None) -> Dict[str, Any]:
        """
        转发消息到 Organization Core (同步)
        等待 Agent 执行完成
        
        Args:
            content: 消息内容
            sender: 发送者
            channel: 渠道
            
        Returns:
            Agent 执行结果
        """
        payload = {
            "content": content,
        }
        
        if sender:
            payload["sender"] = sender
        if channel:
            payload["channel"] = channel
        
        try:
            response = requests.post(self.sync_endpoint, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status": "failed"}
    
    def submit_task(self, content: str, sender: Optional[str] = None, channel: Optional[str] = None, wait: bool = False) -> Dict[str, Any]:
        """
        提交任务到 Organization Core
        
        Args:
            content: 消息内容
            sender: 发送者
            channel: 渠道
            wait: 是否等待结果 (True=同步, False=异步)
            
        Returns:
            任务结果
        """
        if wait:
            return self.forward_sync(content, sender, channel)
        return self.forward(content, sender, channel)
    
    def route(self, content: str, sender: Optional[str] = None, channel: Optional[str] = None) -> Dict[str, Any]:
        """
        路由消息 (通过任务队列)
        
        Args:
            content: 消息内容
            sender: 发送者
            channel: 渠道
            
        Returns:
            任务信息
        """
        payload = {
            "content": content,
        }
        
        if sender:
            payload["sender"] = sender
        if channel:
            payload["channel"] = channel
        
        try:
            response = requests.post(self.route_endpoint, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status": "failed"}
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        try:
            response = requests.get(f"{self.stats_endpoint}", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_tasks(self, status: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """获取任务列表"""
        try:
            url = f"{self.api_url}/tasks"
            params = {"limit": limit}
            if status:
                params["status"] = status
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_task(self, task_id: int) -> Dict[str, Any]:
        """获取单个任务"""
        try:
            response = requests.get(f"{self.api_url}/tasks/{task_id}", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def health_check(self) -> bool:
        """健康检查"""
        try:
            response = requests.get(f"{self.health_endpoint}", timeout=5)
            return response.status_code == 200
        except:
            return False


# ========== Telegram Handler ==========

class TelegramHandler:
    """Telegram 消息处理器"""
    
    def __init__(self, bridge: OpenClawBridge = None):
        self.bridge = bridge or OpenClawBridge()
    
    def handle_message(self, message: str, user_id: str = None, wait: bool = False) -> str:
        """
        处理 Telegram 消息
        
        Args:
            message: 用户消息
            user_id: 用户 ID
            wait: 是否等待结果
            
        Returns:
            回复文本
        """
        # 提交任务
        result = self.bridge.submit_task(
            content=message,
            sender=str(user_id) if user_id else "telegram",
            channel="telegram",
            wait=wait
        )
        
        if "error" in result:
            return f"❌ 错误: {result['error']}"
        
        if wait:
            # 同步模式 - 返回结果
            data = result.get("data", {})
            if isinstance(data, dict):
                return data.get("message", str(result))
            return str(result)
        else:
            # 异步模式 - 返回确认
            return f"✅ 任务已提交: {result.get('agent', 'unknown')} Agent 处理中..."
    
    def handle_photo(self, photo_url: str, caption: str = None, user_id: str = None) -> str:
        """处理图片消息"""
        message = f"[图片] {caption or '收到图片'}"
        return self.handle_message(message, user_id)
    
    def handle_command(self, command: str, args: str = None, user_id: str = None) -> str:
        """处理命令"""
        if command == "/stats":
            stats = self.bridge.get_stats()
            return f"📊 统计:\n{stats}"
        elif command == "/tasks":
            tasks = self.bridge.get_tasks(limit=5)
            return f"📋 任务: {tasks}"
        elif command == "/help":
            return """🤖 可用命令:
/stats - 查看统计
/tasks - 查看任务
直接发送消息 - 交给 AI 处理"""
        else:
            return f"未知命令: {command}"


# 全局实例
bridge = OpenClawBridge()
telegram_handler = TelegramHandler(bridge)


# ========== 便捷函数 ==========

def forward_to_org(content: str, sync: bool = False) -> Dict[str, Any]:
    """
    转发消息到 Organization Core
    
    Args:
        content: 消息内容
        sync: 是否同步执行
        
    Returns:
        执行结果
    """
    if sync:
        return bridge.forward_sync(content)
    return bridge.forward(content)


def submit_task(content: str, wait: bool = False) -> Dict[str, Any]:
    """提交任务"""
    return bridge.submit_task(content, wait=wait)


# ========== 测试 ==========

if __name__ == "__main__":
    print("=" * 60)
    print("🔄 OpenClaw Bridge 测试")
    print("=" * 60)
    
    # 健康检查
    print("\n1. 健康检查...")
    health = bridge.health_check()
    print(f"   Health: {'✅' if health else '❌'}")
    
    # 测试异步
    print("\n2. 异步提交...")
    result = bridge.forward("测试异步消息", sender="test")
    print(f"   Result: {result.get('status', 'error')}")
    
    # 测试同步
    print("\n3. 同步提交...")
    result = bridge.forward_sync("测试同步消息", sender="test")
    print(f"   Result: {result.get('status', 'error')}")
    
    # 统计
    print("\n4. 统计...")
    stats = bridge.get_stats()
    print(f"   Total: {stats.get('total', 0)}")
    
    print("\n" + "=" * 60)
    print("✅ OpenClaw Bridge 测试完成!")
    print("=" * 60)
