# AI Learning Team - 升级版架构

## 架构

```
ai-learning-team/
├── router/          # 路由层
├── agents/          # Agent层
├── memory/         # 记忆层
├── runtime/         # 运行时
├── tools/           # 工具层
└── infrastructure/ # 基础设施
```

## 核心特性

| 功能 | 限制 |
|------|------|
| 上下文 | 2000 tokens |
| Agent调用 | 6次 |
| 任务超时 | 120秒 |
| 日Token | 500万 |

## 使用

每次对话前输入: /new
