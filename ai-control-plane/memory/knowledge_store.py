#!/usr/bin/env python3
"""
Knowledge Store - 知识库
"""
import json
from datetime import datetime


class KnowledgeStore:
    """知识库"""
    
    def __init__(self):
        self.knowledge = {}
    
    def add(self, key: str, value: any, category: str = "general"):
        """添加知识"""
        if category not in self.knowledge:
            self.knowledge[category] = {}
        
        self.knowledge[category][key] = {
            "value": value,
            "timestamp": datetime.now().isoformat(),
        }
    
    def get(self, key: str, category: str = "general") -> any:
        """获取知识"""
        if category in self.knowledge and key in self.knowledge[category]:
            return self.knowledge[category][key]["value"]
        return None
    
    def search(self, query: str) -> dict:
        """搜索"""
        results = {}
        for cat, items in self.knowledge.items():
            for key, value in items.items():
                if query.lower() in str(value["value"]).lower():
                    results[f"{cat}.{key}"] = value["value"]
        return results
    
    def list_categories(self) -> list:
        return list(self.knowledge.keys())


# 全局实例
_store = None

def get_knowledge_store() -> KnowledgeStore:
    global _store
    if _store is None:
        _store = KnowledgeStore()
    return _store
