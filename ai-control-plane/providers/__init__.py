#!/usr/bin/env python3
"""
Provider Factory - Provider 工厂
统一入口
"""
from typing import Dict
from .ollama_provider import get_ollama
from .minimax_provider import get_minimax


class ProviderFactory:
    """Provider 工厂"""
    
    def __init__(self):
        self.providers = {
            "ollama": get_ollama(),
            "minimax": get_minimax(),
        }
    
    def get(self, provider_name: str):
        """获取Provider"""
        return self.providers.get(provider_name)
    
    def generate(self, model: str, prompt: str) -> Dict:
        """
        统一生成接口
        
        根据模型名称自动选择Provider
        
        Args:
            model: 模型名称 (包含provider信息，如 ollama/qwen2.5)
            prompt: 用户输入
        
        Returns:
            {"success": True/False, "response": "...", "error": "..."}
        """
        # 解析provider
        if "/" in model:
            provider_name, model_name = model.split("/", 1)
        elif model.startswith("qwen") or model.startswith("deepseek"):
            provider_name = "ollama"
            model_name = model
        else:
            provider_name = "minimax"
            model_name = model
        
        # 获取provider
        provider = self.get(provider_name)
        if not provider:
            return {
                "success": False,
                "error": f"Unknown provider: {provider_name}",
            }
        
        # 检查可用性
        if not provider.is_available():
            return {
                "success": False,
                "error": f"Provider {provider_name} not available",
                "provider": provider_name,
            }
        
        # 生成
        return provider.generate(model_name, prompt)


# 全局实例
_factory = None

def get_factory() -> ProviderFactory:
    global _factory
    if _factory is None:
        _factory = ProviderFactory()
    return _factory


def generate(model: str, prompt: str) -> Dict:
    """统一生成接口"""
    return get_factory().generate(model, prompt)


# 测试
if __name__ == "__main__":
    factory = get_factory()
    
    print("=== Provider Factory 测试 ===\n")
    
    # 测试 Ollama
    print("【Ollama】")
    result = factory.generate("qwen2.5:latest", "你好")
    print(f"成功: {result['success']}")
    if result["success"]:
        print(f"回复: {result['response'][:50]}...")
    
    # 测试 MiniMax
    print("\n【MiniMax】")
    result = factory.generate("MiniMax-M2.5", "你好")
    print(f"成功: {result['success']}")
    print(f"错误: {result.get('error', 'N/A')}")
