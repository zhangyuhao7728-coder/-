#!/usr/bin/env python3
"""
Smart Router - 智能路由器
功能：
1. 任务自动分类
2. 成本优化策略
3. 质量保证
"""
from typing import Dict, Optional


class SmartRouter:
    """智能路由器"""
    
    # 成本优先级 (从低到高)
    COST_PRIORITY = {
        "ollama": 0,      # 免费
        "doubao": 1,      # 40%配额
        "minimax": 2,     # 付费
    }
    
    def __init__(self):
        self.stats = {
            "total": 0,
            "free_used": 0,
            "paid_used": 0,
            "fallback_count": 0,
        }
    
    # ========== 任务分类 ==========
    
    KEYWORDS = {
        "code": ["python", "代码", "编程", "function", "def ", "class ", "算法"],
        "analysis": ["分析", "比较", "解释", "为什么", "区别"],
        "creative": ["创作", "写诗", "故事", "小说", "创意"],
        "fast": ["简单", "快速", "一句话", "是什么", "介绍"],
    }
    
    def classify(self, prompt: str) -> str:
        """自动分类"""
        prompt_lower = prompt.lower()
        
        for task_type, keywords in self.KEYWORDS.items():
            if any(kw in prompt_lower for kw in keywords):
                return task_type
        
        return "general"
    
    # ========== 成本优化策略 ==========
    
    def get_model_priority(self, task_type: str) -> list:
        """
        获取模型优先级
        
        策略: 优先免费 → 配额 → 付费
        """
        # 任务到模型的映射
        task_models = {
            "code": [
                ("ollama", "deepseek-coder:6.7b"),
                ("ollama", "qwen2.5:7b"),
                ("doubao", "volcengine/doubao-seed-code"),
            ],
            "analysis": [
                ("ollama", "qwen2.5:14b"),
                ("ollama", "qwen3.5:9b"),
                ("minimax", "MiniMax-M2.5"),
            ],
            "creative": [
                ("minimax", "MiniMax-M2.5"),
                ("ollama", "qwen2.5:14b"),
            ],
            "fast": [
                ("ollama", "qwen2.5:latest"),
                ("ollama", "qwen2.5:7b"),
            ],
            "general": [
                ("ollama", "qwen2.5:latest"),
                ("doubao", "volcengine/doubao-seed-code"),
                ("minimax", "MiniMax-M2.5"),
            ],
        }
        
        return task_models.get(task_type, task_models["general"])
    
    # ========== 路由 ==========
    
    def route(self, prompt: str, task_type: str = None) -> Dict:
        """
        智能路由
        
        策略:
        1. 优先使用免费模型
        2. 如果响应质量不足
        3. 自动升级到付费模型
        """
        self.stats["total"] += 1
        
        # 自动分类
        if task_type is None:
            task_type = self.classify(prompt)
        
        print(f"  任务类型: {task_type}")
        
        # 获取优先级模型列表
        models = self.get_model_priority(task_type)
        
        # 依次尝试
        for provider, model in models:
            print(f"  → 尝试: {model} ({provider})")
            
            result = self._try_model(provider, model, prompt)
            
            if result["success"]:
                # 检查是否需要升级
                if provider == "ollama" and self._needs_upgrade(result["response"], task_type):
                    print(f"  ⏭️ 免费模型质量不足，尝试升级...")
                    self.stats["fallback_count"] += 1
                    continue
                
                # 成功
                if provider == "ollama":
                    self.stats["free_used"] += 1
                else:
                    self.stats["paid_used"] += 1
                
                return result
        
        return {"success": False, "error": "All models failed"}
    
    def _needs_upgrade(self, response: str, task_type: str) -> bool:
        """
        判断是否需要升级模型
        
        免费模型可能质量不足时自动升级
        """
        # 简单启发式规则
        
        if task_type == "creative":
            # 创意任务质量不足
            if len(response) < 100:
                return True
        
        if task_type == "analysis":
            # 分析任务太简单
            if len(response) < 200:
                return True
        
        # 默认不升级
        return False
    
    def _try_model(self, provider: str, model: str, prompt: str) -> Dict:
        """尝试调用模型"""
        try:
            if provider == "ollama":
                return self._ollama(model, prompt)
            elif provider == "minimax":
                return self._minimax(model, prompt)
            elif provider == "doubao":
                return self._doubao(model, prompt)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _ollama(self, model: str, prompt: str) -> Dict:
        """Ollama 调用"""
        import requests
        
        try:
            resp = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=60
            )
            
            if resp.status_code == 200:
                return {
                    "success": True,
                    "response": resp.json().get("response", ""),
                    "model": model,
                    "provider": "ollama",
                    "cost": "free",
                }
        except:
            pass
        
        return {"success": False, "error": "Ollama failed"}
    
    def _minimax(self, model: str, prompt: str) -> Dict:
        """MiniMax 调用"""
        import os
        import requests
        
        api_key = os.environ.get("MINIMAX_API_KEY", "")
        if not api_key:
            return {"success": False, "error": "No API key"}
        
        try:
            resp = requests.post(
                "https://api.minimax.chat/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"model": model, "messages": [{"role": "user", "content": prompt}]},
                timeout=60
            )
            
            if resp.status_code == 200:
                return {
                    "success": True,
                    "response": resp.json()["choices"][0]["message"]["content"],
                    "model": model,
                    "provider": "minimax",
                    "cost": "paid",
                }
            elif resp.status_code == 429:
                return {"success": False, "error": "QUOTA_EXCEEDED", "quota": True}
        except:
            pass
        
        return {"success": False, "error": "MiniMax failed"}
    
    def _doubao(self, model: str, prompt: str) -> Dict:
        """Doubao 调用"""
        import os
        import requests
        
        api_key = os.environ.get("VOLCENGINE_API_KEY", "")
        if not api_key:
            return {"success": False, "error": "No API key"}
        
        try:
            resp = requests.post(
                "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"model": model, "messages": [{"role": "user", "content": prompt}]},
                timeout=60
            )
            
            if resp.status_code == 200:
                return {
                    "success": True,
                    "response": resp.json()["choices"][0]["message"]["content"],
                    "model": model,
                    "provider": "doubao",
                    "cost": "quota",
                }
        except:
            pass
        
        return {"success": False, "error": "Doubao failed"}
    
    def get_stats(self) -> Dict:
        return self.stats.copy()


# 全局实例
_router = None

def get_smart_router() -> SmartRouter:
    global _router
    if _router is None:
        _router = SmartRouter()
    return _router


def smart_route(prompt: str, task_type: str = None) -> Dict:
    """智能路由"""
    return get_smart_router().route(prompt, task_type)


# 测试
if __name__ == "__main__":
    router = get_smart_router()
    
    print("=== Smart Router 测试 ===\n")
    
    tests = [
        ("写一个Python函数", "code"),
        ("写一首诗", "creative"),
        ("什么是AI", "fast"),
    ]
    
    for prompt, expected in tests:
        print(f"输入: {prompt}")
        result = router.route(prompt)
        
        print(f"  成功: {result['success']}")
        if result["success"]:
            print(f"  模型: {result['model']}")
            print(f"  成本: {result.get('cost', 'N/A')}")
            print(f"  回复: {result['response'][:60]}...")
        print()
    
    print(f"统计: {router.get_stats()}")
