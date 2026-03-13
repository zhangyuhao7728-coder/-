#!/usr/bin/env python3
"""
Progress Tracker - 学习进度追踪系统
"""
import json
from datetime import datetime
from typing import Dict


class ProgressTracker:
    """学习进度追踪"""
    
    def __init__(self):
        self.data_file = "/Users/zhangyuhao/项目/Ai学习系统/learning/learning-data/progress.json"
        self.load()
    
    def load(self):
        try:
            with open(self.data_file) as f:
                self.data = json.load(f)
        except:
            self.data = {
                "total_time": 0,      # 总学习时间(分钟)
                "problems_solved": 0,   # 解决的题目
                "projects_done": 0,     # 完成的项目
                "skills": {},           # 技能点
                "history": [],          # 学习历史
                "streak": 0            # 连续学习天数
            }
    
    def save(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    # ===== 记录学习 =====
    
    def add_time(self, minutes: int):
        """添加学习时间"""
        self.data["total_time"] += minutes
        self._add_history(f"学习了 {minutes} 分钟")
        self.save()
    
    def add_problem(self, solved: bool = True):
        """添加解题"""
        if solved:
            self.data["problems_solved"] += 1
            self._add_history("解决了1道题")
        self.save()
    
    def add_project(self):
        """添加项目"""
        self.data["projects_done"] += 1
        self._add_history("完成了1个项目")
        self.save()
    
    def add_skill(self, skill: str, points: int):
        """添加技能点"""
        if skill not in self.data["skills"]:
            self.data["skills"][skill] = 0
        self.data["skills"][skill] += points
        self._add_history(f"{skill} +{points}点")
        self.save()
    
    # ===== 获取统计 =====
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "total_time": self.data["total_time"],
            "problems": self.data["problems_solved"],
            "projects": self.data["projects_done"],
            "streak": self.data["streak"],
            "skills": self.data["skills"]
        }
    
    def get_level(self) -> int:
        """计算等级"""
        total = self.data["total_time"] // 60  # 转为小时
        return total // 10 + 1
    
    # ===== 历史 =====
    
    def _add_history(self, action: str):
        """添加历史记录"""
        self.data["history"].append({
            "action": action,
            "time": datetime.now().strftime("%H:%M")
        })
        # 只保留最近50条
        self.data["history"] = self.data["history"][-50:]
    
    def get_history(self, n: int = 10) -> list:
        """获取历史"""
        return self.data["history"][-n:]
    
    # ===== 显示 =====
    
    def print_stats(self):
        """打印统计"""
        stats = self.get_stats()
        level = self.get_level()
        
        print("="*40)
        print("      📊 学习进度统计")
        print("="*40)
        print(f"🕐 总学习时间: {stats['total_time']} 分钟")
        print(f"📝 解决题目: {stats['problems']} 道")
        print(f"💻 完成项目: {stats['projects']} 个")
        print(f"🔥 连续学习: {stats['streak']} 天")
        print(f"⭐ 等级: Lv.{level}")
        print("="*40)
        
        if stats['skills']:
            print("\n📦 技能点:")
            for skill, points in stats['skills'].items():
                print(f"  {skill}: {points}")
        
        print("\n📜 最近:")
        for h in self.get_history(5):
            print(f"  {h['time']} - {h['action']}")
        
        print("="*40)


_tracker = None

def get_progress_tracker() -> ProgressTracker:
    global _tracker
    if _tracker is None:
        _tracker = ProgressTracker()
    return _tracker


# 测试
if __name__ == "__main__":
    tracker = get_progress_tracker()
    
    # 模拟学习
    tracker.add_time(30)
    tracker.add_problem(True)
    tracker.add_skill("Python", 15)
    
    # 显示
    tracker.print_stats()
