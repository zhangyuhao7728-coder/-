# OpenClaw 学习总结

## 一、基础概念

### 1. OpenClaw 是什么
- GitHub Star 全球排名#1（245,119颗Star）
- 自主执行：像真人一样操作浏览器、运行软件、读写文件
- 7×24小时待命：无需人工值守
- 本地运行：不受云端沙箱限制

### 2. 核心组件
| 组件 | 作用 |
|------|------|
| Gateway | 核心服务，负责调度 |
| Agents | AI 代理执行任务 |
| Channels | 对接 Telegram/飞书等 IM |
| Providers | 对接各种 AI 模型 |

---

## 二、本地部署

### 1. 安装
```bash
npm install -g openclaw
```

### 2. 常用命令
```bash
openclaw gateway start    # 启动
openclaw gateway stop     # 停止
openclaw gateway status   # 状态
openclaw gateway restart  # 重启
openclaw gateway install  # 安装开机自启
```

### 3. 开机自启
- LaunchAgent：Mac 系统服务，开机自动运行
- 安装：`openclaw gateway install`
- 状态：`launchctl list | grep openclaw`

---

## 三、模型配置

### 1. 本地模型（Ollama）
- 免费，离线可用
- 安装：`ollama run qwen3.5:9b`
- 配置 Provider：baseUrl + api: "ollama"

### 2. 云端模型
| 提供商 | 模型 | 特点 |
|--------|------|------|
| MiniMax | M2.5 | 便宜，支持长上下文 |
| 阿里云百炼 | Qwen-turbo/max | 国内稳定 |

### 3. Fallback 机制
```json
"model": {
  "primary": "云端模型",
  "fallbacks": ["备选云端", "本地模型"]
}
```
- 优先级：依次尝试，失败自动切换

---

## 四、备份与安全

### 1. 文件备份
- 备份脚本：`~/Scripts/backup_openclaw.sh`
- 备份位置：`~/Backups/openclaw/`
- 保留：3份历史备份

### 2. 断电保护
| 保护项 | 方案 |
|--------|------|
| 来电自动运行 | LaunchAgent |
| 模型自动切换 | Fallback 配置 |
| 文件备份 | 定时 rsync |

---

## 五、常用技巧

### 1. 清理多余文件
- 删除错误/备份文件保持目录整洁
- 用 trash 而非 rm（可恢复）

### 2. 模型切换原则
- 先确认再切换，不擅自操作
- 免费优先（本地模型）
- 避免产生不必要费用

### 3. 问题排查
- 查看日志：`tail -f /tmp/openclaw/openclaw-*.log`
- 检查状态：`openclaw status`
- 查看进程：`pgrep -fl openclaw`

---

## 六、待学习

- [ ] 云端部署（阿里云轻量服务器）
- [ ] Coding Plan 套餐使用
- [ ] MCP 工具集成
- [ ] 飞书/其他 IM 对接

---

*总结时间：2026-03-08*
