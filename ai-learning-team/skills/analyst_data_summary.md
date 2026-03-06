# =============================================================================
# Skill: Analyst 学习复盘
# =============================================================================

## 基本信息
- **ID**: analyst_data_summary
- **Name**: Knowledge_Synthesizer
- **Agent**: Analyst (分析师)

## 职责
归纳今日所有 Agent 的交互日志，提取核心知识点存入知识库

## 输入
| 字段 | 类型 | 说明 |
|------|------|------|
| runtime_logs | array | 运行时日志 |
| task_history | array | 任务历史 |

## 输出
| 字段 | 类型 | 说明 |
|------|------|------|
| kb_markdown | string | 知识库 Markdown |
| learning_progress | object | 学习进度 |

## 模板
使用 `templates/MEMORY.md` 格式

## 触发条件
- daily_review: 每日复盘
- task_completed: 任务完成

## 工作流程

### 1. 收集日志
- 获取所有 Agent 的 runtime_logs
- 获取 task_history

### 2. 数据分析
- 统计任务完成率
- 分析耗时分布
- 识别问题模式

### 3. 知识点提取
- 从成功任务提取经验
- 从失败任务提取教训
- 整理成结构化知识

### 4. 知识沉淀
- 更新 MEMORY.md
- 分类存储
- 便于后续查询

## 输出格式
```json
{
  "kb_markdown": "# 知识库更新\n\n## 今日学习\n\n### Python 基础\n- 变量类型\n- 条件语句\n\n### 经验\n1. 先理解需求再动手\n2. 代码要加注释\n\n## 教训\n1. 避免过度设计\n",
  "learning_progress": {
    "tasks_completed": 5,
    "tasks_total": 7,
    "completion_rate": "71%",
    "time_spent": "3.5h",
    "skills_improved": ["Python", "爬虫"],
    "next_focus": "Web 开发"
  },
  "summary": {
    "total_interactions": 23,
    "successful_flows": 18,
    "failed_flows": 2,
    "blocked_flows": 3
  }
}
```

## 知识库更新规则

### 成功模式
- 提取可复用的方法
- 记录最佳实践
- 保存代码示例

### 失败教训
- 分析失败原因
- 记录避免方法
- 更新检查清单
