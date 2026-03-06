# Squad 架构设计说明

## 团队架构

```
         ┌─────────────┐
         │   CEO      │  ← 调度内核
         │ (张余浩)   │
         └──────┬──────┘
                │
    ┌───────────┼───────────┐
    │           │           │
┌───▼───┐  ┌──▼────┐  ┌──▼────┐
│Planner│  │Research│  │Engineer│
│ 规划  │  │ 调研   │  │ 开发   │
└───┬───┘  └───┬────┘  └───┬────┘
    │          │           │
    └──────────┼───────────┘
               │
         ┌─────▼─────┐
         │  Reviewer │
         │   审查    │
         └─────┬─────┘
               │
         ┌─────▼─────┐
         │  Analyst   │
         │   分析     │
         └───────────┘
```

## Agent 职责

| Agent | 职责 | 产出 |
|-------|------|------|
| CEO | 风险控制、异常处理 | 调度决策 |
| Planner | 任务规划、拆解 | 任务列表 |
| Researcher | 调研、信息搜集 | 调研报告 |
| Engineer | 代码实现 | 可运行代码 |
| Reviewer | 质量审查 | 审查报告 |
| Analyst | 数据分析 | 分析报告 |

## 协作模式

### 简单任务（直接派发）
- 调研 → researcher
- 代码 → engineer
- 审查 → reviewer
- 分析 → analyst

### 复杂任务（CEO调度）
```
Planner → Researcher → Engineer → Reviewer → Analyst
```

## 飞书群聊配置

计划为每个 Agent 创建独立飞书机器人，并建立群聊：

1. **CEO 群** - CEO + 全部 Agent
2. **产品组** - Planner + Engineer + Reviewer
3. **技术组** - Researcher + Engineer
4. **学习组** - 全部成员

## 通信机制

- **Telegram**: 主通信渠道
- **飞书**: 备用/群聊
- **Agent Reach**: 网络访问

## 状态管理

使用 `task_snapshot.json` 管理任务状态：
- status: 任务状态
- locked: 熔断锁定
- retry_count: 重试次数
- token_budget: 预算控制
