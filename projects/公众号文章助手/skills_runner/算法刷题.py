#!/usr/bin/env python3
"""算法刷题Skill执行器"""
import random

def run(difficulty="简单", topic="数组"):
    problems = {
        "简单": [
            {"title": "两数之和", "difficulty": "简单", "topic": "数组"},
            {"title": "反转字符串", "difficulty": "简单", "topic": "字符串"},
            {"title": "合并两个有序链表", "difficulty": "简单", "topic": "链表"},
        ],
        "中等": [
            {"title": "两数相加", "difficulty": "中等", "topic": "数学"},
            {"title": "无重复字符的最长子串", "difficulty": "中等", "topic": "滑动窗口"},
        ],
        "困难": [
            {"title": "寻找两个正序数组的中位数", "difficulty": "困难", "topic": "数组"},
        ]
    }
    
    selected = random.choice(problems.get(difficulty, problems["简单"]))
    
    print(f"📝 每日算法题")
    print(f"题目: {selected['title']}")
    print(f"难度: {selected['difficulty']}")
    print(f"类型: {selected['topic']}")
    print(f"\n💡 解题思路:")
    print(f"1. 分析问题")
    print(f"2. 选择合适的数据结构")
    print(f"3. 编写代码")
    print(f"4. 测试验证")
    
    return selected

if __name__ == "__main__":
    import sys
    diff = sys.argv[1] if len(sys.argv) > 1 else "简单"
    topic = sys.argv[2] if len(sys.argv) > 2 else "数组"
    run(diff, topic)
