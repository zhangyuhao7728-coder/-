# 🤖 AI Model Manager

> 统一管理本地 + 云端 AI 模型

## 📋 简介

一个简洁的 AI 模型管理面板，支持本地模型（Ollama）和云端模型（MiniMax等）的分离管理与智能路由。

## 🚀 快速开始

```bash
# 进入目录
cd ~/项目/Ai学习系统/ai-control-plane

# 启动服务
npm start
```

访问 **http://localhost:3001**

## 📡 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/models` | GET | 获取所有模型 |
| `/api/local/switch` | POST | 切换本地模型 |
| `/api/cloud/switch` | POST | 切换云端模型 |
| `/api/local/add` | POST | 添加本地模型 |
| `/api/cloud/add` | POST | 添加云端模型 |
| `/api/chat` | POST | 对话测试 |
| `/api/stats` | GET | 统计数据 |

## 📊 功能

- 💻 本地模型管理 (Ollama)
- ☁️ 云端模型管理 (MiniMax)
- 🔄 一键切换模型
- 📥 扫描 Ollama 模型
- 📥 从 OpenClaw 导入云端模型
- 📈 使用统计

## 📁 项目结构

```
ai-control-plane/
├── server.js          # 主服务
├── config.json         # 配置文件
├── package.json        # 依赖
├── public/
│   └── index.html     # 管理界面
├── providers/         # 模型提供者
├── router/            # 路由
├── utils/            # 工具
└── logs/             # 日志
```

## ⚙️ 配置

编辑 `config.json`:

```json
{
  "local_model": "qwen3.5:9b",
  "cloud_model": "minimax_m25",
  "models": { ... },
  "cloud_models": { ... }
}
```

## 🧠 智能路由

- **简单任务** → 本地模型 (免费、快速)
- **复杂任务** → 云端模型 (高质量)

---

**Version**: 2.1  
**Author**: AI Assistant  
**Date**: 2026-03-10
