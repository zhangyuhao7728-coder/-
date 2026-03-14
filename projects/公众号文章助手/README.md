# 公众号文章助手

> AI学习系统的公众号文章创作工具

位于：`~/项目/Ai学习系统/projects/公众号文章助手/`

---

## 🚀 快速开始

```bash
cd ~/项目/Ai学习系统/projects/公众号文章助手
```

### 终极自动化

```bash
# 一键生成完整文章
python publish_pipeline.py --topic "AI学习路线"

# 交互模式
python publish_pipeline.py --interactive
```

---

## 📁 目录结构

```
公众号文章助手/
├── publish_pipeline.py         # 终极自动化
├── templates/                 # 文章模板
├── tools/                    # CLI工具
│   ├── new_article.py
│   ├── 抓取文章.py
│   ├── 文章结构解析.py
│   ├── 风格分析.py
│   ├── 风格生成.py
│   ├── 文章优化.py
│   ├── 文章总结.py
│   ├── 转手机版.py
│   └── 生成封面.py
├── crawler/                   # 爬虫模块
├── style/                     # 风格系统
├── ai/                       # AI调用
├── formatter/                 # 排版系统
├── output/                    # 输出
└── learning_notes/            # 学习笔记
```

---

## 📝 核心工具

| 工具 | 功能 |
|------|------|
| `publish_pipeline.py` | 终极自动化，一键生成 |
| `文章优化.py` | 优化标题+推荐概率 |
| `风格生成.py` | AI风格化写作 |
| `风格分析.py` | 提取写作风格 |
| `抓取文章.py` | 公众号文章抓取 |
| `生成封面.py` | 多模板封面 |

---

## 使用示例

### 1. 终极自动化

```bash
cd ~/项目/Ai学习系统/projects/公众号文章助手
python publish_pipeline.py --topic "AI安全" --style 余豪风格
```

### 2. 文章优化

```bash
python tools/文章优化.py --title "AI教程" --variants
```

### 3. 风格分析

```bash
python tools/风格分析.py --file ~/Desktop/AI安全文章.md --preview
```

### 4. 生成封面

```bash
python tools/生成封面.py --title "我的文章" --template tech
```

### 5. 公众号排版

```bash
python formatter/markdown_to_wechat.py input.md output.html
```

---

## 在AI学习系统中调用

你可以通过Telegram发送指令来使用：

- 让AI帮你写文章
- 让AI分析文章风格
- 让AI优化标题

---

更新于：2026-03-14
