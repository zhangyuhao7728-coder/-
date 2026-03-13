#!/usr/bin/env python3
"""
Learning Recommender - 学习推荐
"""


class LearningRecommender:
    """学习推荐"""
    
    # 技能依赖
    SKILL_DEPS = {
        "变量": [],
        "函数": ["变量"],
        "列表": ["变量"],
        "字典": ["变量"],
        "循环": ["变量"],
        "函数": ["变量"],
        "类": ["函数", "列表"],
    }
    
    def recommend(self, current_skills: list, level: str) -> list:
        """推荐下一步学习"""
        recommendations = []
        
        # 根据当前技能推荐
        if "变量" in current_skills:
            recommendations.append("函数")
            recommendations.append("列表")
        
        if "函数" in current_skills:
            recommendations.append("循环")
        
        if "循环" in current_skills:
            recommendations.append("字典")
        
        if "列表" in current_skills:
            recommendations.append("字典")
        
        return recommendations[:3]
    
    def get_next_topic(self, skill: str) -> str:
        topics = {
            "变量": "学习如何使用变量存储数据",
            "函数": "学习如何定义和调用函数",
            "列表": "学习列表的增删改查",
            "字典": "学习字典的键值对操作",
            "循环": "学习for和while循环",
            "条件": "学习if条件判断",
        }
        return topics.get(skill, "继续深入学习")


_recommender = None

def get_learning_recommender():
    global _recommender
    if _recommender is None:
        _recommender = LearningRecommender()
    return _recommender
