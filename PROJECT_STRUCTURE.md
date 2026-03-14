# AI学习系统

> 余豪的AI学习项目集

位于：`~/项目/Ai学习系统/`

---

## 📁 项目结构

```
AI学习系统/
│
├── 核心文件
│   ├── .env                  # 环境变量
│   ├── README.md             # 本文件
│   ├── TOOLS.md             # 工具说明
│   ├── AGENTS.md            # Agent配置
│   └── IDENTITY.md          # 身份配置
│
├── 核心模块 (core/)
│   ├── security/            # 安全模块
│   ├── scripts/             # 自动化脚本
│   ├── openclaw_modules/    # OpenClaw模块
│   ├── config/              # 配置文件
│   └── docs/                # 文档
│
├── 项目集 (projects/)
│   ├── 公众号文章助手/      # 公众号文章工具 ⭐
│   ├── agent-reach/        # Agent Reach配置
│   ├── crawler/             # 爬虫模块
│   ├── ai_control-plane/    # AI控制平面
│   ├── ai-coding-academy/   # 编程学院
│   ├── ai-company-os/      # 公司OS
│   ├── ai-team-os/         # 团队OS
│   ├── learning/             # 学习模块
│   └── ...
│
├── 学习资源
│   ├── memory/              # 学习记忆
│   ├── skills/              # 技能配置
│   └── learning/            # 学习内容
│
├── 运行环境
│   ├── agents/              # Agent运行
│   ├── runtime/             # 运行时
│   ├── skills/              # 技能
│   └── systems/             # 系统
│
└── 辅助
    ├── logs/               # 日志
    ├── scripts/             # 脚本
    └── utils/               # 工具
```

---

## 🚀 快速开始

### 公众号文章助手

```bash
cd ~/项目/Ai学习系统/projects/公众号文章助手

# 生成文章
python publish_pipeline.py --topic "AI安全"

# 优化标题
python tools/文章优化.py --title "标题"
```

### 运行AI系统

```bash
cd ~/项目/Ai学习系统
python openclaw_modules/...
```

---

## 📦 主要项目

| 项目 | 说明 |
|------|------|
| `公众号文章助手` | 公众号文章创作工具 |
| `ai-control-plane` | AI控制平面 |
| `learning` | Python学习系统 |
| `security` | 安全防护模块 |

---

## 🔧 常用命令

```bash
# 启动Gateway
openclaw gateway start

# 查看状态
openclaw gateway status

# 运行脚本
python ~/项目/Ai学习系统/scripts/...
```

---

## 📝 文章发布流程

```
1. 写文章 → projects/公众号文章助手/
2. 生成封面 → tools/生成封面.py
3. 排版 → formatter/markdown_to_wechat.py
4. 保存 → output/published_articles/
```

---

更新于：2026-03-14
