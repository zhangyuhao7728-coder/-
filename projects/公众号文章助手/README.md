# 🛠️ AI公众号内容生产系统 V4

> AI驱动的内容生产平台 | 九大核心模块

位于：`~/项目/Ai学习系统/projects/公众号文章助手/`

---

## 一、系统定位

**AI驱动的内容生产平台**，用于自动完成公众号文章的生产流程。

### 核心能力

| 能力 | 说明 | 状态 |
|------|------|------|
| 内容抓取 | 自动采集参考文章 | ✅ |
| 风格学习 | 分析写作风格 | ✅ |
| 爆文分析 | 分析热门文章特征 | ✅ |
| 自动选题 | 智能推荐主题 | ✅ |
| AI写作 | 自动生成内容 | ✅ |
| SEO优化 | 关键词优化 | ✅ |
| 自动排版 | 公众号格式 | ✅ |
| 封面生成 | 自动制作封面 | ✅ |
| 内容管理 | 素材管理 | ✅ |

---

## 二、系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    AI公众号内容生产系统 V4                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐    │
│  │ 1.内容采集   │ → │ 2.内容解析   │ → │ 3.风格学习   │    │
│  │  crawler/    │   │  Parser     │   │  style/     │    │
│  │ 抓取文章.py  │   │ 结构解析.py  │   │ 风格分析.py  │    │
│  └──────────────┘   └──────────────┘   └──────────────┘    │
│         ↓                  ↓                  ↓             │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐    │
│  │ 4.爆文分析   │ → │ 5.选题系统   │ → │ 6.AI写作     │    │
│  │ 爆文分析.py  │   │ 选题系统.py  │   │ 风格生成.py  │    │
│  └──────────────┘   └──────────────┘   └──────────────┘    │
│         ↓                  ↓                  ↓             │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐    │
│  │ 7.SEO优化   │ → │ 8.排版系统  │ → │ 9.CMS管理    │    │
│  │ 文章优化.py  │   │ Formatter/  │   │ cms.py       │    │
│  └──────────────┘   └──────────────┘   └──────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 三、快速开始

```bash
cd ~/项目/Ai学习系统/projects/公众号文章助手
```

### 终极自动化

```bash
# 一键生成完整文章
python publish_pipeline.py --topic "AI安全"
```

### 分步执行

```bash
# 1. 智能选题
python crawler/选题系统.py

# 2. 抓取参考
python tools/抓取文章.py --url "链接"

# 3. 风格分析
python tools/风格分析.py --file article.md --preview

# 4. AI写作
python tools/风格生成.py --style 余豪风格 --topic "主题"

# 5. SEO优化
python tools/文章优化.py --file output.md --variants

# 6. 排版
python formatter/markdown_to_wechat.py input.md output.html

# 7. 封面
python tools/生成封面.py --title "标题"

# 8. 内容管理
python cms.py
```

---

## 四、模块详解

### 1. 内容采集 (Crawler)

```bash
python tools/抓取文章.py --url "https://mp.weixin.qq.com/xxx"
```

### 2. 内容解析

```bash
python tools/文章结构解析.py --file article.md --style --preview
```

### 3. 风格学习

```bash
python tools/风格分析.py --file article.md --preview
```

### 4. 爆文分析

```bash
python crawler/爆文分析.py
```

### 5. 智能选题

```bash
python crawler/选题系统.py
```

### 6. AI写作

```bash
python tools/风格生成.py --style 余豪风格 --topic "AI安全"
```

### 7. SEO优化

```bash
python tools/文章优化.py --title "标题" --variants
```

### 8. 排版系统

```bash
# 公众号排版
python formatter/markdown_to_wechat.py input.md output.html

# 手机版
python tools/转手机版.py input.html output.html
```

### 9. 内容管理

```bash
python cms.py
```

---

## 五、目录结构

```
公众号文章助手/
│
├── publish_pipeline.py      # 终极自动化
├── cms.py                 # 内容管理系统 ⭐
│
├── tools/                 # 核心工具
│   ├── 抓取文章.py       # 内容采集
│   ├── 文章结构解析.py   # 内容解析
│   ├── 风格分析.py       # 风格学习
│   ├── 风格生成.py       # AI写作
│   ├── 文章优化.py       # SEO优化
│   ├── 生成封面.py       # 封面生成
│   └── 转手机版.py      # 排版
│
├── crawler/                # 采集模块
│   ├── 抓取文章.py
│   ├── 爆文分析.py      # ⭐ 新增
│   └── 选题系统.py      # ⭐ 新增
│
├── style/                 # 风格系统
│   ├── style_database.json
│   └── style_prompt.py
│
├── formatter/             # 排版系统
│   └── markdown_to_wechat.py
│
├── ai/                    # AI调用
│   ├── llm_router.py
│   └── prompts.py
│
└── output/               # 输出
    ├── articles/
    ├── covers/
    └── published_articles/  # CMS管理
```

---

## 六、数据流

```
选题 → 抓取 → 解析 → 学习 → 写作 → 优化 → 排版 → 封面 → CMS
```

---

## 七、技术栈

| 技术 | 用途 |
|------|------|
| Python | 核心语言 |
| requests | 网络请求 |
| BeautifulSoup | HTML解析 |
| MiniMax API | AI写作 |
| 火山引擎 | Plus套餐 |
| Ollama | 本地模型 |

---

## 八、版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| V1 | 2026-03-14 | 基础功能 |
| V2 | 2026-03-14 | 风格学习 |
| V3 | 2026-03-14 | SEO优化 |
| V4 | 2026-03-14 | 九大模块完整版 |

---

## 九、后续规划

- [ ] 爆文分析系统增强
- [ ] 选题系统增强
- [ ] 自动发布
- [ ] 数据统计
- [ ] 多平台支持

---

*更新于：2026-03-14*
