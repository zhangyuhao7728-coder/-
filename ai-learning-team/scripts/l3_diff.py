#!/usr/bin/env python3
"""
L3 差异检测层
对比昨天vs今天，提取新增内容
"""

import json
import os
from datetime import datetime, timedelta

L2_DIR = "knowledge/L2_clean"
L3_DIR = "knowledge/L3_updates"

def load_cleaned(source, date_str):
    """加载清洗后的数据"""
    filepath = f"{L2_DIR}/{source}/{date_str}.json"
    
    if not os.path.exists(filepath):
        return None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def compare_content(old_content, new_content):
    """对比内容差异"""
    if not old_content:
        return {"type": "new", "content": new_content}
    
    old_lines = set(old_content.split('\n'))
    new_lines = set(new_content.split('\n'))
    
    # 新增行
    added = new_lines - old_lines
    
    # 删除行
    removed = old_lines - new_lines
    
    return {
        "type": "updated" if added or removed else "unchanged",
        "added_count": len(added),
        "removed_count": len(removed),
        "added_lines": list(added)[:20],  # 限制数量
        "removed_lines": list(removed)[:20]
    }

def detect_changes(source):
    """检测变化"""
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    old_data = load_cleaned(source, yesterday)
    new_data = load_cleaned(source, today)
    
    if not new_data:
        return None
    
    if not old_data:
        return {
            "source": source,
            "type": "first_import",
            "content": new_data.get("cleaned_content", "")[:10000],
            "note": "首次导入，无历史对比"
        }
    
    # 对比
    old_content = old_data.get("cleaned_content", "")
    new_content = new_data.get("cleaned_content", "")
    
    diff = compare_content(old_content, new_content)
    
    if diff["type"] == "unchanged":
        return None
    
    return {
        "source": source,
        "type": diff["type"],
        "compared_date": f"{yesterday} vs {today}",
        "changes": diff,
        "new_content_preview": '\n'.join(diff.get("added_lines", []))
    }

def save_updates(source, data):
    """保存更新"""
    os.makedirs(f"{L3_DIR}/{source}", exist_ok=True)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{L3_DIR}/{source}/{date_str}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return filename

def main():
    print("=" * 60)
    print("🔍 L3 差异检测层")
    print("=" * 60)
    
    sources = ["real_python", "w3schools", "geeksforgeeks", "kaggle"]
    
    has_changes = False
    
    for source in sources:
        print(f"\n🔎 检测: {source}...")
        
        changes = detect_changes(source)
        
        if changes:
            if changes["type"] == "first_import":
                print(f"   📦 首次导入")
            elif changes["type"] == "updated":
                print(f"   📝 有更新: +{changes['changes']['added_count']} 行")
            elif changes["type"] == "new":
                print(f"   🆕 新内容")
            
            # 保存
            filename = save_updates(source, changes)
            print(f"   ✅ 已保存: {filename}")
            has_changes = True
        else:
            print(f"   ➖ 无变化")
    
    if not has_changes:
        print("\n📭 今日无新内容")
    
    print("\n" + "=" * 60)
    print("✅ L3 检测完成!")
    print("=" * 60)

if __name__ == "__main__":
    main()
