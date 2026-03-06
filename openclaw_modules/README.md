# AI 学习团队系统

## 概述

这是一个基于 OpenClaw 的 AI 学习团队系统，专为 AI 学习者设计。

## 文件结构

```
/
├── README.md                      # 使用说明
├── openclaw.json                  # 主配置文件
├── T01-create-17-agents.sh       # 创建 Agent 脚本
├── T02-generate-daily-plans.sh   # 生成每日计划脚本
├── T03-setup-cron-jobs.sh        # Cron 任务配置
├── Squad架构设计说明.md           # 架构文档
├── core_server.py                 # 核心服务
├── openclaw_bridge.py             # OpenClaw 桥接
├── risk_manager.py                # 风险管理
├── daily-plan-templates/          # 每日计划模板
│   └── 00-CEO总览.md            # CEO 日报模板
├── templates/                     # Agent 模板
│   ├── souL.md                  # Agent 身份模板
│   ├── USER.md                  # 用户信息模板
│   ├── MEMORY.md                # 记忆模板
│   └── daily/                   # 每日计划详细模板
│       ├── L1_CEO_DAILY.md
│       ├── L2_SQUAD_PRODUCT.md
│       ├── L2_SQUAD_TECH.md
│       ├── L2_SQUAD_MARKETING.md
│       ├── L3_TASK_CARD.md
│       └── TIMELINE.md
├── browser-system/                # 浏览器自动化系统
├── browser_cluster/               # 浏览器集群
├── config/                       # 配置文件
├── docs/                         # 文档
├── generated/                    # 生成的输出
├── knowledge/                    # 知识库
├── organization-os/               # 组织系统
├── organization_core/             # 组织核心
├── persistence/                   # 持久化
├── runtime/                      # 运行时
├── scripts/                      # 脚本工具
├── skills/                       # 技能配置
├── souls/                        # Agent 灵魂
├── tools/                        # 工具
└── utils/                        # 工具函数
```

## 快速开始

1. 配置 Telegram Bot
2. 配置飞书机器人（可选）
3. 启动 OpenClaw Gateway
4. 开始使用

## 团队成员

| Agent | 角色 | 状态 |
|-------|------|------|
| CEO | 调度内核 | ✅ |
| Planner | 任务规划师 | ✅ |
| Researcher | 调研研究员 | ✅ |
| Engineer | 工程师 | ✅ |
| Reviewer | 审查员 | ⏳ |
| Analyst | 分析师 | ⏳ |

## 联系方式

- 主人: 张余浩 (CEO)
- 时区: Asia/Shanghai
