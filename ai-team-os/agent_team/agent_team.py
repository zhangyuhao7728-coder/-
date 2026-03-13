#!/usr/bin/env python3
"""
Agent Team - 多Agent协作团队
功能：
1. 多种角色Agent
2. 协作流程
3. 结果汇总
"""
from typing import Dict, List, Optional
from enum import Enum


class AgentRole(Enum):
    """Agent角色"""
    PLANNER = "planner"      # 规划者
    RESEARCHER = "researcher" # 研究者
    CODER = "coder"          # 编码者
    REVIEWER = "reviewer"    # 审核者
    ANALYST = "analyst"      # 分析师
    CEO = "ceo"             # 决策者


class Agent:
    """Agent"""
    
    def __init__(self, role: AgentRole, model: str = "qwen3.5:9b"):
        self.role = role
        self.model = model
        self.name = role.value.capitalize()
        self.tasks_completed = 0
    
    def execute(self, task: str) -> str:
        """执行任务"""
        self.tasks_completed += 1
        
        # 根据角色执行不同任务
        if self.role == AgentRole.PLANNER:
            return self._plan(task)
        elif self.role == AgentRole.RESEARCHER:
            return self._research(task)
        elif self.role == AgentRole.CODER:
            return self._code(task)
        elif self.role == AgentRole.REVIEWER:
            return self._review(task)
        elif self.role == AgentRole.ANALYST:
            return self._analyze(task)
        elif self.role == AgentRole.CEO:
            return self._decide(task)
        
        return f"[{self.name}] 处理: {task}"
    
    def _plan(self, task: str) -> str:
        return f"[Planner] 规划任务: {task}"
    
    def _research(self, task: str) -> str:
        return f"[Researcher] 调研: {task}"
    
    def _code(self, task: str) -> str:
        return f"[Coder] 编写代码: {task}"
    
    def _review(self, task: str) -> str:
        return f"[Reviewer] 审核: {task}"
    
    def _analyze(self, task: str) -> str:
        return f"[Analyst] 分析: {task}"
    
    def _decide(self, task: str) -> str:
        return f"[CEO] 决策: {task}"
    
    def to_dict(self) -> Dict:
        return {
            "role": self.role.value,
            "name": self.name,
            "model": self.model,
            "tasks_completed": self.tasks_completed,
        }


class AgentTeam:
    """Agent团队"""
    
    def __init__(self):
        # 初始化团队成员
        self.agents = {
            AgentRole.PLANNER: Agent(AgentRole.PLANNER, "qwen3.5:9b"),
            AgentRole.RESEARCHER: Agent(AgentRole.RESEARCHER, "qwen2.5:14b"),
            AgentRole.CODER: Agent(AgentRole.CODER, "deepseek-coder:6.7b"),
            AgentRole.REVIEWER: Agent(AgentRole.REVIEWER, "qwen3.5:9b"),
            AgentRole.ANALYST: Agent(AgentRole.ANALYST, "qwen2.5:14b"),
            AgentRole.CEO: Agent(AgentRole.CEO, "qwen3.5:9b"),
        }
        
        self.workflow_results = []
    
    def execute_workflow(self, task: str) -> Dict:
        """执行完整工作流"""
        results = {}
        
        # 1. Planner 规划
        planner = self.agents[AgentRole.PLANNER]
        results["plan"] = planner.execute(task)
        
        # 2. Researcher 调研
        researcher = self.agents[AgentRole.RESEARCHER]
        results["research"] = researcher.execute(task)
        
        # 3. Coder 编码
        coder = self.agents[AgentRole.CODER]
        results["code"] = coder.execute(task)
        
        # 4. Reviewer 审核
        reviewer = self.agents[AgentRole.REVIEWER]
        results["review"] = reviewer.execute(task)
        
        # 5. Analyst 分析
        analyst = self.agents[AgentRole.ANALYST]
        results["analysis"] = analyst.execute(task)
        
        # 6. CEO 决策
        ceo = self.agents[AgentRole.CEO]
        results["decision"] = ceo.execute(task)
        
        self.workflow_results.append({
            "task": task,
            "results": results,
        })
        
        return results
    
    def execute_simple(self, task: str, role: AgentRole = None) -> str:
        """执行简单任务"""
        if role:
            agent = self.agents.get(role)
            if agent:
                return agent.execute(task)
        
        # 根据任务类型自动选择
        task_lower = task.lower()
        
        if "代码" in task or "写" in task or "python" in task_lower:
            return self.agents[AgentRole.CODER].execute(task)
        elif "分析" in task or "比较" in task:
            return self.agents[AgentRole.ANALYST].execute(task)
        elif "调研" in task or "查" in task:
            return self.agents[AgentRole.RESEARCHER].execute(task)
        elif "计划" in task or "规划" in task:
            return self.agents[AgentRole.PLANNER].execute(task)
        else:
            return self.agents[AgentRole.CODER].execute(task)
    
    def get_team_status(self) -> List[Dict]:
        """获取团队状态"""
        return [agent.to_dict() for agent in self.agents.values()]


# 全局实例
_team = None

def get_agent_team() -> AgentTeam:
    global _team
    if _team is None:
        _team = AgentTeam()
    return _team


# 测试
if __name__ == "__main__":
    team = get_agent_team()
    
    print("=== Agent Team 测试 ===\n")
    
    # 简单任务
    result = team.execute_simple("写一个Python函数")
    print(f"简单任务: {result}\n")
    
    # 工作流
    print("完整工作流:")
    results = team.execute_workflow("开发一个Web应用")
    
    for step, result in results.items():
        print(f"  {step}: {result}")
    
    print("\n团队状态:")
    for agent in team.get_team_status():
        print(f"  {agent['name']}: {agent['tasks_completed']} 任务")
