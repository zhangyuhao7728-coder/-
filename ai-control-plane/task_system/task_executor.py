#!/usr/bin/env python3
"""
Task Executor - 任务执行器
自动选择Agent + 自动选择模型
"""
from typing import Dict, List
import requests


class SimpleRouter:
    """简单路由器 - 自动选择模型"""
    
    # 任务类型 -> 模型映射
    TASK_MODELS = {
        "coder": "deepseek-coder:6.7b",
        "researcher": "qwen2.5:14b",
        "analyst": "qwen2.5:14b",
        "planner": "qwen3.5:9b",
        "reviewer": "qwen3.5:9b",
        "general": "qwen2.5:latest",
    }
    
    def route(self, agent_type: str, prompt: str) -> str:
        """自动选择模型"""
        model = self.TASK_MODELS.get(agent_type, "qwen2.5:latest")
        
        # 调用Ollama
        try:
            resp = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=60
            )
            
            if resp.status_code == 200:
                return resp.json().get("response", "")
        except:
            pass
        
        return f"[{model}] 处理: {prompt}"


class TaskExecutor:
    """任务执行器"""
    
    def __init__(self):
        self.router = SimpleRouter()
        self.tasks = {}
    
    def assign_agent(self, subtask):
        """自动选择Agent"""
        agent_type = subtask.get("agent_type", "general")
        
        # 根据agent_type返回处理函数
        return Agent(agent_type, self.router)
    
    def execute(self, task: Dict) -> Dict:
        """
        执行任务
        
        自动流程：
        1. 拆解任务 (如果需要)
        2. 自动选择Agent
        3. Agent自动选择模型
        4. 执行并汇总结果
        """
        goal = task.get("goal", "")
        subtasks = task.get("subtasks", [])
        
        print(f"\n{'='*50}")
        print(f"📋 任务: {goal}")
        print(f"{'='*50}\n")
        
        # 如果没有子任务，自动拆解
        if not subtasks:
            subtasks = self._auto_decompose(goal)
        
        # 执行每个子任务
        results = []
        
        for i, subtask in enumerate(subtasks, 1):
            print(f"🔄 执行 {i}/{len(subtasks)}: {subtask.get('description', subtask)}")
            
            # 自动选择Agent
            agent_type = subtask.get("agent_type", "general")
            agent = Agent(agent_type, self.router)
            
            # Agent自动选择模型并执行
            result = agent.think(subtask.get("description", str(subtask)))
            
            print(f"   ✅ 完成\n")
            
            results.append({
                "step": i,
                "description": subtask.get("description", str(subtask)),
                "agent": agent_type,
                "model": agent.model,
                "result": result[:100] + "..." if len(result) > 100 else result,
            })
        
        # 汇总
        summary = self._summarize(results)
        
        return {
            "goal": goal,
            "subtasks": len(subtasks),
            "results": results,
            "summary": summary,
        }
    
    def _auto_decompose(self, goal: str) -> List[Dict]:
        """自动拆解任务"""
        subtasks = []
        
        # 简单基于关键词的拆解
        if "和" in goal:
            parts = goal.split("和")
            for part in parts:
                part = part.strip()
                agent_type = self._guess_agent(part)
                subtasks.append({
                    "description": part,
                    "agent_type": agent_type,
                })
        else:
            agent_type = self._guess_agent(goal)
            subtasks.append({
                "description": goal,
                "agent_type": agent_type,
            })
        
        return subtasks
    
    def _guess_agent(self, task: str) -> str:
        """猜测Agent类型"""
        task_lower = task.lower()
        
        if any(kw in task_lower for kw in ["写", "代码", "python", "开发", "程序"]):
            return "coder"
        elif any(kw in task_lower for kw in ["研究", "调研", "查", "搜索"]):
            return "researcher"
        elif any(kw in task_lower for kw in ["分析", "比较", "评估"]):
            return "analyst"
        elif any(kw in task_lower for kw in ["审查", "检查", "审核"]):
            return "reviewer"
        elif any(kw in task_lower for kw in ["计划", "规划", "拆解"]):
            return "planner"
        else:
            return "general"
    
    def _summarize(self, results: List[Dict]) -> str:
        """汇总结果"""
        summary = f"\n{'='*50}\n"
        summary += "✅ 任务执行完成\n"
        summary += f"{'='*50}\n\n"
        
        for r in results:
            summary += f"• {r['description']}\n"
            summary += f"  Agent: {r['agent']} | Model: {r['model']}\n"
        
        summary += f"\n总计: {len(results)} 个步骤"
        
        return summary


class Agent:
    """Agent - 自动选择模型"""
    
    # 任务类型 -> 模型
    MODEL_MAP = {
        "coder": "deepseek-coder:6.7b",     # 代码
        "researcher": "qwen2.5:14b",       # 研究
        "analyst": "qwen2.5:14b",           # 分析
        "planner": "qwen3.5:9b",            # 规划
        "reviewer": "qwen3.5:9b",            # 审核
        "general": "qwen2.5:latest",         # 通用
    }
    
    def __init__(self, agent_type: str, router: SimpleRouter = None):
        self.agent_type = agent_type
        self.model = self.MODEL_MAP.get(agent_type, "qwen2.5:latest")
        self.router = router or SimpleRouter()
    
    def think(self, prompt: str) -> str:
        """思考 - 自动选择模型并执行"""
        # 自动选择模型
        model = self.MODEL_MAP.get(self.agent_type, "qwen2.5:latest")
        
        # 调用模型
        try:
            resp = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=60
            )
            
            if resp.status_code == 200:
                return resp.json().get("response", "")
        except:
            pass
        
        return f"[{self.agent_type}] 处理: {prompt}"


# 测试
if __name__ == "__main__":
    print("=== Task Executor 测试 ===\n")
    
    executor = TaskExecutor()
    
    # 测试1: 简单任务
    task1 = {
        "goal": "写一个Python爬虫",
    }
    
    result = executor.execute(task1)
    print(result["summary"])
