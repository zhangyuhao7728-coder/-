#!/usr/bin/env python3
"""
Base Agent - Agent基类
所有Agent继承它
"""
from typing import Dict, Optional


class BaseAgent:
    """Agent基类"""
    
    def __init__(self, name: str, role: str, model: str = "qwen3.5:9b"):
        self.name = name
        self.role = role
        self.model = model
        self.tasks_completed = 0
        self.success_count = 0
        self.fail_count = 0
        self.router = None
    
    def set_router(self, router):
        """设置路由器"""
        self.router = router
    
    def think(self, prompt: str) -> str:
        """思考 - 调用LLM"""
        if self.router:
            response = self.router.route(self.role, prompt)
            return response
        return f"[{self.name}] No router configured"
    
    def execute(self, task: str) -> Dict:
        """执行任务"""
        self.tasks_completed += 1
        
        try:
            result = self.think(task)
            self.success_count += 1
            return {
                "success": True,
                "result": result,
                "agent": self.name,
            }
        except Exception as e:
            self.fail_count += 1
            return {
                "success": False,
                "error": str(e),
                "agent": self.name,
            }
    
    def get_stats(self) -> Dict:
        return {
            "name": self.name,
            "role": self.role,
            "model": self.model,
            "tasks_completed": self.tasks_completed,
            "success": self.success_count,
            "fail": self.fail_count,
        }
    
    def __repr__(self):
        return f"<Agent {self.name} ({self.role})>"


# 具体Agent类

class CEOAgent(BaseAgent):
    """CEO Agent - 决策者"""
    
    def __init__(self):
        super().__init__("CEO", "决策者", "qwen3.5:9b")
    
    def decide(self, task: str, context: Dict = None) -> str:
        """做决策"""
        return f"[CEO] 决策: 批准{task}"


class PlannerAgent(BaseAgent):
    """Planner Agent - 规划者"""
    
    def __init__(self):
        super().__init__("Planner", "规划者", "qwen3.5:9b")
    
    def plan(self, task: str) -> str:
        """制定计划"""
        return f"[Planner] 计划: 拆解{task}为多个子任务"


class ResearcherAgent(BaseAgent):
    """Researcher Agent - 研究者"""
    
    def __init__(self):
        super().__init__("Researcher", "研究者", "qwen2.5:14b")
    
    def research(self, topic: str) -> str:
        """研究"""
        return f"[Researcher] 调研: {topic}"


class CoderAgent(BaseAgent):
    """Coder Agent - 编码者"""
    
    def __init__(self):
        super().__init__("Coder", "编码者", "deepseek-coder:6.7b")
    
    def code(self, task: str) -> str:
        """编写代码"""
        return f"[Coder] 编写: {task}"


class ReviewerAgent(BaseAgent):
    """Reviewer Agent - 审核者"""
    
    def __init__(self):
        super().__init__("Reviewer", "审核者", "qwen3.5:9b")
    
    def review(self, content: str) -> str:
        """审核"""
        return f"[Reviewer] 审核: {content}"


class AnalystAgent(BaseAgent):
    """Analyst Agent - 分析师"""
    
    def __init__(self):
        super().__init__("Analyst", "分析师", "qwen2.5:14b")
    
    def analyze(self, data: str) -> str:
        """分析"""
        return f"[Analyst] 分析: {data}"


# 测试
if __name__ == "__main__":
    print("=== Base Agent 测试 ===\n")
    
    # 创建Agent
    ceo = CEOAgent()
    planner = PlannerAgent()
    coder = CoderAgent()
    
    # 执行
    print(f"创建: {ceo}")
    result = ceo.execute("开发新功能")
    print(f"结果: {result}")
    
    print(f"\n创建: {coder}")
    result = coder.execute("写一个函数")
    print(f"结果: {result}")
    
    # 统计
    print("\n统计:")
    for agent in [ceo, planner, coder]:
        print(f"  {agent.name}: {agent.tasks_completed} 任务")
