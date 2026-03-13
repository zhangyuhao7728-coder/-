# 📁 AI学习系统 - 项目结构

```
AI学习系统/
│
├── 🌐 核心模块
│   ├── learning/              # 学习模块
│   │   ├── ai-coach/        # AI 教练
│   │   ├── curriculum/      # 课程体系
│   │   ├── problems/        # 题目库
│   │   ├── evaluation/      # 评估系统
│   │   └── notes/           # 学习笔记
│   │
│   ├── ai-control-plane/     # AI 控制面板
│   │   ├── core/            # 核心逻辑
│   │   ├── providers/       # 模型提供商
│   │   └── dashboard/      # 仪表盘
│   │
│   ├── projects/             # 实践项目
│   │   ├── crawler/         # 爬虫项目 ⭐
│   │   └── agent-reach/    # Agent 工具
│   │
│   ├── openclaw_modules/    # OpenClaw 对接
│   │
│   └── runtime/             # 运行时
│
├── 🔧 工具模块
│   ├── scripts/             # 自动化脚本
│   ├── skills/              # 技能配置
│   ├── config/              # 配置文件
│   └── utils/               # 工具函数
│
├── 🛡️ 安全模块 (新增)
│   ├── __init__.py
│   ├── secrets_manager.py   # 密钥管理
│   ├── permission_guard.py  # 权限守卫
│   ├── audit_logger.py      # 审计日志
│   └── sandbox.py           # 沙盒环境
│
├── 📊 数据
│   ├── memory/              # 记忆库
│   ├── datasets/            # 数据集
│   └── logs/                # 日志目录
│
├── 📄 配置
│   ├── .env.example         # 密钥模板
│   ├── .gitignore           # Git 忽略
│   └── README.md            # 说明文档
│
└── 🎯 入口
    ├── launcher.html         # 启动器
    └── package.json          # 项目配置
```

---

## 📦 模块说明

### learning/ - 学习模块
| 目录 | 说明 |
|------|------|
| ai-coach | AI 教练 - 智能学习辅导 |
| curriculum | 课程体系 - 学习路径 |
| problems | 题目库 - LeetCode/算法 |
| evaluation | 评估系统 - 能力测评 |
| notes | 学习笔记 - 知识记录 |

### projects/crawler/ - 爬虫项目 ⭐
| 文件 | 说明 |
|------|------|
| crawler.py | 多功能爬虫 v5.0 |
| run.sh | 启动脚本 |
| output/ | 输出目录 |
| crawler.db | SQLite 数据库 |

### security/ - 安全模块 🛡️
| 文件 | 说明 |
|------|------|
| secrets_manager.py | 密钥管理 (从环境变量读取) |
| permission_guard.py | 权限检查和修复 |
| audit_logger.py | 操作审计日志 |
| sandbox.py | 沙盒执行环境 |

---

## 🔐 安全使用

### 1. 配置密钥
```bash
# 复制模板
cp .env.example .env

# 编辑配置
nano .env
```

### 2. 代码中使用
```python
from security import get_secret

# 获取密钥
TOKEN = get_secret("TELEGRAM_BOT_TOKEN")
```

### 3. 权限检查
```python
from security import check_file, scan_dir

# 检查文件权限
result = check_file('/path/to/.env')

# 扫描目录
issues = scan_dir('./projects', ['.py', '.env'])
```

### 4. 审计日志
```python
from security import log

# 记录操作
log('user_login', method='telegram', success=True)
```

### 5. 沙盒执行
```python
from security import safe_read, safe_exec

# 安全读取
content = safe_read('./data/file.txt')

# 安全执行
result = safe_exec('ls -la', timeout=10)
```

---

## 🚀 快速开始

```bash
# 进入项目目录
cd ~/项目/Ai学习系统

# 运行爬虫
cd projects/crawler
python3 crawler.py -s quotes -p 3

# 使用安全模块
python3 -c "
from security import get_secrets_manager
sm = get_secrets_manager()
print(sm.validate())
"
```

---

## 📊 统计

- Python 文件: 2378+
- JS/TS 文件: 1901+
- 项目大小: 432MB

---

*最后更新: 2026-03-13*
