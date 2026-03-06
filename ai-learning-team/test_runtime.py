"""
Test Core Runtime
测试 Organization Core 运行时
"""

from organization_core.core_runtime import OrganizationCore


def ceo_agent(message: dict):
    """CEO Agent"""
    print(f"[CEO] 收到消息: {message['content']}")
    print("[CEO] 开始决策...")


def planner_agent(message: dict):
    """Planner Agent"""
    print(f"[Planner] 收到任务: {message['content']}")
    print("[Planner] 制定计划中...")


def researcher_agent(message: dict):
    """Researcher Agent"""
    print(f"[Researcher] 收到调研任务: {message['content']}")
    print("[Researcher] 搜索信息中...")


def engineer_agent(message: dict):
    """Engineer Agent"""
    print(f"[Engineer] 收到开发任务: {message['content']}")
    print("[Engineer] 编写代码中...")


def reviewer_agent(message: dict):
    """Reviewer Agent"""
    print(f"[Reviewer] 收到审查任务: {message['content']}")
    print("[Reviewer] 审查代码中...")


def analyst_agent(message: dict):
    """Analyst Agent"""
    print(f"[Analyst] 收到分析任务: {message['content']}")
    print("[Analyst] 分析数据中...")


def main():
    print("🚀 初始化 Organization Core...\n")
    
    # 创建核心
    core = OrganizationCore()
    
    # 注册所有 Agent
    print("📝 注册 Agent...\n")
    core.register_agent("ceo", ceo_agent)
    core.register_agent("planner", planner_agent)
    core.register_agent("researcher", researcher_agent)
    core.register_agent("engineer", engineer_agent)
    core.register_agent("reviewer", reviewer_agent)
    core.register_agent("analyst", analyst_agent)
    
    print(f"\n📋 已注册 Agents: {core.list_agents()}\n")
    
    # 测试各种消息
    test_messages = [
        {"content": "你好，今天怎么样？"},
        {"content": "帮我制定一个学习计划"},
        {"content": "研究一下最新的 AI 新闻"},
        {"content": "请帮我写一个 Python 脚本"},
        {"content": "帮我审查这段代码"},
        {"content": "分析一下这个月的学习数据"},
    ]
    
    print("=" * 50)
    print("开始测试消息路由...")
    print("=" * 50 + "\n")
    
    for msg in test_messages:
        print(f"\n📨 收到消息: {msg['content']}")
        print("-" * 30)
        core.receive_message(msg)
        print()


if __name__ == "__main__":
    main()
