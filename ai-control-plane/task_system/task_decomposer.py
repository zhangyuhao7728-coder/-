#!/usr/bin/env python3
"""
Task Decomposer - 任务拆解器
将任务拆解为子任务列表
"""
import requests
from typing import List


class TaskDecomposer:
    """任务拆解器"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
    
    def decompose_task(self, goal: str) -> List[dict]:
        """
        拆解任务
        
        示例：
        任务：写一个网页爬虫
        拆解：
        1. 研究网站结构 (researcher)
        2. 编写爬虫代码 (coder)
        3. 测试爬虫 (tester)
        4. 优化性能 (analyst)
        """
        # 构建Prompt
        prompt = self._build_prompt(goal)
        
        # 调用LLM
        steps = self._call_llm(prompt)
        
        # 解析结果
        subtasks = self._parse_steps(steps, goal)
        
        return subtasks
    
    def _build_prompt(self, goal: str) -> str:
        """构建Prompt"""
        return f"""将以下任务拆解为具体步骤，返回JSON数组格式：
任务：{goal}

要求：
1. 每个步骤描述要简洁
2. 标注合适的Agent类型 (coder/researcher/reviewer/analyst)
3. 最多5个步骤

返回格式示例：
[{{"description": "步骤描述", "agent_type": "coder"}}]"""

    def _call_llm(self, prompt: str) -> str:
        """调用LLM"""
        try:
            resp = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "qwen2.5:14b",
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=30
            )
            
            if resp.status_code == 200:
                return resp.json().get("response", "")
        except:
            pass
        
        # 失败则返回默认拆解
        return self._default_decompose(goal)
    
    def _parse_steps(self, response: str, goal: str) -> List[dict]:
        """解析步骤"""
        import json
        
        # 尝试提取JSON
        try:
            # 查找JSON数组
            import re
            match = re.search(r'\[.*\]', response, re.DOTALL)
            if match:
                steps = json.loads(match.group())
                return steps
        except:
            pass
        
        # 默认拆解
        return self._default_decompose(goal)
    
    def _default_decompose(self, goal: str) -> List[dict]:
        """默认拆解"""
        # 简单基于关键词的拆解
        subtasks = []
        
        if "写" in goal or "开发" in goal or "创建" in goal:
            subtasks.append({"description": "理解任务需求", "agent_type": "planner"})
            subtasks.append({"description": goal, "agent_type": "coder"})
            subtasks.append({"description": "审查代码", "agent_type": "reviewer"})
        elif "分析" in goal or "调研" in goal:
            subtasks.append({"description": "收集信息", "agent_type": "researcher"})
            subtasks.append({"description": "分析数据", "agent_type": "analyst"})
        else:
            subtasks.append({"description": goal, "agent_type": "general"})
        
        return subtasks
    
    def quick_decompose(self, goal: str) -> List[dict]:
        """快速拆解 (无需LLM)"""
        # 基于关键词的快速拆解
        subtasks = []
        
        # 常见模式
        if "和" in goal:
            parts = goal.split("和")
            for part in parts:
                part = part.strip()
                if part:
                    agent = self._guess_agent(part)
                    subtasks.append({"description": part, "agent_type": agent})
        else:
            # 默认步骤
            subtasks.append({"description": f"执行: {goal}", "agent_type": self._guess_agent(goal)})
        
        return subtasks
    
    def _guess_agent(self, task: str) -> str:
        """猜测Agent类型"""
        task_lower = task.lower()
        
        if any(kw in task_lower for kw in ["写", "代码", "python", "程序", "开发"]):
            return "coder"
        elif any(kw in task_lower for kw in ["研究", "调研", "查", "搜索"]):
            return "researcher"
        elif any(kw in task_lower for kw in ["分析", "比较", "评估"]):
            return "analyst"
        elif any(kw in task_lower for kw in ["审查", "检查", "审核"]):
            return "reviewer"
        else:
            return "general"


# 测试
if __name__ == "__main__":
    decomposer = TaskDecomposer()
    
    print("=== Task Decomposer 测试 ===\n")
    
    # 测试
    tasks = [
        "写一个网页爬虫",
        "开发一个Web应用并测试",
        "分析这个代码的性能",
    ]
    
    for goal in tasks:
        print(f"任务: {goal}")
        
        # 快速拆解
        subtasks = decomposer.quick_decompose(goal)
        
        print("拆解:")
        for i, st in enumerate(subtasks, 1):
            print(f"  {i}. {st['description']} ({st['agent_type']})")
        print()
