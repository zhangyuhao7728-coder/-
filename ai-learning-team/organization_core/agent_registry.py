"""
Agent Registry
负责管理系统内所有 Agent Worker
"""

from typing import Callable, Dict, Optional


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: Dict[str, Callable] = {}

    def register(self, name: str, handler: Callable) -> None:
        """注册 Agent"""
        self._agents[name] = handler
        print(f"✅ Agent '{name}' 已注册")

    def get(self, name: str) -> Callable:
        """获取 Agent"""
        if name not in self._agents:
            raise ValueError(f"Agent '{name}' 未注册")
        return self._agents[name]

    def unregister(self, name: str) -> None:
        """注销 Agent"""
        if name in self._agents:
            del self._agents[name]

    def list_agents(self) -> list:
        """列出所有已注册 Agent"""
        return list(self._agents.keys())

    def has(self, name: str) -> bool:
        """检查 Agent 是否存在"""
        return name in self._agents
