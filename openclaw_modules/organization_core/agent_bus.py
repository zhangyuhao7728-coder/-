"""
Agent Bus
Agent 通信系统 - 负责 Agent 之间的消息传递
 Dict, List,"""

from typing import Optional, Any
from collections import defaultdict
import threading


class AgentBus:
    """Agent 消息总线"""
    
    def __init__(self):
        self.mailboxes = defaultdict(list)  # {agent: [messages]}
        self.lock = threading.Lock()
    
    def register(self, agent: str) -> None:
        """注册 Agent"""
        with self.lock:
            if agent not in self.mailboxes:
                self.mailboxes[agent] = []
                print(f"✅ Agent '{agent}' registered to AgentBus")
    
    def send(self, sender: str, receiver: str, message: Any) -> None:
        """发送消息"""
        msg = {
            "from": sender,
            "to": receiver,
            "message": message,
            "timestamp": None
        }
        
        with self.lock:
            self.mailboxes[receiver].append(msg)
        
        print(f"📨 {sender} → {receiver}: {message}")
    
    def receive(self, agent: str) -> Optional[Dict]:
        """接收消息"""
        with self.lock:
            if not self.mailboxes[agent]:
                return None
            return self.mailboxes[agent].pop(0)
    
    def peek(self, agent: str) -> Optional[Dict]:
        """查看消息（不取出）"""
        with self.lock:
            if not self.mailboxes[agent]:
                return None
            return self.mailboxes[agent][0]
    
    def has_messages(self, agent: str) -> bool:
        """检查是否有未读消息"""
        with self.lock:
            return len(self.mailboxes[agent]) > 0
    
    def get_queue_size(self, agent: str) -> int:
        """获取队列大小"""
        with self.lock:
            return len(self.mailboxes[agent])
    
    def broadcast(self, sender: str, message: Any, recipients: List[str]) -> None:
        """广播消息"""
        for recipient in recipients:
            if recipient != sender:
                self.send(sender, recipient, message)
    
    def clear(self, agent: str = None) -> None:
        """清空消息队列"""
        with self.lock:
            if agent:
                self.mailboxes[agent] = []
            else:
                self.mailboxes.clear()


# 全局实例
_agent_bus = None


def get_agent_bus() -> AgentBus:
    """获取 AgentBus 实例"""
    global _agent_bus
    if _agent_bus is None:
        _agent_bus = AgentBus()
    return _agent_bus
