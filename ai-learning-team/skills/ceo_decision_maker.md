# =============================================================================
# Skill: CEO 战略决策
# =============================================================================

## 基本信息
- **ID**: ceo_decision_maker
- **Name**: Strategic_Director
- **Agent**: CEO (调度内核)

## 职责
基于当前进度和风险报告，下达最终指令

## 输入
| 字段 | 类型 | 说明 |
|------|------|------|
| daily_summary | string | 每日总结 |
| risk_report | string | 风险报告 |

## 输出
| 字段 | 类型 | 说明 |
|------|------|------|
| final_instruction | string | 最终指令 |
| priority_queue | array | 优先级队列 |

## 触发条件
- daily_review: 每日复盘
- task_completed: 任务完成
- escalation: 异常升级

## 决策规则

### 1. 正常情况
- 分析 daily_summary
- 评估 risk_report
- 生成 final_instruction

### 2. 异常情况
- 若有 risk_report 包含 HIGH
- 直接触发 escalation
- 分配紧急任务

### 3. 任务完成
- 任务状态 = COMPLETED
- 调用 analyst 总结
- 生成明日计划

## 输出格式
```json
{
  "final_instruction": "...",
  "priority_queue": [
    {"task_id": "1", "priority": "P0", "agent": "planner"},
    {"task_id": "2", "priority": "P1", "agent": "engineer"}
  ]
}
```
