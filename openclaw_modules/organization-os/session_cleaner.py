"""
Session Auto Cleaner - 自动清理 Session
当 Context 超过阈值时自动清理
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path

# 配置
SESSION_DIR = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
MAX_MESSAGES = 30  # 最多保留30条消息
CHECK_INTERVAL = 300  # 5分钟检查一次


def get_session_files():
    """获取 session 文件"""
    if not SESSION_DIR.exists():
        return []
    return [f for f in SESSION_DIR.glob("*.jsonl") if not f.name.endswith('.lock')]


def clean_session(file_path: Path) -> dict:
    """清理单个 session"""
    try:
        messages = []
        
        # 读取消息
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        messages.append(json.loads(line))
                    except:
                        continue
        
        original_count = len(messages)
        
        # 如果消息太多，保留最近的
        if original_count > MAX_MESSAGES:
            messages = messages[-MAX_MESSAGES:]
            
            # 重写文件
            with open(file_path, 'w') as f:
                for msg in messages:
                    f.write(json.dumps(msg, ensure_ascii=False) + '\n')
            
            return {
                'file': file_path.name,
                'before': original_count,
                'after': len(messages),
                'cleaned': True
            }
        
        return {
            'file': file_path.name,
            'count': original_count,
            'cleaned': False
        }
        
    except Exception as e:
        return {
            'file': file_path.name,
            'error': str(e)
        }


def auto_clean():
    """自动清理"""
    print(f"=== 自动清理 Session ===")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    files = get_session_files()
    
    if not files:
        print("没有 session 文件")
        return
    
    total_cleaned = 0
    
    for f in files:
        result = clean_session(f)
        if result.get('cleaned'):
            print(f"✅ {result['file']}: {result['before']} → {result['after']}")
            total_cleaned += 1
        elif 'error' in result:
            print(f"❌ {result['file']}: {result['error']}")
    
    if total_cleaned > 0:
        print(f"🎉 清理了 {total_cleaned} 个 session")
    else:
        print("✨ 无需清理")


# ===== 定时运行 =====

if __name__ == "__main__":
    # 立即清理一次
    auto_clean()
    
    print("\n⏰ 定时任务已启动 (每5分钟检查一次)")
    print("按 Ctrl+C 停止")
    
    while True:
        time.sleep(CHECK_INTERVAL)  # 5分钟
        auto_clean()
