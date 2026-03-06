"""
Database
SQLite 数据库封装 - 负责数据存储，不含业务逻辑
增强版：WAL 模式 + 唯一约束
"""

import sqlite3
from datetime import datetime
from pathlib import Path


class Database:
    """SQLite 数据库封装"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path(__file__).parent.parent / "organization.db"
        self.db_path = str(db_path)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False, timeout=30)
        self.conn.row_factory = sqlite3.Row
        
        # 开启 WAL 模式（解决并发问题）
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA synchronous=NORMAL;")
        self.conn.execute("PRAGMA busy_timeout=5000;")
        
        self._init_tables()
    
    def get_connection(self):
        """获取数据库连接"""
        return self.conn
    
    def _init_tables(self):
        """初始化表"""
        cursor = self.conn.cursor()
        
        # 任务表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                agent TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'PENDING',
                result TEXT,
                error TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                worker_id TEXT,
                lease_expire_at TEXT,
                last_heartbeat TEXT,
                llm_tier TEXT DEFAULT 'auto'
            )
        """)
        
        # 消息表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                sender TEXT,
                channel TEXT,
                agent TEXT,
                status TEXT,
                created_at TEXT NOT NULL
            )
        """)
        
        # Worker 表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                worker_id TEXT UNIQUE NOT NULL,
                status TEXT NOT NULL DEFAULT 'idle',
                current_task_id INTEGER,
                started_at TEXT NOT NULL,
                last_heartbeat TEXT NOT NULL,
                metadata TEXT,
                FOREIGN KEY (current_task_id) REFERENCES tasks(id)
            )
        """)
        
        # 风险事件表 (带唯一约束)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS risk_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                level TEXT NOT NULL,
                cost REAL NOT NULL,
                budget REAL NOT NULL,
                override_count INTEGER NOT NULL,
                reason TEXT NOT NULL,
                created_at TEXT NOT NULL,
                UNIQUE(date, agent_name, level)
            )
        """)
        
        # 成本追踪表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cost_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT NOT NULL,
                date TEXT NOT NULL,
                cost REAL NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        
        # Override 记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS overrides (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT NOT NULL,
                date TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        
        # Risk Cooldowns 表 (新增)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS risk_cooldowns (
                agent TEXT PRIMARY KEY,
                unblock_time REAL NOT NULL,
                level TEXT NOT NULL,
                reason TEXT,
                created_at TEXT NOT NULL
            )
        """)
        
        self.conn.commit()
    
    # ======================
    # Risk Events
    # ======================
    
    def insert_risk_event(self, data: dict):
        """插入风险事件（依赖 UNIQUE 约束防止重复）"""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO risk_events
                (date, agent_name, level, cost, budget, override_count, reason, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["date"],
                data["agent_name"],
                data["level"],
                data["cost"],
                data["budget"],
                data["override_count"],
                data["reason"],
                data["created_at"],
            ))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # 唯一约束冲突，忽略
            return False
    
    def get_today_risk_levels(self, agent_name: str, date: str) -> list:
        """获取今日风险等级"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT level FROM risk_events
            WHERE agent_name=? AND date=?
        """, (agent_name, date))
        return [row["level"] for row in cursor.fetchall()]
    
    def exists_risk(self, agent_name: str, date: str, level: str) -> bool:
        """检查风险事件是否存在"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 1 FROM risk_events
            WHERE agent_name=? AND date=? AND level=?
            LIMIT 1
        """, (agent_name, date, level))
        return cursor.fetchone() is not None
    
    # ======================
    # Cost Queries
    # ======================
    
    def get_today_cost(self, agent_name: str) -> float:
        """获取今日成本"""
        today = datetime.now().date().isoformat()
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT SUM(cost) as total
            FROM cost_tracking
            WHERE agent_name=? AND date=?
        """, (agent_name, today))
        row = cursor.fetchone()
        return row["total"] if row["total"] else 0.0
    
    def insert_cost(self, agent_name: str, cost: float):
        """记录成本"""
        today = datetime.now().date().isoformat()
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO cost_tracking (agent_name, date, cost, created_at)
            VALUES (?, ?, ?, ?)
        """, (agent_name, today, cost, datetime.now().isoformat()))
        self.conn.commit()
    
    # ======================
    # Override Queries
    # ======================
    
    def get_today_override_count(self, agent_name: str) -> int:
        """获取今日 Override 次数"""
        today = datetime.now().date().isoformat()
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as total
            FROM overrides
            WHERE agent_name=? AND date=?
        """, (agent_name, today))
        row = cursor.fetchone()
        return row["total"] if row["total"] else 0
    
    def insert_override(self, agent_name: str):
        """记录 Override"""
        today = datetime.now().date().isoformat()
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO overrides (agent_name, date, created_at)
            VALUES (?, ?, ?)
        """, (agent_name, today, datetime.now().isoformat()))
        self.conn.commit()
    
    # ======================
    # Lock Check
    # ======================
    
    def is_agent_locked(self, agent_name: str) -> bool:
        """检查 Agent 是否被锁定 (基于数据库)"""
        cursor = self.conn.cursor()
        
        # 检查是否有 CRITICAL 级别的冷却
        cursor.execute("""
            SELECT unblock_time FROM risk_cooldowns
            WHERE agent = ?
        """, (agent_name,))
        
        row = cursor.fetchone()
        if not row:
            return False
        
        import time
        return time.time() < row["unblock_time"]
    
    def set_cooldown(self, agent: str, unblock_time: float, level: str, reason: str = ""):
        """设置冷却时间"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO risk_cooldowns (agent, unblock_time, level, reason, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (agent, unblock_time, level, reason, datetime.now().isoformat()))
        self.conn.commit()
    
    def clear_cooldown(self, agent: str):
        """清除冷却"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM risk_cooldowns WHERE agent = ?", (agent,))
        self.conn.commit()
    
    def get_cooldown(self, agent: str) -> dict:
        """获取冷却信息"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM risk_cooldowns WHERE agent = ?
        """, (agent,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_all_cooldowns(self) -> list:
        """获取所有冷却信息"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM risk_cooldowns")
        return [dict(row) for row in cursor.fetchall()]
    
    # ======================
    # Risk Summary
    # ======================
    
    def get_risk_events(self, agent_name: str = None, limit: int = 100) -> list:
        """获取风险事件"""
        cursor = self.conn.cursor()
        if agent_name:
            cursor.execute("""
                SELECT * FROM risk_events
                WHERE agent_name=?
                ORDER BY created_at DESC
                LIMIT ?
            """, (agent_name, limit))
        else:
            cursor.execute("""
                SELECT * FROM risk_events
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))
        return [dict(row) for row in cursor.fetchall()]
    
    def close(self):
        """关闭连接"""
        self.conn.close()


# 全局数据库实例
_db = None


def get_database() -> Database:
    """获取数据库实例"""
    global _db
    if _db is None:
        _db = Database()
    return _db
