#!/usr/bin/env python3
"""
LLM路由器 - 统一调用AI模型
"""
import os

# 支持的模型
MODELS = {
    'minimax': 'MiniMax-M2.5',
    'ollama': 'qwen2.5:7b',
    'default': 'MiniMax-M2.5',
}

def get_client(model: str = 'default'):
    """获取AI客户端"""
    # 简化实现
    return None

async def chat(prompt: str, model: str = 'default') -> str:
    """调用AI"""
    # 这里可以集成实际的AI调用
    return "AI生成的内容..."

def use_model(model_name: str):
    """切换模型"""
    if model_name in MODELS:
        os.environ['DEFAULT_MODEL'] = model_name
        return True
    return False
