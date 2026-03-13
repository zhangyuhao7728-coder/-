#!/usr/bin/env python3
"""
AI Code Reviewer - AI代码审查
"""
import requests
from typing import Dict, List


class AICodeReviewer:
    """AI代码审查"""
    
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
        return "无法审查代码"
    
    def review(self, code: str) -> Dict:
        """审查代码"""
        
        prompt = f"""作为资深Python开发者，审查以下代码：

```python
{code}
```

给出：
1. 代码评分 (0-100)
2. 问题列表
3. 改进建议
"""
        result = self.call_llm(prompt)
        
        return {
            "code": code[:100],
            "review": result,
            "score": self._calc_score(code),
            "issues": self._find_issues(code)
        }
    
    def _calc_score(self, code: str) -> int:
        score = 80
        
        if len(code) > 500:
            score -= 10
        if "print(" in code:
            score -= 5
        if "#" not in code and len(code) > 100:
            score -= 10
        
        return max(0, min(100, score))
    
    def _find_issues(self, code: str) -> List[str]:
        issues = []
        
        if "==" in code and "=" in code:
            if "== " not in code:
                issues.append("注意赋值和比较")
        
        if "for" in code and "range" not in code and "in " not in code:
            issues.append("检查循环语法")
        
        return issues if issues else ["无明显问题"]


_reviewer = None

def get_ai_code_reviewer() -> AICodeReviewer:
    global _reviewer
    if _reviewer is None:
        _reviewer = AICodeReviewer()
    return _reviewer


# 测试
if __name__ == "__main__":
    reviewer = get_ai_code_reviewer()
    
    code = """
def hello():
    print("Hello")
    x = 1
    """
    
    print("=== AI代码审查测试 ===\n")
    result = reviewer.review(code)
    print(f"评分: {result['score']}")
    print(f"问题: {result['issues']}")
