#!/usr/bin/env python3
"""
Design Questions - 设计问题
"""
from typing import Dict, List


class DesignQuestions:
    """系统设计问题"""
    
    QUESTIONS = [
        {
            "id": "url_shortener",
            "title": "设计短链接系统",
            "difficulty": "easy",
            "questions": [
                "如何生成短链接?",
                "如何存储映射关系?",
                "如何处理高并发?"
            ],
            "answer": "使用Base62编码，使用Redis+MySQL，使用计数器方式"
        },
        {
            "id": "twitter",
            "title": "设计Twitter",
            "difficulty": "medium",
            "questions": [
                "如何存储tweet?",
                "如何实现timeline?",
                "如何设计关注系统?"
            ],
            "answer": "使用NoSQL存储，推拉结合，关系型+缓存"
        },
        {
            "id": "message_queue",
            "title": "设计消息队列",
            "difficulty": "hard",
            "questions": [
                "如何保证消息顺序?",
                "如何实现消息持久化?",
                "如何处理重复消息?"
            ],
            "answer": "使用分区+序号，磁盘持久化，幂等设计"
        },
        {
            "id": "web_crawler",
            "title": "设计爬虫系统",
            "difficulty": "medium",
            "questions": [
                "如何抓取URL?",
                "如何去重?",
                "如何存储网页?"
            ],
            "answer": "BFS抓取，URL去重，网页存储"
        }
    ]
    
    def get_question(self, difficulty: str = None) -> Dict:
        """获取问题"""
        questions = self.QUESTIONS
        
        if difficulty:
            questions = [q for q in questions if q["difficulty"] == difficulty]
        
        return questions[0] if questions else {}
    
    def get_all(self) -> List[Dict]:
        return self.QUESTIONS


_questions = None

def get_design_questions():
    global _questions
    if _questions is None:
        _questions = DesignQuestions()
    return _questions
