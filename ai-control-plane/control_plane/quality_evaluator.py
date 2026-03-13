#!/usr/bin/env python3
"""
Quality Evaluator - 质量评估器
功能：
1. 响应质量评估
2. 自动重试
3. 质量保证
"""
from typing import Dict, List, Optional


class QualityEvaluator:
    """质量评估器"""
    
    def __init__(self):
        # 评估配置
        self.min_lengths = {
            "code": 50,
            "analysis": 100,
            "creative": 50,
            "fast": 10,
            "general": 20,
        }
        
        # 统计
        self.stats = {
            "total": 0,
            "good": 0,
            "bad": 0,
            "retries": 0,
        }
        
        # 历史
        self.history = []
    
    def evaluate(self, response: str, task_type: str = "general") -> Dict:
        """
        评估响应质量
        
        Args:
            response: 模型响应
            task_type: 任务类型
        
        Returns:
            {
                "quality": "good/bad",
                "score": 0-100,
                "reasons": []
            }
        """
        self.stats["total"] += 1
        
        score = 100
        reasons = []
        
        # 1. 长度检查
        min_length = self.min_lengths.get(task_type, 20)
        if len(response) < min_length:
            score -= 30
            reasons.append(f"Response too short ({len(response)} < {min_length})")
        
        # 2. 重复检查
        words = response.split()
        if len(words) > 10:
            unique_ratio = len(set(words)) / len(words)
            if unique_ratio < 0.3:
                score -= 20
                reasons.append("Too much repetition")
        
        # 3. 错误关键词
        error_keywords = ["error", "failed", "cannot", "unable", "sorry", "无法"]
        if any(kw in response.lower() for kw in error_keywords):
            score -= 15
            reasons.append("Contains error keywords")
        
        # 4. 空响应
        if not response or response.strip() == "":
            score = 0
            reasons.append("Empty response")
        
        # 5. 任务相关检查
        if task_type == "code":
            # 代码应该有缩进或关键字
            if not any(kw in response for kw in ["def ", "class ", "import ", "return", "print"]):
                score -= 10
                reasons.append("May not be valid code")
        
        if task_type == "creative":
            # 创意应该有一定长度
            if len(response) < 30:
                score -= 15
                reasons.append("Creative response too short")
        
        # 确保分数范围
        score = max(0, min(100, score))
        
        # 判定质量
        quality = "good" if score >= 60 else "bad"
        
        if quality == "good":
            self.stats["good"] += 1
        else:
            self.stats["bad"] += 1
        
        # 记录
        result = {
            "quality": quality,
            "score": score,
            "reasons": reasons,
            "length": len(response),
            "task_type": task_type,
        }
        
        self.history.append(result)
        
        return result
    
    def is_good(self, response: str, task_type: str = "general") -> bool:
        """快速判断是否合格"""
        result = self.evaluate(response, task_type)
        return result["quality"] == "good"
    
    def should_retry(self, response: str, task_type: str = "general", threshold: int = 60) -> bool:
        """
        判断是否应该重试
        
        如果质量低于阈值，返回True
        """
        result = self.evaluate(response, task_type)
        
        if result["score"] < threshold:
            self.stats["retries"] += 1
            return True
        
        return False
    
    # ========== 自动重试 ==========
    
    def retry_with_stronger(self, prompt: str, current_model: str, task_type: str) -> Dict:
        """
        用更强模型重试
        
        Args:
            prompt: 用户输入
            current_model: 当前模型
            task_type: 任务类型
        
        Returns:
            {"model": "...", "response": "...", "quality": "..."}
        """
        # 模型强度排名
        strength_order = [
            "qwen2.5:latest",        # 最弱
            "qwen2.5:7b",
            "deepseek-coder:6.7b",
            "qwen3.5:9b",
            "volcengine/doubao-seed-code",
            "minimax/MiniMax-M2.5",  # 最强
        ]
        
        # 找到当前模型的位置
        try:
            current_idx = strength_order.index(current_model)
        except:
            current_idx = 0
        
        # 尝试更强的模型
        for i in range(current_idx + 1, len(strength_order)):
            stronger_model = strength_order[i]
            
            print(f"  → 重试使用更强的模型: {stronger_model}")
            
            # 这里应该调用模型
            # 简化版返回信息
            return {
                "model": stronger_model,
                "response": f"[使用{stronger_model}重试]",
                "quality": "good",
                "retried": True,
            }
        
        return {
            "model": current_model,
            "response": "无法提升质量",
            "quality": "bad",
            "retried": False,
        }
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return self.stats.copy()
    
    def print_report(self):
        """打印报告"""
        stats = self.stats
        
        total = stats["total"]
        good_pct = (stats["good"] / total * 100) if total > 0 else 0
        bad_pct = (stats["bad"] / total * 100) if total > 0 else 0
        retry_pct = (stats["retries"] / total * 100) if total > 0 else 0
        
        print("=== Quality Report ===\n")
        print(f"总评估数: {total}")
        print(f"✅ 合格: {stats['good']} ({good_pct:.1f}%)")
        print(f"❌ 不合格: {stats['bad']} ({bad_pct:.1f}%)")
        print(f"🔄 重试: {stats['retries']} ({retry_pct:.1f}%)")


# 全局实例
_evaluator = None

def get_quality_evaluator() -> QualityEvaluator:
    global _evaluator
    if _evaluator is None:
        _evaluator = QualityEvaluator()
    return _evaluator


def evaluate(response: str, task_type: str = "general") -> Dict:
    """评估质量"""
    return get_quality_evaluator().evaluate(response, task_type)


# 测试
if __name__ == "__main__":
    ev = get_quality_evaluator()
    
    print("=== Quality Evaluator 测试 ===\n")
    
    # 测试用例
    tests = [
        ("def hello():\n    print('hello')", "code"),
        ("OK", "code"),  # 太短
        ("这是一段很长的分析内容，用于解释某些概念和原理..." * 3, "analysis"),
        ("OK", "fast"),
    ]
    
    for response, task_type in tests:
        result = ev.evaluate(response, task_type)
        
        print(f"任务: {task_type}")
        print(f"  长度: {len(response)}")
        print(f"  质量: {result['quality']}")
        print(f"  分数: {result['score']}")
        print(f"  原因: {result['reasons'] or '无'}")
        print()
    
    ev.print_report()
