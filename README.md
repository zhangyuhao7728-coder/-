# 🤖 AI学习系统 (OpenClaw AI Learning Team)

> 基于OpenClaw的70个AI自动化用例

## 📁 项目结构

```
Ai学习系统/
├── openclaw_modules/     ← 核心模块 (70个用例)
│   ├── scripts/           # Python脚本 (45+)
│   ├── skills/            # Skill文档 (20+)
│   ├── browser-system/   # 浏览器自动化
│   ├── organization-os/  # 组织系统
│   └── organization_core/ # 核心架构
├── projects/             # 附加项目
│   ├── agent-reach/      # AgentReach配置
│   └── crawler/          # 爬虫工具
├── memory/               # 记忆数据
├── docs/                # 文档
└── config/              # 配置
```

## 🎯 已安装用例

| 类别 | 数量 | 用例 |
|------|------|------|
| 内容创作 | 5 | 03, 20, 52, 57, 58 |
| 记忆与知识 | 5 | 04, 40, 41, 42, 60 |
| 夜间自动化 | 6 | 12, 13, 34, 35, 36, 17 |
| 安全类 | 11 | 05-09, 19, 30, 31, 07, 26 |
| 开发者工具 | 1 | 26 |

## 🚀 快速开始

```bash
# 运行健康检查
python3 openclaw_modules/scripts/health_check.py

# 查看Cron任务
python3 openclaw_modules/scripts/cron_dashboard.py
```

## 📝 默认项目

此项目为学习系统默认AI，其他项目请放在同级目录的 `projects/` 文件夹中。

---
*基于 OpenClaw + Moltbook 70用例构建*
