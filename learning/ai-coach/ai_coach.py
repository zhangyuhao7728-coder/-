#!/usr/bin/env python3
"""
AI Coach - AI学习助手
功能：解释概念、生成练习、发现错误、提供提示
"""
import requests
from typing import Dict, List


class AICoach:
    """AI学习助手"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        self.model = "qwen2.5:14b"  # 分析用较强模型
    
    def call_llm(self, prompt: str) -> str:
        """调用LLM"""
        try:
            resp = requests.post(
                f"{self.ollama_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=60
            )
            
            if resp.status_code == 200:
                return resp.json().get("response", "")
        except:
            pass
        
        return "AI暂时无法回答，请检查模型服务"
    
    # ===== 1. 解释概念 =====
    
    def explain(self, topic: str) -> str:
        """用简单方式解释概念"""
        prompt = f"""你是一个Python老师。用简单易懂的方式解释以下概念：

{topic}

要求：
- 用生活中的例子说明
- 给出代码示例
- 控制在100字内
"""
        return self.call_llm(prompt)
    
    # ===== 2. 生成练习 =====
    
    def generate_exercise(self, topic: str, difficulty: str = "easy") -> Dict:
        """生成练习题"""
        prompt = f"""生成一道{difficulty}难度的Python练习题，主题是{topic}。

返回格式：
题目：[题目内容]
答案：[答案代码]
提示：[给初学者的提示]
"""
        result = self.call_llm(prompt)
        
        # 简单解析
        lines = result.split("\n")
        exercise = {
            "topic": topic,
            "difficulty": difficulty,
            "question": "",
            "answer": "",
            "hint": ""
        }
        
        for line in lines:
            if "题目" in line:
                exercise["question"] = line.split("：")[-1].strip()
            elif "答案" in line:
                exercise["answer"] = line.split("：")[-1].strip()
            elif "提示" in line:
                exercise["hint"] = line.split("：")[-1].strip()
        
        if not exercise["question"]:
            exercise["question"] = f"请用Python实现{topic}"
        
        return exercise
    
    # ===== 3. 发现错误 =====
    
    def find_errors(self, code: str) -> List[str]:
        """发现代码中的错误"""
        prompt = f"""分析以下Python代码，找出其中的错误或问题：

```python
{code}
```

返回格式：
问题1：[描述]
问题2：[描述]
"""
        result = self.call_llm(prompt)
        
        # 解析错误
        errors = []
        for line in result.split("\n"):
            if "问题" in line or "错误" in line or "Bug" in line.upper():
                errors.append(line)
        
        return errors if errors else ["代码看起来没有明显错误"]
    
    # ===== 4. 提供提示 =====
    
    def give_hint(self, problem: str, attempt: str = None) -> str:
        """给提示"""
        prompt = f"""用户在做这道题：
{problem}
"""
        
        if attempt:
            prompt += f"用户的尝试：\n{attempt}\n"
        
        prompt += """
给出一个有用的提示，帮助用户自己解决问题。
提示要具体但不要直接给出答案。
"""
        return self.call_llm(prompt)
    
    # ===== 5. 代码审查 =====
    
    def review_code(self, code: str) -> str:
        """审查代码并给出改进建议"""
        prompt = f"""你是一个资深Python开发者。审查以下代码：

```python
{code}
```

从以下方面给出评价：
1. 代码正确性
2. 代码风格
3. 性能优化
4. 可能的bug
"""
        return self.call_llm(prompt)
    
    # ===== 6. 回答问题 =====
    
    def answer(self, question: str) -> str:
        """回答学习相关问题"""
        prompt = f"""你是一个Python学习助手。简短回答这个问题：

{question}
"""
        return self.call_llm(prompt)
    
    # ===== 7. 生成学习计划 =====
    
    def create_plan(self, goal: str, days: int = 7) -> str:
        """生成学习计划"""
        prompt = f"""为一个想学习{goal}的初学者，生成一个{days}天的学习计划。

每天包含：
- 学习主题
- 练习任务
- 目标

格式清晰简洁。
"""
        return self.call_llm(prompt)
    
    # ===== 8. 调试代码 =====
    
    def debug(self, code: str, error: str) -> str:
        """调试代码"""
        prompt = f"""用户的Python代码出错了：

错误信息：{error}

代码：
```python
{code}
```

分析错误原因并给出修复方案。
"""
        return self.call_llm(prompt)


# 全局实例
_coach = None

def get_ai_coach() -> AICoach:
    global _coach
    if _coach is None:
        _coach = AICoach()
    return _coach


# 便捷函数
def explain(topic: str) -> str:
    return get_ai_coach().explain(topic)

def review_code(code: str) -> str:
    return get_ai_coach().review_code(code)

def answer(question: str) -> str:
    return get_ai_coach().answer(question)


# 测试
if __name__ == "__main__":
    coach = get_ai_coach()
    
    print("=== AI Coach 测试 ===\n")
    
    # 测试解释
    print("1. 解释概念:")
    result = coach.explain("什么是变量")
    print(result[:100])
