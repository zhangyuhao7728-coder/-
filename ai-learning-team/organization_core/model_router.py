"""
Model Router
根据任务和 Agent 自动选择最佳模型
"""

from typing import Optional


class ModelRouter:
    """模型路由器 - 智能选择模型"""
    
    # 模型配置
    MODELS = {
        "general": "qwen2.5:14b",      # 通用任务
        "coding": "deepseek-coder:6.7b",  # 代码任务
        "reasoning": "MiniMax-M2.5",     # 复杂推理
    }
    
    def __init__(self):
        self.default_model = self.MODELS["general"]
        self.coding_model = self.MODELS["coding"]
        self.reasoning_model = self.MODELS["reasoning"]
    
    def select_model(self, agent: str, message: str) -> str:
        """
        根据 Agent 和消息内容选择模型
        
        Args:
            agent: Agent 名称
            message: 消息内容
            
        Returns:
            模型名称
        """
        msg = message.lower()
        
        # 1. Engineer / 代码任务 → 使用代码模型
        if agent == "engineer":
            return self.coding_model
        
        # 2. 代码关键词检测
        if any(kw in msg for kw in ["代码", "python", "写程序", "编程", "script", "code", "function", "class "]):
            return self.coding_model
        
        # 3. 长文本 (>1500字符) → 使用云端模型
        if len(message) > 1500:
            return self.reasoning_model
        
        # 4. CEO / 复杂推理任务
        if agent == "ceo":
            # 长对话用云端
            if len(message) > 500:
                return self.reasoning_model
        
        # 5. 默认使用通用模型
        return self.default_model
    
    def get_model_info(self, model: str) -> dict:
        """获取模型信息"""
        model_info = {
            "qwen2.5:14b": {
                "name": "Qwen2.5 14B",
                "provider": "ollama",
                "type": "general",
                "context": "32K"
            },
            "deepseek-coder:6.7b": {
                "name": "DeepSeek Coder 6.7B", 
                "provider": "ollama",
                "type": "coding",
                "context": "16K"
            },
            "MiniMax-M2.5": {
                "name": "MiniMax M2.5",
                "provider": "cloud",
                "type": "reasoning",
                "context": "200K"
            }
        }
        return model_info.get(model, {"name": model, "provider": "unknown"})


# 全局实例
_model_router = None


def get_model_router() -> ModelRouter:
    """获取模型路由器实例"""
    global _model_router
    if _model_router is None:
        _model_router = ModelRouter()
    return _model_router
