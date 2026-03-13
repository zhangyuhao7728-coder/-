#!/usr/bin/env python3
"""
Task Classifier - 任务自动分类器
根据prompt自动识别任务类型
"""
from typing import Dict, List


class TaskClassifier:
    """任务分类器"""
    
    # 关键词映射
    KEYWORDS = {
        "code": [
            "python", "代码", "写程序", "编程", "function", "class ", "def ",
            "算法", "实现", "程序", "coding", "script", "函数", "方法"
        ],
        "analysis": [
            "分析", "比较", "解释", "为什么", "原因", "评估", "总结",
            "区别", "优势", "劣势", "推荐", "建议", "分析", "review"
        ],
        "creative": [
            "创作", "写诗", "故事", "小说", "创意", "写作", "编故事",
            "写一", " poem", "story", "创意", "想象"
        ],
        "fast": [
            "简单", "快速", "一句话", "是什么", "介绍",
            "什么是", "哪个", "how to", "what is"
        ],
    }
    
    def __init__(self):
        self.stats = {"classifications": {}}
    
    def classify(self, prompt: str) -> str:
        """
        自动分类任务
        
        Args:
            prompt: 用户输入
        
        Returns:
            任务类型: code/analysis/creative/fast/general
        """
        prompt_lower = prompt.lower()
        
        # 优先级匹配
        for task_type, keywords in self.KEYWORDS.items():
            if any(kw in prompt_lower for kw in keywords):
                self._record(task_type)
                return task_type
        
        # 默认
        self._record("general")
        return "general"
    
    def _record(self, task_type: str):
        """记录统计"""
        self.stats["classifications"][task_type] = \
            self.stats["classifications"].get(task_type, 0) + 1
    
    def get_stats(self) -> Dict:
        return self.stats.copy()


# 全局实例
_classifier = None

def get_classifier() -> TaskClassifier:
    global _classifier
    if _classifier is None:
        _classifier = TaskClassifier()
    return _classifier


def classify_task(prompt: str) -> str:
    """自动分类任务"""
    return get_classifier().classify(prompt)


# ========== 完整 Router ==========

def route(prompt: str = None, task_type: str = None) -> dict:
    """
    智能路由
    
    自动:
    1. 任务分类
    2. 模型选择
    3. Fallback
    
    Args:
        prompt: 用户输入 (自动分类)
        task_type: 指定任务类型 (可选)
    
    Returns:
        {"success": True/False, "response": "...", "model": "..."}
    """
    from model_registry import MODEL_REGISTRY
    from fallback_manager import get_fallback_manager
    from quota_manager import should_use_model
    from providers import get_ollama
    
    # 1. 任务分类
    if task_type is None and prompt:
        task_type = classify_task(prompt)
    
    task_type = task_type or "general"
    
    # 2. 获取模型列表
    models = MODEL_REGISTRY.get(task_type, MODEL_REGISTRY["general"])
    
    # 3. 依次尝试
    fallback_mgr = get_fallback_manager()
    fallback_count = 0
    
    for model_info in models:
        model_name = model_info["name"]
        
        # 配额检查
        if not should_use_model(model_name):
            print(f"  ⏭️ 跳过 {model_name} (配额不足)")
            fallback_count += 1
            continue
        
        # 调用
        print(f"  → {model_name}")
        
        # 根据provider调用
        provider = model_info["provider"]
        
        if provider == "ollama":
            ollama = get_ollama()
            result = ollama.generate(model_name.split(":")[-1], prompt)
        elif provider == "minimax":
            from providers import get_minimax
            minimax = get_minimax()
            result = minimax.generate(model_name, prompt)
        else:
            result = {"success": False, "error": "Unknown provider"}
        
        if result["success"]:
            return {
                "success": True,
                "response": result["response"],
                "model": model_name,
                "task_type": task_type,
                "fallback_count": fallback_count,
            }
        
        fallback_count += 1
        print(f"  ⚠️ 失败: {result.get('error')}")
    
    return {"success": False, "error": "All models failed"}


# 测试
if __name__ == "__main__":
    print("=== Task Classifier + Router ===\n")
    
    tests = [
        "帮我写一个Python函数",
        "分析这段代码",
        "写一首诗",
        "什么是AI？",
    ]
    
    for prompt in tests:
        task = classify_task(prompt)
        print(f"输入: {prompt}")
        print(f"  → 任务: {task}")
        
        # 自动路由
        result = route(prompt=prompt)
        print(f"  → 模型: {result.get('model', 'N/A')}")
        print(f"  → 成功: {result['success']}\n")
