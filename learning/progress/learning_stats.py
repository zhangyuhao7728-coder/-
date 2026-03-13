#!/usr/bin/env python3
"""
Learning Stats - 学习统计
"""
import json
from datetime import datetime
from typing import Dict


class LearningStats:
    """学习统计"""
    
    def __init__(self):
        self.data_file = "/Users/zhangyuhao/项目/Ai学习系统/learning/learning-data/stats.json"
        self.load()
    
    def load(self):
        try:
            with open(self.data_file) as f:
                self.data = json.load(f)
        except:
            self.data = {
                "total_time": 0,
                "problems_solved": 0,
                "projects_completed": 0,
                "skills": {},
                "daily": {},
                "streak": 0
            }
    
    def save(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    # 记录
    def add_time(self, minutes: int):
        """添加学习时间"""
        self.data["total_time"] += minutes
        self._record_daily("time", minutes)
        self.save()
    
    def add_problem(self):
        """添加解题"""
        self.data["problems_solved"] += 1
        self._record_daily("problems", 1)
        self.save()
    
    def add_project(self):
        """添加项目"""
        self.data["projects_completed"] += 1
        self._record_daily("projects", 1)
        self.save()
    
    def add_skill(self, skill: str, points: int):
        """添加技能点"""
        if skill not in self.data["skills"]:
            self.data["skills"][skill] = 0
        self.data["skills"][skill] += points
        self.save()
    
    def _record_daily(self, key: str, value: int):
        """记录每日"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in self.data["daily"]:
            self.data["daily"][today] = {"time": 0, "problems": 0, "projects": 0}
        
        self.data["daily"][today][key] = self.data["daily"][today].get(key, 0) + value
    
    # 获取
    def get_total(self) -> Dict:
        """获取总统计"""
        return {
            "total_time": self.data["total_time"],
            "problems": self.data["problems_solved"],
            "projects": self.data["projects_completed"],
            "skills": len(self.data["skills"]),
            "streak": self.data["streak"]
        }
    
    def get_level(self) -> int:
        """计算等级"""
        total = self.data["total_time"] // 60
        return total // 10 + 1
    
    def get_today(self) -> Dict:
        """获取今日"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.data["daily"].get(today, {"time": 0, "problems": 0, "projects": 0})
    
    def get_week(self) -> Dict:
        """获取本周"""
        week_data = {"time": 0, "problems": 0, "projects": 0}
        
        for i in range(7):
            date = datetime.now().strftime("%Y-%m-%d")
        
        return week_data
    
    def print_summary(self):
        """打印摘要"""
        total = self.get_total()
        level = self.get_level()
        today = self.get_today()
        
        print("="*40)
        print("     📊 学习统计")
        print("="*40)
        print(f"🕐 总学习: {total['total_time']}分钟")
        print(f"📝 解题: {total['problems']}道")
        print(f"💻 项目: {total['projects']}个")
        print(f"📦 技能: {total['skills']}个")
        print(f"🔥 连续: {total['streak']}天")
        print(f"⭐ 等级: Lv.{level}")
        print("="*40)
        print(f"\n今日:")
        print(f"  学习: {today['time']}分钟")
        print(f"  解题: {today['problems']}道")


_stats = None

def get_learning_stats() -> LearningStats:
    global _stats
    if _stats is None:
        _stats = LearningStats()
    return _stats


# 测试
if __name__ == "__main__":
    stats = get_learning_stats()
    stats.print_summary()
