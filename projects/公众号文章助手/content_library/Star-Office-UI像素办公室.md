# Star-Office-UI - 像素办公室

**来源：** 逛逛GitHub  
**日期：** 2026年3月6日  
**作者：** Simon_阿文、海辛

---

## 项目简介

**Star-Office-UI** 是一个给AI团队打造的像素办公室可视化工具。

- **Star:** 1.5k+
- **定位:** 多Agent可视化状态看板
- **风格:** 复古像素风RPG小办公室

---

## 核心功能

### 1. 状态可视化

AI Agent会实时显示工作状态：

| 状态 | 行为 |
|------|------|
| 思考/执行中 | 自动走到工作区敲键盘 |
| 空闲/待机 | 休息区喝咖啡/摸鱼 |
| 代码报错 | Bug区面壁思过 |

### 2. 拟人化工作小记

- 左下角动态展示AI工作日记
- 用第一人称口吻总结完成的任务

### 3. 多智能体串门

- 邀请其他AI角色作为访客
- 直观呈现多Agent协同工作

### 4. 移动端支持

- 完美适配手机屏幕
- 随时随地监工AI

---

## 安装和使用

### 1. 下载仓库

```bash
git clone https://github.com/ringhyacinth/Star-Office-UI.git
cd Star-Office-UI
```

### 2. 安装依赖

```bash
python3 -m pip install -r backend/requirements.txt
```

### 3. 准备状态文件

```bash
cp state.sample.json state.json
```

### 4. 启动后端

```bash
cd backend
python3 app.py
```

### 5. 访问

打开浏览器访问：http://127.0.0.1:18791

---

## 项目原理

用极简HTTP状态服务 + 前端像素小场景，把AI Agent的状态文件实时翻译成办公室里角色的走动和动画。

---

## 适用场景

- 监控OpenClaw Agent运行状态
- 多Agent协同可视化
- 有趣的AI工作状态展示

---

## 相关链接

- GitHub: https://github.com/ringhyacinth/Star-Office-UI

---

*记录时间：2026-03-14*
