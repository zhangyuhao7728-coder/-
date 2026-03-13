#!/usr/bin/env python3
"""
Weekly Challenge - 每周挑战
"""
from datetime import datetime, timedelta
from typing import Dict


class WeeklyChallenge:
    """每周挑战"""
    
    def __init__(self):
        self.current = None
        self.completed = []
        self.start_date = None
    
    def start_new(self, challenge: Dict):
        """开始新挑战"""
        
        self.current = {
            **challenge,
            "start_time": datetime.now().isoformat(),
            "progress": 0
        }
        self.start_date = datetime.now()
    
    def update_progress(self, progress: int):
        """更新进度"""
        
        if self.current:
            self.current["progress"] = min(100, max(0, progress))
    
    def complete(self):
        """完成挑战"""
        
        if self.current:
            self.current["completed"] = True
            self.current["end_time"] = datetime.now().isoformat()
            
            # 计算用时
            if self.start_date:
                days = (datetime.now() - self.start_date).days
                self.current["days_used"] = days
            
            self.completed.append(self.current)
            self.current = None
    
    def get_status(self) -> Dict:
        """获取状态"""
        
        if not self.current:
            return {"active": False}
        
        return {
            "active": True,
            "title": self.current.get("title"),
            "progress": self.current.get("progress", 0),
            "difficulty": self.current.get("difficulty"),
            "type": self.current.get("type")
        }
    
    def get_history(self) -> list:
        """获取历史"""
        return self.completed


_challenge = None

def get_weekly_challenge() -> WeeklyChallenge:
    global _challenge
    if _challenge is None:
        _challenge = WeeklyChallenge()
    return _challenge
