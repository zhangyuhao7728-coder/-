# 混合模式调度配置

## 简单任务路由（直接派发）

| 关键词 | Agent | 说明 |
|--------|-------|------|
| 调研 / 查 / 了解 | researcher | 技术调研、信息搜集 |
| 写代码 / 开发 / 实现 | engineer | 代码编写 |
| 审查 / 检查 / 验证 | reviewer | 质量检查 |
| 分析 / 数据 / 统计 | analyst | 数据分析 |
| 规划 / 拆解 / 任务 | planner | 任务规划 |

## 复杂任务（CEO 调度）

- 包含多个关键词
- 需要跨 Agent 协作
- 大型项目/需求不明确

## 示例

### 简单任务
```
"帮我调研 Python 异步编程"
→ 直接派给 researcher

"写一个计算器"
→ 直接派给 engineer

"检查这段代码有没有 Bug"
→ 直接派给 reviewer
```

### 复杂任务
```
"帮我做一个爬虫系统，包含数据存储和可视化"
→ CEO 调度：planner → researcher → engineer → reviewer → analyst
```

## 优先级

1. 关键词匹配 → 直接派发
2. 模糊匹配 → CEO 判断
3. 多 Agent 需求 → CEO 调度
