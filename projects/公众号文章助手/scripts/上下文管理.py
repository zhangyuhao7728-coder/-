#!/usr/bin/env python3
"""
上下文管理脚本
功能：
1. 定期清理会话历史
2. 保留关键记忆到memory
3. 生成会话摘要
"""

import os
import json
from datetime import datetime, timedelta

SESSION_DIR = os.path.expanduser("~/.openclaw/sessions/")
MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory/")

def get_session_size(session_path):
    """获取会话大小"""
    total = 0
    for f in os.listdir(session_path):
        fp = os.path.join(session_path, f)
        if os.path.isfile(fp):
            total += os.path.getsize(fp)
    return total

def should_keep_session(session_name, max_age_days=7):
    """判断是否应该保留会话"""
    try:
        # 解析日期
        date_str = session_name.split('-')[0]
        session_date = datetime.strptime(date_str, "%Y%m%d")
        age = (datetime.now() - session_date).days
        return age <= max_age_days
    except:
        return False

def cleanup_sessions(max_size_mb=10, max_days=7):
    """清理会话，保留关键信息"""
    
    if not os.path.exists(SESSION_DIR):
        print("无会话目录")
        return
    
    sessions = [d for d in os.listdir(SESSION_DIR) 
                if os.path.isdir(os.path.join(SESSION_DIR, d))]
    
    print(f"发现 {len(sessions)} 个会话")
    
    # 按日期排序
    sessions.sort(reverse=True)
    
    total_size = 0
    kept = []
    
    for session in sessions:
        session_path = os.path.join(SESSION_DIR, session)
        size = get_session_size(session_path)
        total_size += size
        
        # 保留最近的或重要的会话
        if should_keep_session(session, max_days):
            kept.append((session, size))
        else:
            # 移动到归档
            archive_dir = os.path.join(SESSION_DIR, "archive")
            os.makedirs(archive_dir, exist_ok=True)
            # 这里可以添加移动逻辑
    
    size_mb = total_size / 1024 / 1024
    print(f"总会话大小: {size_mb:.2f} MB")
    print(f"保留会话: {len(kept)}")
    
    return kept

if __name__ == "__main__":
    cleanup_sessions()
