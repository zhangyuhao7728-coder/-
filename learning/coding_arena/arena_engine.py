#!/usr/bin/env python3
"""
Arena Engine - 竞技场引擎
"""
import random
import time
from typing import Dict, List


class Arena:
    """AI编程竞技场"""
    
    # 挑战类型
    CHALLENGE_TYPES = {
        "algorithm": "算法挑战",
        "optimization": "代码优化",
        "bugfix": "Bug修复",
        "architecture": "架构设计"
    }
    
    def __init__(self):
        self.current_challenge = None
        self.start_time = None
        self.attempts = 0
    
    def start_challenge(self, challenge_type: str = "algorithm") -> Dict:
        """开始挑战"""
        
        challenges = self._get_challenges(challenge_type)
        challenge = random.choice(challenges)
        
        self.current_challenge = {
            **challenge,
            "type": challenge_type,
            "start_time": time.time(),
            "time_limit": 30 * 60  # 30分钟
        }
        
        return self.current_challenge
    
    def _get_challenges(self, challenge_type: str) -> List[Dict]:
        """获取挑战列表"""
        
        if challenge_type == "algorithm":
            return [
                {"id": "two_sum", "title": "两数之和", "difficulty": "easy", "points": 100},
                {"id": "lru_cache", "title": "LRU缓存", "difficulty": "hard", "points": 300},
                {"id": "merge_sort", "title": "归并排序", "difficulty": "medium", "points": 200},
            ]
        elif challenge_type == "optimization":
            return [
                {"id": "perf_opt", "title": "性能优化", "difficulty": "medium", "points": 200},
                {"id": "mem_opt", "title": "内存优化", "difficulty": "hard", "points": 300},
            ]
        else:
            return [
                {"id": "fix_bug", "title": "修复Bug", "difficulty": "easy", "points": 100},
            ]
    
    def submit(self, code: str) -> Dict:
        """提交代码"""
        
        self.attempts += 1
        
        if not self.current_challenge:
            return {"error": "没有进行中的挑战"}
        
        # 简单评分
        score = random.randint(60, 100)
        
        elapsed = time.time() - self.current_challenge.get("start_time", 0)
        
        return {
            "score": score,
            "attempts": self.attempts,
            "time_used": int(elapsed),
            "passed": score >= 60
        }
    
    def get_status(self) -> Dict:
        """获取状态"""
        
        if not self.current_challenge:
            return {"active": False}
        
        elapsed = time.time() - self.current_challenge.get("start_time", 0)
        remaining = self.current_challenge.get("time_limit", 0) - elapsed
        
        return {
            "active": True,
            "challenge": self.current_challenge.get("title"),
            "remaining": int(remaining),
            "attempts": self.attempts
        }


_arena = None

def get_arena() -> Arena:
    global _arena
    if _arena is None:
        _arena = Arena()
    return _arena


# 测试
if __name__ == "__main__":
    arena = get_arena()
    
    print("=== 竞技场测试 ===\n")
    
    # 开始挑战
    challenge = arena.start_challenge("algorithm")
    print(f"挑战: {challenge['title']}")
    print(f"难度: {challenge['difficulty']}")
    print(f"分数: {challenge['points']}")
    
    # 提交
    result = arena.submit("print('hello')")
    print(f"\n得分: {result['score']}")
    print(f"通过: {result['passed']}")
