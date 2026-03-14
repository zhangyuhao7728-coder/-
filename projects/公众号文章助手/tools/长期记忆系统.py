#!/usr/bin/env python3
"""
长期记忆系统
自动保存和加载学习内容，跨会话记住所学知识
"""
import os
import json
from datetime import datetime

class LongTermMemory:
    """长期记忆系统"""
    
    def __init__(self):
        self.memory_dir = os.path.expanduser("~/.openclaw/memory")
        self.main_memory = f"{self.memory_dir}/MEMORY.md"
        self.daily_dir = f"{self.memory_dir}/daily"
        self.learned_dir = f"{self.memory_dir}/learned"
        
        # 确保目录存在
        os.makedirs(self.memory_dir, exist_ok=True)
        os.makedirs(self.daily_dir, exist_ok=True)
        os.makedirs(self.learned_dir, exist_ok=True)
    
    def save_learned(self, category: str, content: dict):
        """保存学到的内容"""
        # 按类别保存
        category_file = f"{self.learned_dir}/{category}.json"
        
        # 加载已有记忆
        if os.path.exists(category_file):
            with open(category_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {'items': [], 'updated': None}
        
        # 添加新内容
        data['items'].append({
            **content,
            'learned_at': datetime.now().isoformat()
        })
        data['updated'] = datetime.now().isoformat()
        
        # 保存
        with open(category_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 同时更新主记忆文件
        self.update_main_memory(category, content)
        
        return True
    
    def update_main_memory(self, category: str, content: dict):
        """更新主记忆文件"""
        title = content.get('title', 'Untitled')
        source = content.get('source', 'Unknown')
        
        entry = f"""
## {title}
- 来源: {source}
- 学习时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
- 摘要: {content.get('summary', '')[:200]}
"""
        
        # 追加到主记忆
        with open(self.main_memory, 'a', encoding='utf-8') as f:
            f.write(entry)
    
    def load_all_learned(self) -> dict:
        """加载所有学到的内容"""
        all_learned = {}
        
        if not os.path.exists(self.learned_dir):
            return all_learned
        
        for f in os.listdir(self.learned_dir):
            if f.endswith('.json'):
                category = f.replace('.json', '')
                with open(f"{self.learned_dir}/{f}", 'r', encoding='utf-8') as fp:
                    all_learned[category] = json.load(fp)
        
        return all_learned
    
    def load_category(self, category: str) -> dict:
        """加载特定类别"""
        category_file = f"{self.learned_dir}/{category}.json"
        
        if os.path.exists(category_file):
            with open(category_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'items': []}
    
    def get_summary(self) -> str:
        """获取记忆摘要"""
        all_learned = self.load_all_learned()
        
        summary = "# 🧠 长期记忆摘要\n\n"
        summary += f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        for category, data in all_learned.items():
            count = len(data.get('items', []))
            summary += f"- **{category}**: {count}项\n"
        
        return summary
    
    def search(self, keyword: str) -> list:
        """搜索记忆"""
        results = []
        all_learned = self.load_all_learned()
        
        for category, data in all_learned.items():
            for item in data.get('items', []):
                # 简单搜索
                text = json.dumps(item).lower()
                if keyword.lower() in text:
                    results.append({
                        'category': category,
                        **item
                    })
        
        return results
    
    def remember(self, category: str, title: str, source: str, content: str, summary: str = ""):
        """记住新内容 - 简化接口"""
        return self.save_learned(category, {
            'title': title,
            'source': source,
            'content': content,
            'summary': summary or content[:200]
        })

# 创建全局实例
memory = LongTermMemory()

# ========== 命令行接口 ==========
def cmd_save():
    """保存记忆"""
    import sys
    if len(sys.argv) < 3:
        print("用法: memory.py save <类别> <标题>")
        return
    
    category = sys.argv[2]
    title = sys.argv[3] if len(sys.argv) > 3 else "Untitled"
    source = sys.argv[4] if len(sys.argv) > 4 else "CLI"
    
    memory.remember(category, title, source, "通过CLI保存")
    print(f"✅ 已记住: {title}")

def cmd_load():
    """加载记忆"""
    all_learned = memory.load_all_learned()
    print(memory.get_summary())
    
    for category, data in all_learned.items():
        print(f"\n【{category}】")
        for item in data.get('items', [])[-3:]:  # 最近3条
            print(f"  - {item.get('title', 'Untitled')}")

def cmd_search():
    """搜索记忆"""
    import sys
    if len(sys.argv) < 3:
        print("用法: memory.py search <关键词>")
        return
    
    keyword = sys.argv[2]
    results = memory.search(keyword)
    
    print(f"找到 {len(results)} 条结果:")
    for r in results:
        print(f"  - [{r.get('category')}] {r.get('title')}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print(memory.get_summary())
    else:
        cmd = sys.argv[1]
        if cmd == 'save':
            cmd_save()
        elif cmd == 'load':
            cmd_load()
        elif cmd == 'search':
            cmd_search()
        elif cmd == 'summary':
            print(memory.get_summary())
        else:
            print("未知命令: save/load/search/summary")
