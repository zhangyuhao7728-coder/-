# 📗 001. 两数之和

**难度**: ⭐ (简单)

---

## 📝 题目描述

给定一个整数数组 `nums` 和一个整数目标值 `target`，找出和为目标值的两个整数，返回它们的数组下标。

---

## 📥 输入输出

```
输入: nums = [2, 7, 11, 15], target = 9
输出: [0, 1]
解释: nums[0] + nums[1] = 2 + 7 = 9
```

---

## 💡 解题思路

**方法1: 暴力枚举** O(n²)
```python
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```

**方法2: 哈希表** O(n) ✅ 推荐
```python
def two_sum(nums, target):
    seen = {}  # 值 -> 下标
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

---

## 🧪 测试用例

```json
{
  "test_cases": [
    {"input": {"nums": [2,7,11,15], "target": 9}, "output": [0,1]},
    {"input": {"nums": [3,2,4], "target": 6}, "output": [1,2]},
    {"input": {"nums": [3,3], "target": 6}, "output": [0,1]}
  ]
}
```

---

## 📊 复杂度

| 方法 | 时间 | 空间 |
|------|------|------|
| 暴力枚举 | O(n²) | O(1) |
| 哈希表 | O(n) | O(n) |

---

## ✅ 答案

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```
