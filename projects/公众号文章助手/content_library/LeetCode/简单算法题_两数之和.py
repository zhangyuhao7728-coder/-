#!/usr/bin/env python3
"""
LeetCode第一题：两数之和
难度: 简单 ⭐

题目描述：
给定一个整数数组 nums 和一个目标值 target，
请你在该数组中找出和为目标值 target 的两个整数，
返回它们的数组下标。

示例：
输入: nums = [2,7,11,15], target = 9
输出: [0, 1]
解释: nums[0] + nums[1] = 2 + 7 = 9

🎯 解题思路

方法1: 暴力枚举
- 遍历每个元素
- 检查target - 当前元素是否在数组中
- 时间复杂度: O(n²)

方法2: 哈希表（推荐）
- 用字典存储已遍历的元素
- 一遍遍历即可找到答案
- 时间复杂度: O(n)
"""

# ==================== 方法1: 暴力枚举 ====================
def two_sum_brute(nums, target):
    """
    暴力解法
    时间复杂度: O(n²)
    空间复杂度: O(1)
    """
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


# ==================== 方法2: 哈希表（推荐）==============
def two_sum_hash(nums, target):
    """
    哈希表解法
    时间复杂度: O(n)
    空间复杂度: O(n)
    """
    seen = {}  # 存储 {数值: 索引}
    
    for i, num in enumerate(nums):
        complement = target - num
        
        if complement in seen:
            return [seen[complement], i]
        
        seen[num] = i
    
    return []


# ==================== 测试 ====================
if __name__ == "__main__":
    # 测试用例
    test_cases = [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),
        ([3, 3], 6, [0, 1]),
    ]
    
    print("=" * 50)
    print("🧪 两数之和 测试")
    print("=" * 50)
    
    for nums, target, expected in test_cases:
        result = two_sum_hash(nums, target)
        status = "✅" if result == expected else "❌"
        print(f"{status} nums={nums}, target={target}")
        print(f"   预期: {expected}, 结果: {result}")
    
    print("\n" + "=" * 50)
    print("📊 复杂度分析")
    print("=" * 50)
    print("""
方法1: 暴力枚举
  时间: O(n²) - 两层循环
  空间: O(1)  - 只用常数空间

方法2: 哈希表 ⭐推荐
  时间: O(n)  - 一遍遍历
  空间: O(n)  - 哈希表存储
""")

    print("💡 关键点:")
    print("   - 用空间换时间")
    print("   - 一遍遍历，边存边查")
    print("   - target - num = 另一个数")
