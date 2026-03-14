#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会话防护脚本 - 防止 token/context 爆炸
功能：
1. 限制会话消息数量
2. 自动截断过长上下文
3. 清理过期会话
4. 监控 token 使用
"""

import os
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

# 配置
SESSIONS_DIR = os.path.expanduser("~/.openclaw/sessions")
MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory")

# 限制配置
MAX_MESSAGES_PER_SESSION = 100  # 单会话最大消息数
MAX_SESSION_AGE_DAYS = 7       # 会话保留天数
MAX_MEMORY_SIZE_MB = 50        # memory 目录最大大小
MAX_TOKENS_PER_MSG = 8000     # 单条消息最大 token 估算

class SessionGuard:
    """会话防护"""
    
    def __init__(self):
        self.cleaned_sessions = 0
        self.truncated_sessions = 0
        self.deleted_files = 0
        
    def get_token_estimate(self, text: str) -> int:
        """估算 token 数量（中英文混合）"""
        # 简单估算：中文约 1.5 字符/token，英文约 4 字符/token
        chinese = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        english = len(text) - chinese
        return int(chinese / 1.5 + english / 4)
    
    def clean_old_sessions(self):
        """清理过期会话"""
        if not os.path.exists(SESSIONS_DIR):
            return
            
        now = datetime.now()
        for filename in os.listdir(SESSIONS_DIR):
            if not filename.endswith(".json"):
                continue
                
            filepath = os.path.join(SESSIONS_DIR, filename)
            try:
                # 检查文件修改时间
                mtime = os.path.getmtime(filepath)
                age_days = (time.time() - mtime) / 86400
                
                if age_days > MAX_SESSION_AGE_DAYS:
                    os.remove(filepath)
                    self.cleaned_sessions += 1
                    print(f"   🗑️ 删除过期会话: {filename}")
            except Exception as e:
                print(f"   ⚠️ 处理失败: {filename}: {e}")
    
    def truncate_long_sessions(self):
        """截断过长会话"""
        if not os.path.exists(SESSIONS_DIR):
            return
            
        for filename in os.listdir(SESSIONS_DIR):
            if not filename.endswith(".json"):
                continue
                
            filepath = os.path.join(SESSIONS_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # 检查消息数量
                messages = data.get("messages", [])
                if len(messages) > MAX_MESSAGES_PER_SESSION:
                    # 保留最新消息 + 系统提示
                    system_prompt = data.get("system_prompt", "")
                    kept_messages = messages[-MAX_MESSAGES_PER_SESSION:]
                    
                    # 重建会话
                    new_data = {
                        "id": data.get("id"),
                        "created": data.get("created"),
                        "updated": datetime.now().isoformat(),
                        "system_prompt": system_prompt,
                        "messages": kept_messages,
                        "truncated": True
                    }
                    
                    with open(filepath, "w", encoding="utf-8") as f:
                        json.dump(new_data, f, ensure_ascii=False, indent=2)
                    
                    self.truncated_sessions += 1
                    print(f"   ✂️ 截断会话: {filename} ({len(messages)} → {len(kept_messages)})")
                    
            except Exception as e:
                print(f"   ⚠️ 处理失败: {filename}: {e}")
    
    def clean_memory_bloat(self):
        """清理 memory 目录膨胀"""
        if not os.path.exists(MEMORY_DIR):
            return
            
        total_size = 0
        files_info = []
        
        for root, dirs, files in os.walk(MEMORY_DIR):
            for f in files:
                filepath = os.path.join(root, f)
                size = os.path.getsize(filepath)
                total_size += size
                mtime = os.path.getmtime(filepath)
                files_info.append((filepath, size, mtime))
        
        size_mb = total_size / 1024 / 1024
        
        if size_mb > MAX_MEMORY_SIZE_MB:
            print(f"   ⚠️ memory 目录过大: {size_mb:.1f}MB")
            
            # 按时间排序，删除最旧的文件
            files_info.sort(key=lambda x: x[2])
            target_size = MAX_MEMORY_SIZE_MB * 0.8 * 1024 * 1024  # 保留 80%
            
            current_size = total_size
            for filepath, size, mtime in files_info:
                if current_size <= target_size:
                    break
                try:
                    os.remove(filepath)
                    current_size -= size
                    self.deleted_files += 1
                    print(f"   🗑️ 删除: {filepath}")
                except Exception as e:
                    pass
            
            print(f"   ✅ 清理完成，释放 {total_size - current_size:.1f}MB")
    
    def check_session_health(self):
        """检查会话健康状态"""
        if not os.path.exists(SESSIONS_DIR):
            print("   ✅ 无会话目录")
            return
            
        session_count = 0
        total_messages = 0
        
        for filename in os.listdir(SESSIONS_DIR):
            if not filename.endswith(".json"):
                continue
            session_count += 1
            
            filepath = os.path.join(SESSIONS_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                messages = data.get("messages", [])
                total_messages += len(messages)
            except:
                pass
        
        avg_messages = total_messages / max(session_count, 1)
        
        print(f"   📊 会话数: {session_count}, 总消息: {total_messages}, 平均: {avg_messages:.0f}")
        
        if avg_messages > MAX_MESSAGES_PER_SESSION * 0.8:
            print(f"   ⚠️ 平均消息数偏高，建议清理")
    
    def run(self):
        """运行防护"""
        print("=" * 50)
        print("🛡️ 会话防护检查")
        print("=" * 50)
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n1️⃣ 检查会话健康...")
        self.check_session_health()
        
        print("\n2️⃣ 清理过期会话...")
        self.clean_old_sessions()
        
        print("\n3️⃣ 截断过长会话...")
        self.truncate_long_sessions()
        
        print("\n4️⃣ 清理 memory 膨胀...")
        self.clean_memory_bloat()
        
        print("\n" + "=" * 50)
        print(f"✅ 完成: 清理 {self.cleaned_sessions} 个过期会话, "
              f"截断 {self.truncated_sessions} 个过长会话, "
              f"删除 {self.deleted_files} 个文件")
        print("=" * 50)

def main():
    guard = SessionGuard()
    guard.run()

if __name__ == "__main__":
    main()
