#!/usr/bin/env python3
"""
Skill Tree - 技能树系统
"""
from typing import Dict, List


class SkillTree:
    """技能树"""
    
    # Python技能树
    SKILL_TREE = {
        "Python": {
            "children": ["Syntax", "DataTypes", "ControlFlow"],
            "mastery": 0
        },
        "Syntax": {
            "parent": "Python",
            "children": ["Variables", "Operators"],
            "mastery": 0
        },
        "DataTypes": {
            "parent": "Python", 
            "children": ["List", "Dict", "String"],
            "mastery": 0
        },
        "ControlFlow": {
            "parent": "Python",
            "children": ["IfElse", "Loops", "Functions"],
            "mastery": 0
        },
        "Functions": {
            "parent": "ControlFlow",
            "children": ["Lambda", "Decorators", "Generators"],
            "mastery": 0
        },
        "OOP": {
            "parent": "Python",
            "children": ["Class", "Inheritance", "Polymorphism"],
            "mastery": 0
        },
        "DataStructures": {
            "parent": "Python",
            "children": ["List", "Dict", "Set", "Tuple"],
            "mastery": 0
        },
        "Algorithms": {
            "parent": "Python",
            "children": ["Sorting", "Searching", "DP"],
            "mastery": 0
        },
        "Web": {
            "parent": "Python",
            "children": ["Flask", "Django", "API"],
            "mastery": 0
        },
        "AI": {
            "parent": "Python",
            "children": ["ML", "DL", "NLP"],
            "mastery": 0
        }
    }
    
    def __init__(self):
        self.skills = self.SKILL_TREE.copy()
    
    def update_mastery(self, skill: str, value: int):
        """更新掌握度"""
        if skill in self.skills:
            self.skills[skill]["mastery"] = min(100, max(0, value))
    
    def get_mastery(self, skill: str) -> int:
        """获取掌握度"""
        return self.skills.get(skill, {}).get("mastery", 0)
    
    def can_learn(self, skill: str) -> bool:
        """是否可以学习"""
        if skill not in self.skills:
            return True
        
        parent = self.skills[skill].get("parent")
        if parent is None:
            return True
        
        # 父技能需要达到50%才能解锁
        return self.get_mastery(parent) >= 50
    
    def get_unlocked(self) -> List[str]:
        """获取已解锁技能"""
        return [s for s in self.skills if self.can_learn(s)]
    
    def learn(self, skill: str, points: int = 10):
        """学习技能"""
        if not self.can_learn(skill):
            return False
        
        current = self.get_mastery(skill)
        self.update_mastery(skill, current + points)
        return True
    
    def get_tree(self) -> Dict:
        """获取技能树"""
        return self.skills
    
    def print_tree(self):
        """打印技能树"""
        print("🌳 Python技能树\n")
        
        for skill, info in self.skills.items():
            mastery = info["mastery"]
            status = "🔒" if not self.can_learn(skill) else "✅"
            
            # 进度条
            bar = "█" * (mastery // 10) + "░" * (10 - mastery // 10)
            
            print(f"{status} {skill}: [{bar}] {mastery}%")


_tree = None

def get_skill_tree() -> SkillTree:
    global _tree
    if _tree is None:
        _tree = SkillTree()
    return _tree


# 测试
if __name__ == "__main__":
    tree = get_skill_tree()
    
    print("=== 技能树测试 ===\n")
    
    # 学习技能
    tree.learn("Variables", 30)
    tree.learn("List", 50)
    
    # 打印
    tree.print_tree()
    
    print("\n已解锁:", tree.get_unlocked())
