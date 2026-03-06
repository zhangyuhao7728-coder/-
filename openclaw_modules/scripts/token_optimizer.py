#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例 27：Token 用量优化器
统计并优化 API 使用
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path

SESSION_DIR = "/Users/zhangyuhao/.openclaw/agents/main/sessions"

def get_session_tokens():
    """获取会话 token 使用量"""
    results = []
    
    if not os.path.exists(SESSION_DIR):
        return results
    
    sessions_file = os.path.join(SESSION_DIR, "sessions.json")
    if not os.path.exists(sessions_file):
        return results
    
    try:
        with open(sessions_file, 'r') as f:
            data = json.load(f)
            sessions = data.get('sessions', [])
            
            total_tokens = 0
            session_count = len(sessions)
            
            for session in sessions:
                # 估算 token（简化计算）
                msgs = session.get('messageCount', 0)
                tokens = msgs * 1000  # 估算
                total_tokens += tokens
            
            return {
                "sessions": session_count,
                "estimated_tokens": total_tokens
            }
    except:
        pass
    
    return {"sessions": 0, "estimated_tokens": 0}

def analyze_usage():
    """分析使用情况"""
    data = get_session_tokens()
    
    report = f"""📊 Token 使用分析

📅 统计周期: 最近会话

📈 会话统计:
- 会话数量: {data.get('sessions', 0)}
- 预估Token: {data.get('estimated_tokens', 0):,}

💡 优化建议:
"""
    
    # 基础建议
    if data.get('estimated_tokens', 0) > 500000:
        report += """
⚠️ Token 使用较高，建议:
1. 启用记忆归档（用例41）
2. 减少会话历史长度
3. 使用缓存避免重复请求
"""
    else:
        report += """
✅ Token 使用正常
"""
    
    return report

if __name__ == "__main__":
    print(analyze_usage())
