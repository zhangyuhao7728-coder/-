#!/usr/bin/env python3
"""
学习进度追踪
"""
import json
import os
from datetime import datetime


class ProgressTracker:
    def __init__(self):
        self.data_file = os.path.expanduser("~/项目/ai-coding-academy/progress/data.json")
        self.load()
    
    def load(self):
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file) as f:
                self.data = json.load(f)
        except:
            self.data = {
                "total_time": 0,
                "problems_solved": 0,
                "projects_done": 0,
                "level": 1,
                "streak": 0,
                "skills": {},
                "history": []
            }
    
    def save(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_time(self, minutes: int):
        self.data["total_time"] += minutes
        self._add_history(f"学习了 {minutes} 分钟")
        self.save()
    
    def add_problem(self):
        self.data["problems_solved"] += 1
        self._add_history("解决了1道题")
        self.save()
    
    def add_project(self):
        self.data["projects_done"] += 1
        self._add_history("完成了1个项目")
        self.save()
    
    def add_skill(self, skill: str, points: int):
        if skill not in self.data["skills"]:
            self.data["skills"][skill] = 0
        self.data["skills"][skill] += points
        self._add_history(f"{skill} +{points}点")
        self.save()
    
    def _add_history(self, action: str):
        self.data["history"].append({
            "action": action,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        self.data["history"] = self.data["history"][-50:]
    
    def get_stats(self):
        return self.data
    
    def get_level(self):
        return self.data.get("level", 1)


_tracker = None

def get_progress_tracker():
    global _tracker
    if _tracker is None:
        _tracker = ProgressTracker()
    return _tracker
