"""
Database Connection
SQLite 封装 - 支持租约 + 心跳机制
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

# 数据库文件路径
DB_PATH = Path(__file__).parent.parent / "organization.db"

# 默认租约时间 (秒)
DEFAULT_LEASE_DURATION = 300  # 5分钟


def get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 任务表 (增强版 - 含租约)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            agent TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'PENDING',
            result TEXT,
            error TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            worker_id TEXT,
            lease_expire_at TIMESTAMP,
            last_heartbeat TIMESTAMP,
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Worker 表 (新增)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker_id TEXT UNIQUE NOT NULL,
            status TEXT NOT NULL DEFAULT 'idle',
            current_task_id INTEGER,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_heartbeat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metadata TEXT,
            FOREIGN KEY (current_task_id) REFERENCES tasks(id)
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"✅ Database initialized: {DB_PATH}")
    print("   - tasks (with lease): ✅")
    print("   - messages: ✅")
    print("   - workers: ✅")


def add_lease_fields():
    """迁移：为 tasks 表添加租约字段"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 检查字段是否存在
    cursor.execute("PRAGMA table_info(tasks)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'worker_id' not in columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN worker_id TEXT")
        print("   + worker_id")
    
    if 'lease_expire_at' not in columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN lease_expire_at TIMESTAMP")
        print("   + lease_expire_at")
    
    if 'last_heartbeat' not in columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN last_heartbeat TIMESTAMP")
        print("   + last_heartbeat")
    
    if 'llm_tier' not in columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN llm_tier TEXT DEFAULT 'auto'")
        print("   + llm_tier")
    
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
