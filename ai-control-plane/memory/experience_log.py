#!/usr/bin/env python3
"""
Experience Log - 经验日志
记录任务执行经验
"""
import json
from datetime import datetime
from typing import Dict, List


class ExperienceLog:
    """经验日志"""
    
    def __init__(self):
        self.experiences = []
        self.max_size = 1000
    
    def log_task(self, task: str, agent: str, model: str, 
                 result: str, success: bool, duration: float = 0):
        """记录任务经验"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "agent": agent,
            "model": model,
            "result": result[:200] if result else "",
            "success": success,
            "duration": duration,
        }
        
        self.experiences.append(entry)
        
        # 保持大小
        if len(self.experiences) > self.max_size:
            self.experiences.pop(0)
    
    def log_success(self, task: str, agent: str, model: str, result: str):
        """记录成功"""
        self.log_task(task, agent, model, result, True)
    
    def log_failure(self, task: str, agent: str, model: str, error: str):
        """记录失败"""
        self.log_task(task, agent, model, error, False)
    
    def get_recent(self, n: int = 10) -> List[Dict]:
        """获取最近经验"""
        return self.experiences[-n:]
    
    def get_success_rate(self, agent: str = None) -> float:
        """获取成功率"""
        if agent:
            filtered = [e for e in self.experiences if e.get("agent") == agent]
        else:
            filtered = self.experiences
        
        if not filtered:
            return 0
        
        success = sum(1 for e in filtered if e.get("success"))
        return success / len(filtered) * 100
    
    def get_best_model(self, agent: str) -> str:
        """获取最佳模型"""
        agent_exp = [e for e in self.experiences if e.get("agent") == agent]
        
        if not agent_exp:
            return "unknown"
        
        # 统计每个模型的成功率
        models = {}
        for e in agent_exp:
            model = e.get("model", "unknown")
            if model not in models:
                models[model] = {"success": 0, "total": 0}
            
            models[model]["total"] += 1
            if e.get("success"):
                models[model]["success"] += 1
        
        # 返回成功率最高的
        best = max(models.items(), 
                   key=lambda x: x[1]["success"]/x[1]["total"] if x[1]["total"] > 0 else 0)
        
        return best[0]
    
    def get_stats(self) -> Dict:
        """获取统计"""
        total = len(self.experiences)
        success = sum(1 for e in self.experiences if e.get("success"))
        
        return {
            "total": total,
            "success": success,
            "failure": total - success,
            "success_rate": (success / total * 100) if total > 0 else 0,
        }
    
    def print_stats(self):
        """打印统计"""
        stats = self.get_stats()
        
        print("="*50)
        print("      Experience Log")
        print("="*50)
        print(f"总经验: {stats['total']}")
        print(f"成功: {stats['success']}")
        print(f"失败: {stats['failure']}")
        print(f"成功率: {stats['success_rate']:.1f}%")
        
        # 按Agent统计
        agents = set(e.get("agent") for e in self.experiences)
        if agents:
            print("\n按Agent:")
            for agent in agents:
                rate = self.get_success_rate(agent)
                best = self.get_best_model(agent)
                print(f"  {agent}: {rate:.1f}% (最佳: {best})")
        
        print("="*50)


# 全局实例
_log = None

def get_experience_log() -> ExperienceLog:
    global _log
    if _log is None:
        _log = ExperienceLog()
    return _log
