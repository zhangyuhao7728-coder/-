#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周记忆归档 - 用例41
每周压缩旧日志为月度摘要，减少Token消耗
"""

import os
import json
import shutil
from datetime import datetime, timedelta

# 文件路径
MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory/daily")
ARCHIVE_DIR = os.path.expanduser("~/.openclaw/workspace/memory/archive")
MEMORY_FILE = os.path.expanduser("~/.openclaw/workspace/MEMORY.md")

DAYS_THRESHOLD = 30  # 超过30天归档

def get_date_from_filename(filename):
    """从文件名提取日期"""
    try:
        date_str = filename.replace('.md', '')
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return None

def create_monthly_summary(files):
    """创建月度摘要"""
    if not files:
        return None
    
    # 按年月分组
    by_month = {}
    for f in files:
        date = get_date_from_filename(f)
        if date:
            key = date.strftime("%Y-%m")
            if key not in by_month:
                by_month[key] = []
            by_month[key].append(f)
    
    summaries = []
    
    for month, month_files in by_month.items():
        summary_file = os.path.join(ARCHIVE_DIR, f"summary_{month}.md")
        
        with open(summary_file, 'w') as f:
            f.write(f"# {month} 月度记忆摘要\n\n")
            f.write(f"## 概要\n")
            f.write(f"- 总天数: {len(month_files)}天\n")
            f.write(f"- 创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write(f"## 每日要点\n\n")
            
            for day_file in sorted(month_files):
                day_path = os.path.join(MEMORY_DIR, day_file)
                if os.path.exists(day_path):
                    with open(day_path, 'r') as df:
                        content = df.read()
                    # 提取标题和前几行
                    lines = content.split('\n')[:5]
                    title = lines[0] if lines else day_file
                    f.write(f"### {day_file.replace('.md', '')}\n")
                    f.write(f"{title}\n\n")
            
            # 添加索引到MEMORY
            add_to_memory(month, summary_file)
            summaries.append((month, summary_file))
    
    return summaries

def add_to_memory(month, summary_file):
    """添加到MEMORY.md索引"""
    index_line = f"- **{month}月**: [月度摘要](memory/archive/summary_{month}.md)"
    
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            content = f.read()
        
        if month not in content:
            # 添加到归档部分
            if "## 归档" in content:
                content = content.replace("## 归档", f"## 归档\n{index_line}")
            else:
                content += f"\n\n## 归档\n{index_line}\n"
            
            with open(MEMORY_FILE, 'w') as f:
                f.write(content)

def archive_old_files():
    """归档旧文件"""
    if not os.path.exists(MEMORY_DIR):
        return "无记忆目录"
    
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    
    now = datetime.now()
    threshold = now - timedelta(days=DAYS_THRESHOLD)
    
    # 获取所有日记文件
    all_files = [f for f in os.listdir(MEMORY_DIR) if f.endswith('.md')]
    
    # 分类
    to_archive = []
    to_keep = []
    
    for f in all_files:
        date = get_date_from_filename(f)
        if date and date < threshold:
            to_archive.append(f)
        else:
            to_keep.append(f)
    
    if not to_archive:
        return f"无超过{DAYS_THRESHOLD}天的文件"
    
    # 移动到归档
    archived_count = 0
    for f in to_archive:
        src = os.path.join(MEMORY_DIR, f)
        dst = os.path.join(ARCHIVE_DIR, f)
        shutil.move(src, dst)
        archived_count += 1
    
    # 创建月度摘要
    summaries = create_monthly_summary(to_archive)
    
    result = f"📦 已归档: {archived_count}个文件\n"
    result += f"📋 创建摘要: {len(summaries)}个\n"
    result += f"📁 保留: {len(to_keep)}个近期文件"
    
    return result

def show_archive_stats():
    """显示归档统计"""
    if not os.path.exists(ARCHIVE_DIR):
        return "暂无归档"
    
    files = [f for f in os.listdir(ARCHIVE_DIR) if f.endswith('.md')]
    
    output = "📦 记忆归档\n"
    output += f"📁 归档文件: {len(files)}个\n"
    
    # 按月份统计
    by_month = {}
    for f in files:
        if 'summary' in f:
            month = f.replace('summary_', '').replace('.md', '')
            by_month[month] = by_month.get(month, 0) + 1
    
    if by_month:
        output += "\n📅 按月统计:\n"
        for month, count in sorted(by_month.items()):
            output += f"   {month}: {count}个\n"
    
    return output

def main():
    import sys
    
    if len(sys.argv) < 2:
        print(show_archive_stats())
        return
    
    cmd = sys.argv[1]
    
    if cmd == "archive":
        result = archive_old_files()
        print(result)
    
    elif cmd == "stats":
        print(show_archive_stats())
    
    else:
        print(show_archive_stats())

if __name__ == "__main__":
    main()
