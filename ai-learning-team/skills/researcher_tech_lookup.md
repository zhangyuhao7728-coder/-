# =============================================================================
# Skill: Researcher 技术洞察
# =============================================================================

## 基本信息
- **ID**: researcher_tech_lookup
- **Name**: Knowledge_Informer
- **Agent**: Researcher (调研研究员)

## 职责
从外部文档和 GitHub 抓取最新的 AI 工具使用方法

## 输入
| 字段 | 类型 | 说明 |
|------|------|------|
| tech_keyword | string | 技术关键词 |
| search_depth | string | 搜索深度 (brief/detailed) |

## 输出
| 字段 | 类型 | 说明 |
|------|------|------|
| reference_doc | object | 参考文档 |
| tool_evaluation | array | 工具评估 |

## 工具
- web_search: 网络搜索
- web_fetch: 网页抓取
- agent-reach: Agent Reach 工具

## 触发条件
- research_requested: 收到调研请求

## 工作流程

### 1. 快速响应
- 10 分钟内给初步结论
- 30 分钟内给完整报告

### 2. 信息搜集
- 使用 Agent Reach 搜索
- 抓取官方文档
- 查找 GitHub 仓库

### 3. 筛选整理
- 提取关键 3-5 点
- 过滤重复信息
- 附上原文链接

### 4. 对比分析
- 多方案对比优缺点
- 给出明确推荐
- 说明推荐理由

## 输出格式
```json
{
  "reference_doc": {
    "topic": "Python 异步编程",
    "summary": "asyncio vs aiohttp vs httpx 对比",
    "sources": [
      {"title": "官方文档", "url": "https://..."},
      {"title": "GitHub", "url": "https://..."}
    ]
  },
  "tool_evaluation": [
    {
      "name": "asyncio",
      "pros": ["标准库", "性能高"],
      "cons": ["门槛高"],
      "recommendation": "有经验开发者首选"
    }
  ]
}
```
