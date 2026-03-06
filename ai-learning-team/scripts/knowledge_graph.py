#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识图谱重建器 - 用例40
从日常记忆中提取实体和关系，构建知识网络
"""

import os
import json
import re
from datetime import datetime

# 文件路径
GRAPH_FILE = os.path.expanduser("~/.openclaw/workspace/memory/knowledge_graph.json")
DAILY_FILE = os.path.expanduser("~/.openclaw/workspace/memory/daily")

# 实体类型
ENTITY_TYPES = {
    "person": "人物",
    "project": "项目", 
    "concept": "概念",
    "tool": "工具",
    "location": "地点",
    "company": "公司"
}

# 关系类型
RELATION_TYPES = {
    "depends_on": "依赖",
    "knows": "认识",
    "works_on": "工作于",
    "uses": "使用",
    "created": "创建",
    "interested_in": "感兴趣",
    "related_to": "相关"
}

def load_graph():
    """加载知识图谱"""
    if os.path.exists(GRAPH_FILE):
        with open(GRAPH_FILE, 'r') as f:
            return json.load(f)
    return {"entities": {}, "relations": []}

def save_graph(graph):
    """保存知识图谱"""
    os.makedirs(os.path.dirname(GRAPH_FILE), exist_ok=True)
    with open(GRAPH_FILE, 'w') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)

def extract_entities(text):
    """从文本提取实体"""
    entities = []
    
    # 简单规则提取
    patterns = {
        "project": r'([A-Z][a-zA-Z]+[-_]?[A-Za-z0-9]*)',  # 项目名
        "concept": r'(AI|AGI|LLM|GPT|Transformer|神经网络|机器学习|深度学习)',
        "person": r'@(\w+)',  # @人名
        "tool": r'(Python|JavaScript|React|Vue|Docker|Kubernetes)',
    }
    
    for etype, pattern in patterns.items():
        matches = re.findall(pattern, text)
        for m in matches:
            entities.append({"name": m, "type": etype})
    
    return entities

def extract_relations(text, entities):
    """从文本提取关系"""
    relations = []
    entity_names = [e['name'] for e in entities]
    
    # 简单关系模式
    relation_patterns = [
        (r'(\w+) 依赖 (\w+)', 'depends_on'),
        (r'(\w+) 使用 (\w+)', 'uses'),
        (r'(\w+) 创建 (\w+)', 'created'),
        (r'(\w+) 从事 (\w+)', 'works_on'),
    ]
    
    for pattern, rtype in relation_patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            if m[0] in entity_names and m[1] in entity_names:
                relations.append({
                    "from": m[0],
                    "to": m[1],
                    "type": rtype,
                    "source": "auto"
                })
    
    return relations

def add_to_graph(entities, relations):
    """添加到知识图谱"""
    graph = load_graph()
    
    # 添加实体
    for e in entities:
        name = e['name']
        if name not in graph['entities']:
            graph['entities'][name] = {
                "type": e['type'],
                "types": ENTITY_TYPES.get(e['type'], e['type']),
                "mentions": 0,
                "first_seen": datetime.now().strftime("%Y-%m-%d"),
                "last_seen": datetime.now().strftime("%Y-%m-%d")
            }
        graph['entities'][name]['mentions'] += 1
        graph['entities'][name]['last_seen'] = datetime.now().strftime("%Y-%m-%d")
    
    # 添加关系
    for r in relations:
        # 检查是否已存在
        exists = False
        for existing in graph['relations']:
            if existing['from'] == r['from'] and existing['to'] == r['to']:
                exists = True
                break
        if not exists:
            graph['relations'].append(r)
    
    save_graph(graph)
    return len(entities), len(relations)

def query_graph(query):
    """查询知识图谱"""
    graph = load_graph()
    results = {"entities": [], "relations": []}
    
    query = query.lower()
    
    # 查询实体
    for name, info in graph['entities'].items():
        if query in name.lower() or query in info.get('types', '').lower():
            results['entities'].append({name: info})
    
    # 查询关系
    for r in graph['relations']:
        if query in r['from'].lower() or query in r['to'].lower():
            results['relations'].append(r)
    
    return results

def format_graph():
    """格式化图谱输出"""
    graph = load_graph()
    
    output = "🕸️ 知识图谱\n"
    output += f"📅 更新: {datetime.now().strftime('%Y-%m-%d')}\n\n"
    
    output += f"📊 统计:\n"
    output += f"   实体: {len(graph['entities'])}个\n"
    output += f"   关系: {len(graph['relations'])}条\n\n"
    
    # 按类型分组
    by_type = {}
    for name, info in graph['entities'].items():
        t = info.get('types', '其他')
        if t not in by_type:
            by_type[t] = []
        by_type[t].append(name)
    
    for etype, names in by_type.items():
        output += f"🏷️ {etype}: {', '.join(names[:5])}"
        if len(names) > 5:
            output += f" ... (+{len(names)-5})"
        output += "\n"
    
    # 最近关系
    if graph['relations']:
        output += f"\n🔗 最近关系:\n"
        for r in graph['relations'][-5:]:
            output += f"   {r['from']} --[{r['type']}]--> {r['to']}\n"
    
    return output

def process_daily_memory():
    """处理今日记忆"""
    today = datetime.now().strftime("%Y-%m-%d")
    daily_path = os.path.join(DAILY_FILE, f"{today}.md")
    
    if not os.path.exists(daily_path):
        return "今日无记忆文件"
    
    with open(daily_path, 'r') as f:
        content = f.read()
    
    # 提取
    entities = extract_entities(content)
    relations = extract_relations(content, entities)
    
    # 添加
    e_count, r_count = add_to_graph(entities, relations)
    
    return f"提取 {e_count} 个实体, {r_count} 条关系"

def main():
    import sys
    
    if len(sys.argv) < 2:
        print(format_graph())
        return
    
    cmd = sys.argv[1]
    
    if cmd == "update":
        result = process_daily_memory()
        print(result)
    
    elif cmd == "query" and len(sys.argv) > 2:
        query = sys.argv[2]
        results = query_graph(query)
        print(f"查询 '{query}':")
        print(f"  实体: {len(results['entities'])}个")
        print(f"  关系: {len(results['relations'])}条")
    
    elif cmd == "stat":
        graph = load_graph()
        print(f"实体: {len(graph['entities'])}")
        print(f"关系: {len(graph['relations'])}")
    
    else:
        print(format_graph())

if __name__ == "__main__":
    main()
