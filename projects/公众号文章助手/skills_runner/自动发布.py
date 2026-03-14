#!/usr/bin/env python3
"""自动发布Skill执行器"""
import os
from datetime import datetime

def run(title, content):
    output_dir = os.path.expanduser("~/项目/Ai学习系统/projects/公众号文章助手/output/drafts")
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{output_dir}/{datetime.now().strftime('%Y%m%d_%H%M%S')}_{title}.md"
    
    draft = f"""# {title}

> 自动生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
> 状态: 草稿待发布

---

## 文章内容

{content}

---

## 发布检查清单

- [ ] 标题优化
- [ ] SEO检查
- [ ] 封面图片
- [ ] 格式排版
- [ ] 预览确认
- [ ] 定时发布

---
*由AI学习系统自动生成*
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(draft)
    
    print(f"✅ 文章已准备好!")
    print(f"📝 文件: {filename}")
    print(f"\n📋 下一步:")
    print(f"1. 检查内容")
    print(f"2. 优化标题")
    print(f"3. 添加封面")
    print(f"4. 手动发布到公众号")

if __name__ == "__main__":
    import sys
    title = sys.argv[1] if len(sys.argv) > 1 else "新文章"
    content = sys.argv[2] if len(sys.argv) > 2 else "文章内容"
    run(title, content)
