#!/usr/bin/env python3
"""
LLM Control Plane - LLM控制层
功能：
1. 模型路由
2. 任务调度
3. Fallback
"""
from typing import Dict, List


class LLMControlPlane:
    """LLM控制层"""
    
    # 模型配置
    MODELS = {
        "qwen3.5:9b": {"provider": "ollama", "type": "general"},
        "qwen2.5:14b": {"provider": "ollama", "type": "analysis"},
        "deepseek-coder:6.7b": {"provider": "ollama", "type": "code"},
        "qwen2.5:latest": {"provider": "ollama", "type": "fast"},
        "minimax/MiniMax-M2.5": {"provider": "minimax", "type": "creative"},
        "volcengine/doubao-seed-code": {"provider": "doubao", "type": "general"},
    }
    
    # 任务类型 -> 模型映射
    TASK_MODELS = {
        "code": ["deepseek-coder:6.7b", "qwen2.5:7b", "qwen3.5:9b"],
        "analysis": ["qwen2.5:14b", "qwen3.5:9b"],
        "creative": ["minimax/MiniMax-M2.5", "qwen2.5:14b"],
        "fast": ["qwen2.5:latest", "deepseek-coder:6.7b"],
        "general": ["qwen3.5:9b", "qwen2.5:latest"],
        "research": ["qwen2.5:14b", "qwen3.5:9b"],
    }
    
    def __init__(self):
        self.current_model = "qwen3.5:9b"
        self.stats = {
            "total_requests": 0,
            "successful": 0,
            "failed": 0,
            "fallback_count": 0,
        }
    
    def route(self, task_type: str, prompt: str = None) -> str:
        """
        路由模型
        
        Args:
            task_type: 任务类型
            prompt: 用户输入
        
        Returns:
            选择的模型
        """
        self.stats["total_requests"] += 1
        
        # 获取任务对应的模型列表
        models = self.TASK_MODELS.get(task_type, self.TASK_MODELS["general"])
        
        # 选择第一个
        self.current_model = models[0]
        
        return self.current_model
    
    def fallback(self) -> str:
        """Fallback到下一个模型"""
        self.stats["fallback_count"] += 1
        
        # 获取当前模型在列表中的位置
        for models in self.TASK_MODELS.values():
            if self.current_model in models:
                idx = models.index(self.current_model)
                if idx + 1 < len(models):
                    self.current_model = models[idx + 1]
                    return self.current_model
        
        return self.current_model
    
    def call(self, model: str, prompt: str) -> Dict:
        """
        调用模型
        
        Args:
            model: 模型名
            prompt: 输入
        
        Returns:
            结果
        """
        import requests
        
        # 本地模型
        if model in self.MODELS and self.MODELS[model]["provider"] == "ollama":
            try:
                resp = requests.post(
                    "http://localhost:11434/api/generate",
                    json={"model": model, "prompt": prompt, "stream": False},
                    timeout=60
                )
                
                if resp.status_code == 200:
                    self.stats["successful"] += 1
                    return {
                        "success": True,
                        "response": resp.json().get("response", ""),
                        "model": model,
                    }
            except:
                pass
        
        self.stats["failed"] += 1
        return {"success": False, "error": "Failed", "model": model}
    
    def execute(self, task_type: str, prompt: str) -> Dict:
        """
        执行任务
        
        自动路由 + 调用 + Fallback
        """
        # 路由
        model = self.route(task_type, prompt)
        
        # 调用
        result = self.call(model, prompt)
        
        # 如果失败，尝试Fallback
        if not result["success"]:
            for _ in range(3):  # 最多Fallback 3次
                model = self.fallback()
                result = self.call(model, prompt)
                if result["success"]:
                    break
        
        return result
    
    def get_stats(self) -> Dict:
        return self.stats.copy()
    
    def print_status(self):
        """打印状态"""
        s = self.stats
        print("=== LLM Control Plane ===")
        print(f"当前模型: {self.current_model}")
        print(f"总请求: {s['total_requests']}")
        print(f"成功: {s['successful']}")
        print(f"失败: {s['failed']}")
        print(f"Fallback: {s['fallback_count']}")


# 全局实例
_llm = None

def get_llm_control_plane() -> LLMControlPlane:
    global _llm
    if _llm is None:
        _llm = LLMControlPlane()
    return _llm


# 测试
if __name__ == "__main__":
    llm = get_llm_control_plane()
    
    print("=== LLM Control Plane 测试 ===\n")
    
    # 路由测试
    for task in ["code", "analysis", "fast"]:
        model = llm.route(task)
        print(f"{task}: {model}")
    
    # 调用测试
    print("\n调用测试:")
    result = llm.execute("fast", "Hello")
    print(f"成功: {result['success']}")
    if result['success']:
        print(f"回复: {result['response'][:50]}...")
    
    llm.print_status()
