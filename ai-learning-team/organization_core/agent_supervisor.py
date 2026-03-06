"""
Agent Supervisor
解决 Agent 死循环、任务卡死、多 Agent 互相等待问题
"""

import time
import threading
from collections import defaultdict
from typing import Dict, Optional, Any
from datetime import datetime, timedelta


class AgentSupervisor:
    """Agent 监督器 - 防止死循环和卡死"""
    
    # 配置
    MAX_LOOP_COUNT = 5        # 最大循环次数
    MAX_WAIT_TIME = 30        # 最大等待时间 (秒)
    TASK_TIMEOUT = 120        # 任务超时 (秒)
    MAX_RECURSIVE_CALLS = 3   # 最大递归调用深度
    
    def __init__(self):
        # Agent 循环计数
        self.loop_counts = defaultdict(int)
        
        # Agent 最后活跃时间
        self.last_active = defaultdict(float)
        
        # 任务状态
        self.task_status = {}  # {task_id: {state, start_time, agent}}
        
        # Agent 等待关系图 (检测死锁)
        self.waiting_for = {}  # {agent: waiting_for_agent}
        
        # 死锁检测
        self.deadlock_detected = False
        
        self.lock = threading.Lock()
    
    # ===== 循环检测 =====
    
    def check_loop(self, agent: str, action: str) -> bool:
        """
        检查是否陷入循环
        
        Returns:
            True if loop detected (should stop)
        """
        with self.lock:
            key = f"{agent}:{action}"
            self.loop_counts[key] += 1
            
            if self.loop_counts[key] > self.MAX_LOOP_COUNT:
                print(f"⚠️ Loop detected: {agent} repeating '{action}' ({self.loop_counts[key]} times)")
                return True
            
            return False
    
    def reset_loop(self, agent: str, action: str = None):
        """重置循环计数"""
        with self.lock:
            if action:
                key = f"{agent}:{action}"
                if key in self.loop_counts:
                    del self.loop_counts[key]
            else:
                # 重置该 Agent 所有计数
                keys_to_remove = [k for k in self.loop_counts.keys() if k.startswith(f"{agent}:")]
                for k in keys_to_remove:
                    del self.loop_counts[k]
    
    # ===== 任务超时 =====
    
    def start_task(self, task_id: str, agent: str):
        """开始任务"""
        with self.lock:
            self.task_status[task_id] = {
                "agent": agent,
                "state": "RUNNING",
                "start_time": time.time(),
                "loop_count": 0
            }
            self.last_active[agent] = time.time()
    
    def check_task_timeout(self, task_id: str) -> bool:
        """检查任务是否超时"""
        with self.lock:
            if task_id not in self.task_status:
                return False
            
            task = self.task_status[task_id]
            elapsed = time.time() - task["start_time"]
            
            if elapsed > self.TASK_TIMEOUT:
                print(f"⏱️ Task {task_id} timeout ({elapsed:.1f}s)")
                task["state"] = "TIMEOUT"
                return True
            
            return False
    
    def finish_task(self, task_id: str):
        """完成任务"""
        with self.lock:
            if task_id in self.task_status:
                del self.task_status[task_id]
    
    # ===== Agent 活跃检测 =====
    
    def ping(self, agent: str):
        """Agent 活跃信号"""
        self.last_active[agent] = time.time()
    
    def is_agent_stuck(self, agent: str) -> bool:
        """检查 Agent 是否卡死"""
        with self.lock:
            if agent not in self.last_active:
                return False
            
            elapsed = time.time() - self.last_active[agent]
            return elapsed > self.MAX_WAIT_TIME
    
    def get_stuck_agents(self) -> list:
        """获取所有卡死的 Agent"""
        stuck = []
        with self.lock:
            for agent, last_time in self.last_active.items():
                if time.time() - last_time > self.MAX_WAIT_TIME:
                    stuck.append(agent)
        return stuck
    
    # ===== 死锁检测 (多 Agent 互相等待) =====
    
    def wait_for(self, agent: str, other_agent: str):
        """记录 Agent 等待关系"""
        with self.lock:
            self.waiting_for[agent] = other_agent
            print(f"⏳ {agent} waiting for {other_agent}")
    
    def clear_wait(self, agent: str):
        """清除等待关系"""
        with self.lock:
            if agent in self.waiting_for:
                del self.waiting_for[agent]
    
    def check_deadlock(self) -> Optional[Dict]:
        """
        检测死锁
        
        Returns:
            死锁信息或 None
        """
        with self.lock:
            # 检测循环等待
            visited = set()
            path = []
            
            def dfs(agent: str) -> bool:
                if agent in path:
                    # 发现循环
                    cycle_start = path.index(agent)
                    cycle = path[cycle_start:] + [agent]
                    return {
                        "type": "DEADLOCK",
                        "cycle": cycle,
                        "agents": list(set(cycle))
                    }
                
                if agent in visited:
                    return None
                
                visited.add(agent)
                path.append(agent)
                
                if agent in self.waiting_for:
                    next_agent = self.waiting_for[agent]
                    result = dfs(next_agent)
                    if result:
                        return result
                
                path.pop()
                return None
            
            # 检查所有 Agent
            for agent in self.waiting_for.keys():
                result = dfs(agent)
                if result:
                    self.deadlock_detected = True
                    print(f"🚨 DEADLOCK detected: {result['cycle']}")
                    return result
            
            return None
    
    # ===== 恢复机制 =====
    
    def recover_from_deadlock(self) -> Dict:
        """从死锁恢复"""
        print("🔄 Recovering from deadlock...")
        
        with self.lock:
            # 强制解除所有等待关系
            self.waiting_for.clear()
            self.deadlock_detected = False
            
            # 重置所有循环计数
            self.loop_counts.clear()
        
        return {"status": "recovered", "action": "cleared_waiting_graph"}
    
    def recover_stuck_agent(self, agent: str) -> Dict:
        """恢复卡死的 Agent"""
        print(f"🔄 Recovering stuck agent: {agent}")
        
        with self.lock:
            # 重置该 Agent 的循环计数
            keys_to_remove = [k for k in self.loop_counts.keys() if k.startswith(f"{agent}:")]
            for k in keys_to_remove:
                del self.loop_counts[k]
            
            # 清除等待关系
            if agent in self.waiting_for:
                del self.waiting_for[agent]
        
        return {"status": "recovered", "agent": agent}
    
    # ===== 状态报告 =====
    
    def get_status(self) -> Dict:
        """获取监督状态"""
        with self.lock:
            return {
                "loop_counts": dict(self.loop_counts),
                "active_tasks": len(self.task_status),
                "waiting_pairs": len(self.waiting_for),
                "stuck_agents": self.get_stuck_agents(),
                "deadlock_detected": self.deadlock_detected
            }


# 全局实例
_supervisor = None


def get_supervisor() -> AgentSupervisor:
    """获取监督器实例"""
    global _supervisor
    if _supervisor is None:
        _supervisor = AgentSupervisor()
    return _supervisor
