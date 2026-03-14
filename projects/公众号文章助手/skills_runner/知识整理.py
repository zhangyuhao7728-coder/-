#!/usr/bin/env python3
"""知识整理Skill执行器"""
import os
from datetime import datetime

def run(topic, content):
    notes_dir = os.path.expanduser("~/笔记/AI学习")
    os.makedirs(notes_dir, exist_ok=True)
    
    filename = f"{notes_dir}/{topic}_{datetime.now().strftime('%Y%m%d')}.md"
    
    content_md = f"""# {topic}

> 创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 内容

{content}

## 标签

- AI学习
- {topic}

## 总结

---
*由AI学习系统自动整理*
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content_md)
    
    print(f"✅ 知识已整理保存到:")
    print(f"   {filename}")

if __name__ == "__main__":
    import sys
    topic = sys.argv[1] if len(sys.argv) > 1 else "Python学习"
    content = sys.argv[2] if len(sys.argv) > 2 else "学习笔记内容"
    run(topic, content)
