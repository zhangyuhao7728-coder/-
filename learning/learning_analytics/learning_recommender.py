#!/usr/bin/env python3
"""
Learning Recommender - 学习推荐
"""
from typing import Dict, List


class LearningRecommender:
    """学习推荐"""
    
    def __init__(self):
        self.history = []
    
    def recommend(self, stats: Dict, weakness: List[Dict] = None) -> List[Dict]:
        """推荐学习内容"""
        
        recommendations = []
        
        # 基于弱点推荐
        if weakness:
            for w in weakness[:2]:
                skill = w.get("skill", "")
                recommendations.append({
                    "type": "weakness",
                    "topic": skill,
                    "reason": f"{skill}能力需要提高",
                    "priority": "high"
                })
        
        # 基于水平推荐
        level = stats.get("level", 1)
        
        if level == 1:
            recommendations.append({
                "type": "level",
                "topic": "Python基础语法",
                "reason": "巩固基础",
                "priority": "high"
            })
        elif level == 2:
            recommendations.append({
                "type": "level",
                "topic": "算法和数据结构",
                "reason": "提升编程能力",
                "priority": "medium"
            })
        
        return recommendations
    
    def get_daily_recommendation(self) -> Dict:
        """每日推荐"""
        
        import random
        
        topics = [
            "复习函数",
            "练习列表操作",
            "做一道算法题",
            "阅读一篇技术文章"
        ]
        
        return {
            "topic": random.choice(topics),
            "duration": "30分钟"
        }


_recommender = None

def get_learning_recommender():
    global _recommender
    if _recommender is None:
        _recommender = LearningRecommender()
    return _recommender
