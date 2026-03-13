#!/usr/bin/env python3
"""
Coach Agent - 教练代理
"""
import requests
from typing import Dict


class CoachAgent:
    """AI教练代理"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
    
    def teach(self, topic: str) -> str:
        """教授知识"""
        
        prompt = f"""作为Python导师，简洁讲解: {topic}

要求：
- 简单易懂
- 举例说明
- 50字内
"""
        return self._call_llm(prompt)
    
    def explain_code(self, code: str) -> str:
        """解释代码"""
        
        prompt = f"""解释这段Python代码:

{code}
"""
        return self._call_llm(prompt)
    
    def _call_llm(self, prompt: str) -> str:
        try:
            resp = requests.post(
                f"{self.ollama_url}/api/generate",
                json={"model": "qwen2.5:14b", "prompt": prompt, "stream": False},
                timeout=30
            )
            if resp.status_code == 200:
                return resp.json().get("response", "")[:200]
        except:
            pass
        return "导师暂时无法回答"


_agent = None

def get_coach_agent():
    global _agent
    if _agent is None:
        _agent = CoachAgent()
    return _agent
