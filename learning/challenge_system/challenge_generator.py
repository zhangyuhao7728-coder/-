#!/usr/bin/env python3
"""
Challenge Generator - 挑战生成器
"""
import random
from typing import Dict, List


class ChallengeGenerator:
    """挑战生成"""
    
    # 算法挑战
    ALGO_CHALLENGES = [
        {"id": "two_sum", "title": "两数之和", "difficulty": "easy"},
        {"id": "reverse", "title": "反转链表", "difficulty": "medium"},
        {"id": "valid_parens", "title": "有效括号", "difficulty": "easy"},
        {"id": "merge_sort", "title": "归并排序", "difficulty": "medium"},
        {"id": "lru_cache", "title": "LRU缓存", "difficulty": "hard"},
        {"id": "binary_tree", "title": "二叉树遍历", "difficulty": "medium"},
    ]
    
    # 项目挑战
    PROJECT_CHALLENGES = [
        {"id": "todo_cli", "title": "CLI待办应用", "difficulty": "easy"},
        {"id": "web_crawler", "title": "简单爬虫", "difficulty": "medium"},
        {"id": "weather_api", "title": "天气API", "difficulty": "medium"},
        {"id": "chat_bot", "title": "聊天机器人", "difficulty": "hard"},
        {"id": "file_manager", "title": "文件管理器", "difficulty": "hard"},
    ]
    
    def generate_daily(self) -> Dict:
        """生成每日挑战"""
        
        challenge = random.choice(self.ALGO_CHALLENGES)
        
        return {
            "type": "daily",
            "title": challenge["title"],
            "difficulty": challenge["difficulty"],
            "points": self._calc_points(challenge["difficulty"])
        }
    
    def generate_weekly(self) -> Dict:
        """生成每周挑战"""
        
        challenge = random.choice(self.PROJECT_CHALLENGES)
        
        return {
            "type": "weekly",
            "title": challenge["title"],
            "difficulty": challenge["difficulty"],
            "points": self._calc_points(challenge["difficulty"]) * 5,
            "deadline": "7天后"
        }
    
    def _calc_points(self, difficulty: str) -> int:
        points = {
            "easy": 10,
            "medium": 30,
            "hard": 50
        }
        return points.get(difficulty, 10)
    
    def get_challenges(self, difficulty: str = None) -> List[Dict]:
        """获取挑战列表"""
        
        challenges = self.ALGO_CHALLENGES + self.PROJECT_CHALLENGES
        
        if difficulty:
            challenges = [c for c in challenges if c["difficulty"] == difficulty]
        
        return challenges


_generator = None

def get_challenge_generator() -> ChallengeGenerator:
    global _generator
    if _generator is None:
        _generator = ChallengeGenerator()
    return _generator


# 测试
if __name__ == "__main__":
    gen = get_challenge_generator()
    
    print("=== 挑战生成测试 ===\n")
    
    daily = gen.generate_daily()
    print(f"每日挑战: {daily['title']} ({daily['difficulty']}) +{daily['points']}分")
    
    weekly = gen.generate_weekly()
    print(f"每周挑战: {weekly['title']} ({weekly['difficulty']}) +{weekly['points']}分")
