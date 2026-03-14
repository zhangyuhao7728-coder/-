# AiToEarn 项目安装记录

**日期：** 2026-03-14

---

## 项目信息

- **名称：** AiToEarn
- **描述：** 基于AI的全平台社交媒体管理与内容分发工具
- **官网：** https://github.com/yikart/AiToEarn

---

## 功能特点

| 功能 | 说明 |
|------|------|
| 多平台分发 | 抖音、小红书、B站、TikTok、YouTube等 |
| AI内容生成 | 关键词生成标题、封面、文案、视频脚本 |
| 内容日历 | 排期管理，支持循环任务 |
| 趋势挖掘 | 分析账号数据，盯热点、看竞品 |
| 自动发布 | 定时通过官方接口发布 |

---

## 安装状态

| 步骤 | 状态 |
|------|------|
| 克隆项目 | ✅ 完成 |
| Docker检查 | ✅ 已安装 (v29.2.1) |
| 环境配置 | ✅ 已创建 |
| Docker启动 | ⏳ 需要手动启动 |

---

## 待完成步骤

### 1. 启动Docker

打开Docker应用：
```bash
open -a Docker
# 或在Launchpad中搜索Docker打开
```

### 2. 配置环境变量

编辑 `.env` 文件，修改以下必需项：
- MONGODB_PASSWORD
- REDIS_PASSWORD
- JWT_SECRET
- INTERNAL_TOKEN
- NEXT_PUBLIC_API_URL
- APP_DOMAIN

### 3. 启动服务

```bash
cd ~/项目/Ai学习系统/projects/AiToEarn
docker compose up -d
```

### 4. 访问服务

| 服务 | 地址 |
|------|------|
| 前端 | http://localhost:3000 |
| 后端 | http://localhost:3002 |
| Channel | http://localhost:7001 |

---

## 项目位置

```
~/项目/Ai学习系统/projects/AiToEarn/
```

---

*记录时间：2026-03-14*

---

## 2026-03-14 更新

### 安装尝试

| 步骤 | 状态 |
|------|------|
| 克隆项目 | ✅ 完成 |
| Docker | ✅ 运行中 |
| 环境配置 | ✅ 完成 |
| 拉取镜像 | ❌ Docker Hub网络问题 |

### 问题

Docker Hub无法访问，可能是：
- 网络被墙
- 限流

### 解决方案

1. 使用VPN
2. 配置国内镜像
3. 等待后重试

---

## 2026-03-14 晚 更新

### 问题

Docker Hub部分镜像拉取失败：
- ✅ redis:7-alpine - 成功
- ❌ mongo:7 - 失败
- ❌ aitoearn镜像 - 失败

### 解决方案

**方案1：使用国内镜像**
```bash
cd ~/项目/Ai学习系统/projects/AiToEarn
docker compose -f docker-compose-cn.yml up -d
```

**方案2：等待后重试**
- 网络不稳定，等待一段时间后再试

**方案3：手动构建**
- 从源码构建镜像（需要较长时间）


---

## 2026-03-14 21:59

### 状态

| 镜像 | 状态 |
|------|------|
| redis:7-alpine | ✅ 已下载 |
| mongo:7 | ❌ 失败 |
| aitoearn系列 | ❌ 失败 |

### 说明

Docker Hub网络持续不稳定，需要：
1. 等待网络恢复
2. 或使用国内镜像源

---

## 2026-03-14 22:10

### 问题分析

| 问题 | 说明 |
|------|------|
| Docker Hub | 网络持续不稳定 |
| ARM64支持 | 镜像无Apple Silicon版本 |
| QEMU | 需要网络下载镜像 |

### 当前可用镜像

| 镜像 | 状态 |
|------|------|
| mongo:7.0 (国内) | ✅ 已下载 |
| redis:7-alpine (国内) | ✅ 已下载 |
| aitoearn/* | ❌ Docker Hub访问失败 |

### 解决方案

1. **等待网络恢复** - Docker Hub恢复正常后重试
2. **从源码构建** - 需要较长编译时间
3. **使用类似工具** - 寻找替代方案

