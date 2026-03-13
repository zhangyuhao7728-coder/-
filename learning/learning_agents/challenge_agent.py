#!/usr/bin/env python3
"""
Challenge Agent - 挑战代理
"""
import random
from typing import Dict


class ChallengeAgent:
    """挑战生成代理"""
    
    CHALLENGES = [
        {"title": "两数之和", "difficulty": "easy", "points": 10},
        {"title": "反转链表", "difficulty": "medium", "points": 30},
        {"title": "LRU缓存", "difficulty": "hard", "points": 50},
    ]
    
    def generate(self, difficulty: str = None) -> Dict:
        """生成挑战"""
        
        challenges = self.CHALLENGES
        
        if difficulty:
            challenges = [c for c in challenges if c["difficulty"] == difficulty]
        
        return random.choice(challenges)
    
    def daily_challenge(self) -> Dict:
        """每日挑战"""
        
        challenge = self.generate()
        
        return {
            **challenge,
            "type": "daily",
            "expire": "23:59"
        }


_agent = None

def get_challenge_agent():
    global _agent
    if _agent is None:
        _agent = ChallengeAgent()
    return _agent
