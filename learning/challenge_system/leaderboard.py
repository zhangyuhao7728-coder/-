#!/usr/bin/env python3
"""
Leaderboard - 排行榜
"""
from typing import List, Dict


class Leaderboard:
    """排行榜"""
    
    def __init__(self):
        self.users = {}
    
    def add_points(self, user_id: str, points: int):
        """加分"""
        
        if user_id not in self.users:
            self.users[user_id] = {
                "points": 0,
                "challenges": 0,
                "streak": 0
            }
        
        self.users[user_id]["points"] += points
        self.users[user_id]["challenges"] += 1
    
    def get_rank(self, user_id: str) -> int:
        """获取排名"""
        
        sorted_users = sorted(
            self.users.items(),
            key=lambda x: x[1]["points"],
            reverse=True
        )
        
        for i, (uid, _) in enumerate(sorted_users, 1):
            if uid == user_id:
                return i
        
        return len(sorted_users) + 1
    
    def get_top(self, n: int = 10) -> List[Dict]:
        """获取Top N"""
        
        sorted_users = sorted(
            self.users.items(),
            key=lambda x: x[1]["points"],
            reverse=True
        )
        
        result = []
        for i, (uid, data) in enumerate(sorted_users[:n], 1):
            result.append({
                "rank": i,
                "user_id": uid,
                "points": data["points"],
                "challenges": data["challenges"]
            })
        
        return result
    
    def reset(self):
        """重置"""
        self.users = {}


_leaderboard = None

def get_leaderboard() -> Leaderboard:
    global _leaderboard
    if _leaderboard is None:
        _leaderboard = Leaderboard()
    return _leaderboard


# 测试
if __name__ == "__main__":
    lb = get_leaderboard()
    
    print("=== 排行榜测试 ===\n")
    
    # 添加分数
    lb.add_points("user1", 100)
    lb.add_points("user2", 80)
    lb.add_points("user3", 120)
    
    # Top
    print("Top 3:")
    for u in lb.get_top(3):
        print(f"  #{u['rank']} {u['user_id']}: {u['points']}分")
