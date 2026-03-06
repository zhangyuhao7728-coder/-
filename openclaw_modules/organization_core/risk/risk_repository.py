"""
Risk Repository
风险事件仓储 - SQLite 持久化版
"""

import time
from collections import defaultdict
from typing import List, Dict, Optional
from datetime import datetime, timedelta


class RiskRepository:
    """风险事件仓储 - 支持 SQLite 持久化"""
    
    def __init__(self, db=None):
        # 内存缓存 (用于快速查询)
        self.events = defaultdict(list)  # {agent: [events]}
        self.cooldowns = {}  # {agent: unblock_time} - 内存缓存
        self.org_events = []  # 组织级事件
        
        # SQLite 数据库连接
        self.db = db
        self._load_from_db()
    
    def _load_from_db(self):
        """从数据库加载数据"""
        if not self.db:
            return
        
        # 加载事件 (最近7天)
        try:
            import sqlite3
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # 加载 Override 事件
            cursor.execute("""
                SELECT agent_name, date, COUNT(*) as count
                FROM overrides
                WHERE date >= date('now', '-7 days')
                GROUP BY agent_name, date
            """)
            for row in cursor.fetchall():
                agent, date, count = row
                for _ in range(count):
                    self.events[agent].append({
                        "type": "override",
                        "value": 1.0,
                        "timestamp": time.time(),  # 简化处理
                        "datetime": date
                    })
            
            # 加载 Cost 事件
            cursor.execute("""
                SELECT agent_name, date, SUM(cost) as total
                FROM cost_tracking
                WHERE date >= date('now', '-7 days')
                GROUP BY agent_name, date
            """)
            for row in cursor.fetchall():
                agent, date, total = row
                self.events[agent].append({
                    "type": "cost",
                    "value": total,
                    "timestamp": time.time(),
                    "datetime": date
                })
            
            conn.close()
        except Exception as e:
            print(f"Warning: Failed to load from DB: {e}")
    
    def record_event(self, agent: str, event_type: str, value: float = 1.0):
        """记录风险事件"""
        event = {
            "type": event_type,
            "value": value,
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat()
        }
        self.events[agent].append(event)
        
        # 持久化到数据库
        if self.db:
            if event_type == "override":
                self.db.insert_override(agent)
            elif event_type == "cost":
                self.db.insert_cost(agent, value)
        
        # 清理超过7天的事件
        self._cleanup_old_events(agent)
    
    def _cleanup_old_events(self, agent: str, days: int = 7):
        """清理旧事件"""
        cutoff = time.time() - (days * 86400)
        self.events[agent] = [
            e for e in self.events[agent]
            if e["timestamp"] > cutoff
        ]
    
    def get_recent_events(self, agent: str, seconds: int = 86400) -> List[Dict]:
        """获取最近事件（默认24小时）"""
        now = time.time()
        return [
            e for e in self.events.get(agent, [])
            if now - e["timestamp"] <= seconds
        ]
    
    def get_event_count(self, agent: str, event_type: str = None, seconds: int = 86400) -> int:
        """获取事件数量"""
        events = self.get_recent_events(agent, seconds)
        if event_type:
            return sum(1 for e in events if e["type"] == event_type)
        return len(events)
    
    def get_total_cost(self, agent: str, seconds: int = 86400) -> float:
        """获取总成本"""
        events = self.get_recent_events(agent, seconds)
        return sum(e["value"] for e in events if e["type"] == "cost")
    
    # ===== 持久化冷却 =====
    
    def set_cooldown(self, agent: str, duration_seconds: int, level: str = "CRITICAL", reason: str = ""):
        """设置冷却时间 (持久化)"""
        unblock_time = time.time() + duration_seconds
        
        # 内存
        self.cooldowns[agent] = unblock_time
        
        # 持久化到数据库
        if self.db:
            self.db.set_cooldown(agent, unblock_time, level, reason)
    
    def clear_cooldown(self, agent: str):
        """清除冷却"""
        if agent in self.cooldowns:
            del self.cooldowns[agent]
        
        if self.db:
            self.db.clear_cooldown(agent)
    
    def is_blocked(self, agent: str) -> bool:
        """检查是否被封锁 (优先从数据库检查)"""
        # 先检查数据库
        if self.db:
            if self.db.is_agent_locked(agent):
                return True
        
        # 再检查内存
        if agent not in self.cooldowns:
            return False
        return time.time() < self.cooldowns[agent]
    
    def get_cooldown_remaining(self, agent: str) -> int:
        """获取剩余冷却时间（秒）"""
        # 优先从数据库获取
        if self.db:
            cooldown = self.db.get_cooldown(agent)
            if cooldown:
                remaining = cooldown["unblock_time"] - time.time()
                return max(0, int(remaining))
        
        # 内存备用
        if agent not in self.cooldowns:
            return 0
        remaining = self.cooldowns[agent] - time.time()
        return max(0, int(remaining))
    
    # ===== 组织级风险 =====
    
    def record_org_event(self, event_type: str, value: float = 0):
        """记录组织级事件"""
        event = {
            "type": event_type,
            "value": value,
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat()
        }
        self.org_events.append(event)
    
    def get_org_risk_level(self) -> Optional[str]:
        """获取组织级风险等级"""
        now = time.time()
        today_events = [
            e for e in self.org_events
            if now - e["timestamp"] <= 86400
        ]
        
        total_cost = sum(e["value"] for e in today_events if e["type"] == "cost")
        
        # 组织级预算阈值
        ORG_BUDGET = 100.0
        
        if total_cost >= ORG_BUDGET * 2:
            return "CRITICAL"
        if total_cost >= ORG_BUDGET * 1.5:
            return "HIGH"
        
        return None
    
    def get_stats(self, agent: str = None) -> dict:
        """获取统计信息"""
        if agent:
            events = self.events.get(agent, [])
            return {
                "agent": agent,
                "total_events": len(events),
                "override_count": self.get_event_count(agent, "override"),
                "cost_total": self.get_total_cost(agent),
                "is_blocked": self.is_blocked(agent),
                "cooldown_remaining": self.get_cooldown_remaining(agent)
            }
        
        # 全局
        all_agents = list(self.events.keys())
        return {
            "total_agents": len(all_agents),
            "agents": [self.get_stats(a) for a in all_agents],
            "org_risk_level": self.get_org_risk_level()
        }
