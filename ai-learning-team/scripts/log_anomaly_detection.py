#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例 19：日志异常检测
检测系统日志异常
"""

import os
import re
import subprocess
from datetime import datetime, timedelta
from collections import Counter

LOG_FILES = [
    "/var/log/system.log",
    os.path.expanduser("~/Library/Logs"),
]

ERROR_PATTERNS = [
    r"error",
    r"failed",
    r"critical",
    r"exception",
    r"warning",
]

def analyze_log_file(log_path):
    """分析日志文件"""
    errors = []
    
    if not os.path.exists(log_path):
        return errors
    
    try:
        # 读取最近修改的日志
        result = subprocess.run(
            ["tail", "-n", "500", log_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                for pattern in ERROR_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        errors.append(line.strip())
                        break
    except:
        pass
    
    return errors

def detect_anomalies():
    """检测异常"""
    print("🔍 正在分析系统日志...")
    print()
    
    # 分析 OpenClaw 日志
    log_path = os.path.expanduser("~/.openclaw/logs/gateway.log")
    
    if os.path.exists(log_path):
        errors = analyze_log_file(log_path)
        
        print(f"📊 分析完成")
        print()
        
        if not errors:
            print("✅ 未发现异常")
        else:
            # 统计错误类型
            error_counts = Counter()
            for e in errors:
                # 提取错误类型
                if "error" in e.lower():
                    error_counts["error"] += 1
                elif "warning" in e.lower():
                    error_counts["warning"] += 1
                elif "failed" in e.lower():
                    error_counts["failed"] += 1
                else:
                    error_counts["other"] += 1
            
            print(f"⚠️ 发现 {len(errors)} 条异常:")
            for err_type, count in error_counts.items():
                print(f"   - {err_type}: {count}")
            
            print()
            print("🔍 建议检查最近的错误")
    else:
        print("⚠️ 日志文件不存在")
    
    return len(errors)

if __name__ == "__main__":
    detect_anomalies()
