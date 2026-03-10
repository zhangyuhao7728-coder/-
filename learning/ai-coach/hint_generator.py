#!/usr/bin/env python3
"""
💡 提示生成器
根据问题给出逐步提示
"""

class HintGenerator:
    def __init__(self):
        self.hints_db = {
            "两数之和": {
                "hint1": "可以使用哈希表来存储已经遍历过的数字",
                "hint2": "对于每个数字,检查target减去它是否在哈希表中",
                "hint3": "如果找到,返回两个数字的下标",
                "solution": "使用字典存储数字和下标,一次遍历完成"
            },
            "最大子数组和": {
                "hint1": "考虑使用动态规划",
                "hint2": "当前子数组和为负数时,不如重新开始",
                "hint3": "记录最大的子数组和",
                "solution": "Kadane算法:维护当前和和最大和"
            },
            "回文数判断": {
                "hint1": "可以将数字转换为字符串",
                "hint2": "字符串反转后与原字符串比较",
                "hint3": "或者只反转一半的数字",
                "solution": "数字反转法:比较原数字和反转后的数字"
            },
            "反转字符串": {
                "hint1": "可以使用双指针",
                "hint2": "从字符串两端交换字符",
                "hint3": "Python可以用切片[::-1]",
                "solution": "s = s[::-1] 或者双指针交换"
            },
            "合并两个有序数组": {
                "hint1": "从数组尾部开始",
                "hint2": "比较两个数组的尾部元素",
                "hint3": "从大到小依次放入",
                "solution": "双指针从后往前合并"
            }
        }
        
        self.generic_hints = [
            "仔细阅读题目要求",
            "考虑边界情况",
            "先尝试暴力解法,再优化",
            "画图帮助理解",
            "考虑使用数据结构哈希表"
        ]
    
    def get_hints(self, problem_title, level=1):
        """获取提示"""
        if problem_title in self.hints_db:
            hints = self.hints_db[problem_title]
            if level == 1:
                return hints.get("hint1", self._random_hint())
            elif level == 2:
                return hints.get("hint2", self._random_hint())
            elif level == 3:
                return hints.get("hint3", self._random_hint())
            elif level == 4:
                return hints.get("solution", "查看答案")
        
        return self._random_hint()
    
    def get_all_hints(self, problem_title):
        """获取所有提示"""
        if problem_title in self.hints_db:
            return self.hints_db[problem_title]
        return {
            "hint1": self._random_hint(),
            "hint2": self._random_hint(),
            "hint3": self._random_hint(),
            "solution": "参考答案解答"
        }
    
    def _random_hint(self):
        """随机通用提示"""
        import random
        return random.choice(self.generic_hints)
    
    def interactive_hints(self, problem_title):
        """交互式提示"""
        print(f"\n💡 {problem_title} 提示")
        print("=" * 40)
        
        hints = self.get_all_hints(problem_title)
        
        for i, (key, hint) in enumerate(hints.items(), 1):
            print(f"\n[{i}] {hint}")
            
            if i < len(hints):
                response = input("\n继续提示? (y/n): ").strip().lower()
                if response != 'y':
                    break

def main():
    generator = HintGenerator()
    
    print("💡 提示生成器")
    print("=" * 40)
    
    # 测试
    problem = "两数之和"
    for level in range(1, 5):
        hint = generator.get_hints(problem, level)
        print(f"Level {level}: {hint}")

if __name__ == "__main__":
    main()
