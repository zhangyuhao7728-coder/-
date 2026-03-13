#!/usr/bin/env python3
"""
Vector Memory - 向量记忆 (简化版)
"""
import json
from datetime import datetime
from typing import Dict, List


class VectorMemory:
    """向量记忆"""
    
    def __init__(self):
        self.embeddings = []
    
    def add(self, text: str, metadata: Dict = None):
        """添加记忆"""
        # 简化: 使用文本长度作为"向量"
        embedding = {
            "text": text,
            "vector": self._simple_embed(text),
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat(),
        }
        self.embeddings.append(embedding)
    
    def _simple_embed(self, text: str) -> list:
        """简单 embedding"""
        # 简化实现
        return [hash(text) % 1000]
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """搜索"""
        # 简化: 文本包含即返回
        results = []
        for e in self.embeddings:
            if query.lower() in e["text"].lower():
                results.append(e)
        return results[:top_k]
    
    def get_all(self) -> List[Dict]:
        return self.embeddings


# 全局实例
_vmem = None

def get_vector_memory() -> VectorMemory:
    global _vmem
    if _vmem is None:
        _vmem = VectorMemory()
    return _vmem
