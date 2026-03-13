#!/usr/bin/env python3
"""
System Design Trainer - 系统设计训练
"""
from typing import Dict, List


class SystemDesignTrainer:
    """系统设计训练"""
    
    # 设计题目
    DESIGN_PROBLEMS = [
        {
            "id": "url_shortener",
            "title": "短链接系统",
            "difficulty": "easy",
            "questions": [
                "如何生成短链接?",
                "如何存储映射关系?",
                "如何处理高并发?"
            ]
        },
        {
            "id": "twitter",
            "title": "Twitter类系统",
            "difficulty": "medium",
            "questions": [
                "如何存储 tweets?",
                "如何实现时间线?",
                "如何设计关注系统?"
            ]
        },
        {
            "id": "distributed_cache",
            "title": "分布式缓存",
            "difficulty": "hard",
            "questions": [
                "如何实现缓存一致性?",
                "如何处理缓存穿透?",
                "如何设计淘汰策略?"
            ]
        }
    ]
    
    def __init__(self):
        self.completed = []
    
    def get_problem(self, difficulty: str = None) -> Dict:
        """获取设计题目"""
        
        problems = self.DESIGN_PROBLEMS
        
        if difficulty:
            problems = [p for p in problems if p["difficulty"] == difficulty]
        
        return problems[0] if problems else {}
    
    def get_guide(self, problem_id: str) -> Dict:
        """获取设计指南"""
        
        guides = {
            "url_shortener": {
                "components": ["URL生成器", "存储服务", "重定向服务"],
                "tech": ["Redis", "MySQL", "CDN"],
                "steps": [
                    "1. 确定需求和规模",
                    "2. 设计API接口",
                    "3. 选择存储方案",
                    "4. 考虑扩展性"
                ]
            }
        }
        
        return guides.get(problem_id, {"steps": ["分析需求", "设计架构", "考虑扩展"]})
    
    def evaluate_design(self, design: str) -> Dict:
        """评估设计"""
        
        score = 70
        
        if "数据库" in design or "DB" in design:
            score += 10
        if "缓存" in design or "Cache" in design:
            score += 10
        if "扩展" in design or "Scale" in design:
            score += 10
        
        return {
            "score": min(100, score),
            "feedback": "设计合理，考虑了存储和扩展"
        }


_trainer = None

def get_system_design_trainer() -> SystemDesignTrainer:
    global _trainer
    if _trainer is None:
        _trainer = SystemDesignTrainer()
    return _trainer


# 测试
if __name__ == "__main__":
    trainer = get_system_design_trainer()
    
    print("=== 系统设计训练测试 ===\n")
    
    problem = trainer.get_problem()
    print(f"题目: {problem['title']}")
    print(f"难度: {problem['difficulty']}")
    print(f"问题: {problem['questions']}")
