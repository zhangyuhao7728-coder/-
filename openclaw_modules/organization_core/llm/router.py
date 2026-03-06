"""
LLM Router
LLM 智能路由 - 根据任务复杂度选择合适的 LLM 提供商
"""

from typing import Optional, Dict, Any
from organization_core.llm.base import BaseLLMProvider
from organization_core.llm.registry import get_llm_registry


class LLMRouter:
    """
    LLM 智能路由器
    
    根据任务特征选择合适的 LLM 提供商：
    - 简单任务 → 本地模型 (低成本、低延迟)
    - 复杂任务 → 云端模型 (高能力)
    """
    
    # Token 阈值配置
    LOCAL_THRESHOLD = 1500  # < 1500 tokens 使用本地
    LOCAL_MAX_TOKENS = 8192  # 本地模型最大输出
    
    def __init__(self):
        self.registry = get_llm_registry()
        
        # 路由规则
        self.rules = [
            {"provider": "ollama", "max_tokens": self.LOCAL_THRESHOLD},
            {"provider": "minimax", "max_tokens": float("inf")},
        ]
        
        print("✅ LLMRouter initialized")
    
    def select_provider(self, content: str, force_provider: Optional[str] = None) -> str:
        """
        选择 LLM 提供商
        
        Args:
            content: 输入内容
            force_provider: 强制使用某个提供商
            
        Returns:
            提供商名称
        """
        # 强制指定
        if force_provider:
            if self.registry.get(force_provider):
                return force_provider
            print(f"⚠️ Provider '{force_provider}' not available, using default")
        
        # 估算 token 数量
        provider = self.registry.get_default()
        if not provider:
            raise RuntimeError("No LLM provider available")
        
        estimated_tokens = provider.estimate_tokens(content)
        
        # 根据 token 数量选择
        if estimated_tokens < self.LOCAL_THRESHOLD:
            # 检查本地模型是否可用
            if self.registry.get("ollama") and self.registry.get("ollama").health_check():
                return "ollama"
        
        # 默认使用云端
        return "minimax"
    
    def get_provider(self, name: Optional[str] = None) -> Optional[BaseLLMProvider]:
        """
        获取 LLM 提供商实例
        
        Args:
            name: 提供商名称 (默认自动选择)
            
        Returns:
            提供商实例
        """
        if name:
            return self.registry.get(name)
        
        # 自动选择
        default = self.registry.get_default()
        return default
    
    def estimate_cost(self, provider_name: str, tokens: int) -> float:
        """
        估算成本
        
        Args:
            provider_name: 提供商名称
            tokens: token 数量
            
        Returns:
            估算成本 (美元)
        """
        # MiniMax M2.5 价格 (约)
        pricing = {
            "minimax": 0.000,  # 暂免费或待确认
            "ollama": 0.0,  # 本地免费
        }
        
        return pricing.get(provider_name, 0) * tokens
    
    def get_stats(self) -> Dict[str, Any]:
        """
        获取路由统计
        
        Returns:
            统计信息
        """
        providers = self.registry.list_providers()
        
        return {
            "providers": providers,
            "local_threshold": self.LOCAL_THRESHOLD,
            "default_provider": self.registry._default_provider
        }


# 全局路由器
_router = None


def get_llm_router() -> LLMRouter:
    """获取 LLM 路由器实例"""
    global _router
    if _router is None:
        _router = LLMRouter()
    return _router
