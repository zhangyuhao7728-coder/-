"""
Task Repository
任务持久化
"""

import json
from typing import Optional, List, Dict, Any
from datetime import datetime
from organization_core.persistence.db import get_connection


class TaskRepository:
    """任务仓储"""
    
    def create(self, content: str, agent: str) -> int:
        """创建新任务"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO tasks (content, agent, status) VALUES (?, ?, ?)",
            (content, agent, "PENDING")
        )
        
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        
        print(f"📝 Task created: #{task_id} - {agent} - {content[:30]}...")
        return task_id
    
    def update_status(
        self, 
        task_id: int, 
        status: str, 
        result: Optional[str] = None,
        error: Optional[str] = None
    ) -> None:
        """更新任务状态"""
        conn = get_connection()
        cursor = conn.cursor()
        
        if result:
            cursor.execute(
                "UPDATE tasks SET status = ?, result = ?, updated_at = ? WHERE id = ?",
                (status, result, datetime.now().isoformat(), task_id)
            )
        elif error:
            cursor.execute(
                "UPDATE tasks SET status = ?, error = ?, updated_at = ? WHERE id = ?",
                (status, error, datetime.now().isoformat(), task_id)
            )
        else:
            cursor.execute(
                "UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?",
                (status, datetime.now().isoformat(), task_id)
            )
        
        conn.commit()
        conn.close()
        
        print(f"✅ Task #{task_id} status: {status}")
    
    def get(self, task_id: int) -> Optional[Dict[str, Any]]:
        """获取单个任务"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def list_all(self, limit: int = 100) -> List[Dict[str, Any]]:
        """列出所有任务"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM tasks ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def list_by_status(self, status: str, limit: int = 100) -> List[Dict[str, Any]]:
        """按状态列出任务"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC LIMIT ?",
            (status, limit)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_pending(self) -> List[Dict[str, Any]]:
        """获取所有待处理任务（用于恢复）"""
        return self.list_by_status("PENDING")
    
    def get_running(self) -> List[Dict[str, Any]]:
        """获取所有运行中任务（用于恢复）"""
        return self.list_by_status("RUNNING")
    
    def delete(self, task_id: int) -> None:
        """删除任务"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        
        conn.commit()
        conn.close()
    
    def get_unfinished_tasks(self) -> List[Dict[str, Any]]:
        """获取所有未完成任务（PENDING + RUNNING）用于崩溃恢复"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, content, agent, status
            FROM tasks
            WHERE status IN ('PENDING', 'RUNNING')
            ORDER BY created_at ASC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
