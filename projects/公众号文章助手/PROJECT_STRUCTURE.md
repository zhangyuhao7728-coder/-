# 📁 项目结构说明

```
公众号文章助手/
├── 📂 core/                  # 核心脚本
│   ├── cms.py               # 内容管理系统
│   └── publish_pipeline.py   # 发布流程
│
├── 📂 crawler/              # 采集系统
│   ├── 选题系统.py          # 智能选题
│   ├── 爆文分析.py          # 爆文分析
│   └── 抓取文章.py          # 文章采集
│
├── 📂 tools/                # 工具脚本
│   ├── 📂 crawler/         # 采集工具
│   ├── 📂 generate/         # 生成工具
│   ├── 📂 optimize/        # 优化工具
│   ├── 📂 system/          # 系统工具
│   └── 其他工具...
│
├── 📂 skills_runner/       # Skills执行器
│   ├── 算法刷题.py
│   ├── 知识整理.py
│   └── 自动发布.py
│
├── 📂 data/                # 配置文件
│   ├── 📂 learning/        # 学习资料
│   ├── 📂 project/        # 项目配置
│   └── 📂 ai_team/        # AI团队配置
│
├── 📂 docs/                # 文档
│   ├── 效率提升10倍指南.md
│   └── 项目升级报告.md
│
├── 📂 ai_team/            # AI团队配置
│   ├── 团队配置.md
│   ├── 三层工作流.md
│   └── agents.json
│
├── 📂 output/              # 输出文件
│   ├── published_articles/ # 已发布文章
│   └── drafts/            # 草稿
│
└── 📂 scripts/             # 启动脚本
    ├── AI学习系统.command
    ├── 开机自启.command
    └── 成本优化.command
```

## 📊 统计

| 类型 | 数量 |
|------|------|
| 核心脚本 | 2 |
| 采集系统 | 3 |
| 工具脚本 | 20+ |
| Skills | 19 |
| 配置文件 | 15+ |

## 🚀 快速开始

```bash
# 选题
python3 crawler/选题系统.py

# 生成文章
python3 tools/generate/智能写作V3.py

# 安全检查
python3 tools/system/安全检查.py

# 启动系统
open AI学习系统.command
```

---
*更新时间: 2026-03-14*
