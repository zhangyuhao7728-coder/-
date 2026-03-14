# 🛠️ AI公众号内容生产系统

> 位于：`~/项目/Ai学习系统/projects/公众号文章助手/`

## 📁 项目结构

```
公众号文章助手/
├── core/              # 核心脚本
│   ├── cms.py         # 内容管理
│   └── publish_pipeline.py  # 发布流程
├── crawler/           # 采集系统
│   ├── 选题系统.py
│   ├── 爆文分析.py
│   └── ...
├── tools/            # 工具脚本 (26个)
├── skills_runner/    # Skills执行器
├── data/            # 配置文件 (18个)
├── docs/            # 文档
├── formatter/       # 排版工具
├── ai_team/        # AI团队配置
└── output/         # 输出文件
```

## 🚀 快速开始

```bash
cd ~/项目/Ai学习系统/projects/公众号文章助手

# 选题
python3 crawler/选题系统.py

# 写作
python3 tools/智能写作V3.py

# 安全检查
python3 tools/security_check.py
```

## 📊 能力

- Skills: 19个
- 工具: 26个
- 配置: 18个

## 🧠 长期记忆

- 8项分类
- 跨会话记忆

---
*版本: V5 | 更新: 2026-03-14*

---

## WordPress AI 开发

### 新增功能

- WordPress开发Skill
- Claude Code配置
- WordPress Studio配置
- AI开发教程

### 快速开始

```bash
# 1. 安装Claude Code
npm install @anthropic-ai/claude-code

# 2. 安装WordPress Studio
# https://developer.wordpress.com/studio/

# 3. 查看教程
# docs/WordPress_AI开发教程.md
```
