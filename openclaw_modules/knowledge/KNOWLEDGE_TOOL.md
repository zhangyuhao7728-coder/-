# 知识库索引更新工具

## 命令

```bash
# 添加新知识
./scripts/knowledge_add.sh <title> <tags> <layer> <content>

# 示例
./scripts/knowledge_add.sh "Python 变量" "python,基础" L1 "Python 变量命名规则..."
```

## 自动更新 L0 索引

每次添加知识时，自动更新 `L0_index.json`

## 懒加载读取

```python
def read_knowledge(query):
    # 1. 读取 L0 索引 (< 1KB)
    index = load_json("knowledge/L0_index.json")
    
    # 2. 匹配标签
    matches = [e for e in index["index"] if any(t in query for t in e["tags"])]
    
    # 3. 按需读取 L1 或 L2
    if matches:
        layer = matches[0]["layer"]
        if layer == "L1":
            content = read_file(f"knowledge/L1/{matches[0]['id']}_summary.md")
        else:
            content = read_file(f"knowledge/L2/{matches[0]['id']}_full.md")
    
    return content
```
