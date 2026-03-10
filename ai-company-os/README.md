# 🤖 AI 公司操作系统

## 系统架构

```
ai-company-os/
│
├── ai-control-plane/        # 模型控制平面 (端口 3001)
│   ├── server.js           # 统一 API 网关
│   ├── config.json        # 模型配置
│   ├── stats.json         # 请求统计
│   ├── providers/          # 模型提供商
│   │   ├── ollama.js     # 本地模型
│   │   ├── openai.js     # OpenAI
│   │   └── generic.js     # 通用 API
│   ├── router/            # 智能路由
│   │   └── router.js     # 轮询调度
│   └── utils/            # 工具
│       ├── config.js     # 热更新配置
│       ├── logger.js     # 日志
│       └── queue.js      # 请求队列
│
├── tasks/                 # 任务系统
│   └── scheduler.js      # 定时任务
│
├── agents/               # AI 代理团队
│   ├── planner/         # 规划师
│   ├── engineer/        # 工程师
│   ├── researcher/      # 研究员
│   └── reviewer/        # 审核员
│
├── integrations/         # 集成
│   ├── telegram/        # Telegram 机器人
│   ├── discord/        # Discord 集成
│   └── web/            # Web 接口
│
└── dashboard/          # 管理面板
    └── index.html     # 控制台
```

## 核心功能

### 1. 模型控制平面
- 统一 API: `POST /v1/chat`
- 多模型支持: Ollama, OpenAI, Generic
- 智能路由 + Fallback
- 请求队列防并发
- 配置热更新

### 2. 任务调度
- 定时任务
- 自动重试
- 任务队列

### 3. AI 代理团队
- 多代理协作
- 自动任务分配
- 结果汇总

### 4. 集成
- Telegram 机器人
- Web 控制台
- API 接口

## 启动

```bash
# 启动模型控制平面
cd ai-control-plane
node server.js

# 访问
# API: http://localhost:3001/v1/chat
# Dashboard: http://localhost:3001
```

## 使用

```bash
# 对话
curl -X POST http://localhost:3001/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt":"你好"}'
```

---

*AI 公司操作系统 v1.0*
