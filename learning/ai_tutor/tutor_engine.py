#!/usr/bin/env python3
"""
AI Tutor Engine - AI导师引擎
"""
import requests
from typing import Dict, List


class AITutor:
    """AI导师"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
    
    def call_llm(self, prompt: str) -> str:
        try:
            resp = requests.post(
                f"{self.ollama_url}/api/generate",
                json={"model": "qwen2.5:14b", "prompt": prompt, "stream": False},
                timeout=60
            )
            if resp.status_code == 200:
                return resp.json().get("response", "")
        except:
            pass
        return "导师暂时无法回答"
    
    # ===== 1. 解释概念 =====
    def explain(self, topic: str) -> str:
        prompt = f"""你是一个耐心的Python导师。用简单易懂的方式解释：

{topic}

要求：
- 用生活中的例子
- 给出代码示例
- 100字内
"""
        return self.call_llm(prompt)
    
    # ===== 2. 代码审查 =====
    def review_code(self, code: str) -> Dict:
        prompt = f"""作为Python导师，分析这段代码：

```python
{code}
```

给出：
1. 优点
2. 问题
3. 改进建议
"""
        result = self.call_llm(prompt)
        
        return {
            "code": code,
            "review": result,
            "score": self._calc_score(result)
        }
    
    def _calc_score(self, review: str) -> int:
        score = 80
        if "问题" in review or "错误" in review:
            score -= 10
        if "优点" in review:
            score += 5
        return min(100, max(0, score))
    
    # ===== 3. 问答 =====
    def answer(self, question: str) -> str:
        prompt = f"""作为Python导师，回答这个问题：

{question}

简短准确回答：
"""
        return self.call_llm(prompt)
    
    # ===== 4. 指导学习 =====
    def guide(self, current_level: str, goal: str) -> str:
        prompt = f"""导师指导：

当前水平：{current_level}
学习目标：{goal}

给出具体学习路径和建议：
"""
        return self.call_llm(prompt)


_tutor = None

def get_ai_tutor() -> AITutor:
    global _tutor
    if _tutor is None:
        _tutor = AITutor()
    return _tutor


# 测试
if __name__ == "__main__":
    tutor = get_ai_tutor()
    print("=== AI导师测试 ===\n")
    print(tutor.explain("什么是变量"))
