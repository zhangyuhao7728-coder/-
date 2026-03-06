"""
Base Agent
所有 Agent 的基类
"""

from typing import Dict, Any, Optional


class BaseAgent:
    """Agent 基类"""
    
    def __init__(self, name: str, model_router=None, agent_bus=None):
        self.name = name
        self.model_router = model_router
        self.agent_bus = agent_bus
        
        # 注册到 Agent Bus
        if self.agent_bus:
            self.agent_bus.register(name)
    
    def send(self, to: str, message: Any) -> None:
        """发送消息给其他 Agent"""
        if self.agent_bus:
            self.agent_bus.send(self.name, to, message)
    
    def receive(self) -> Optional[Dict]:
        """接收消息"""
        if self.agent_bus:
            return self.agent_bus.receive(self.name)
        return None
    
    def peek(self) -> Optional[Dict]:
        """查看消息（不取出）"""
        if self.agent_bus:
            return self.agent_bus.peek(self.name)
        return None
    
    def broadcast(self, message: Any, recipients: list) -> None:
        """广播消息"""
        if self.agent_bus:
            self.agent_bus.broadcast(self.name, message, recipients)
    
    def handle(self, task: Dict) -> Dict:
        """
        处理任务（子类实现）
        
        Args:
            task: 任务对象
            
        Returns:
            处理结果
        """
        raise NotImplementedError("Subclass must implement handle()")
    
    def select_model(self, task: Dict) -> str:
        """
        选择模型
        
        Args:
            task: 任务对象
            
        Returns:
            模型名称
        """
        if self.model_router:
            return self.model_router.route(self.name, task)
        
        # 默认模型
        return "ollama/qwen2.5:14b"
