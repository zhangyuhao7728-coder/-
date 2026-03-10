# ⭐ 简单难度 - 数组

---

## 001. 两数之和

**题目**: 给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出和为目标值 target 的两个整数，并返回它们的数组下标。

**示例**:
```
输入: nums = [2,7,11,15], target = 9
输出: [0,1]
解释: nums[0] + nums[1] == 9
```

**代码模板**:
```python
def two_sum(nums: list[int], target: int) -> list[int]:
    # 在这里写你的代码
    pass
```

**答案**:
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

---

## 002. 最大子数组和

**题目**: 给你一个整数数组 nums ，请你找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

**示例**:
```
输入: nums = [-2,1,-3,4,-1,2,1,-5,4]
输出: 6
解释: 连续子数组 [4,-1,2,1] 的和最大，为 6
```

**代码模板**:
```python
def max_sub_array(nums: list[int]) -> int:
    # 在这里写你的代码
    pass
```

---

## 003. 买卖股票的最佳时机

**题目**: 给定一个数组 prices ，它的第 i 个元素 prices[i] 表示一支股票在某一天的最低价格。设计一个算法来计算你所能获取的最大利润。你可以尽可能地完成更多的交易（多次买卖一支股票）。

**示例**:
```
输入: prices = [7,1,5,3,6,4]
输出: 7
解释: 在第 2 天买入(价格=1)，第 3 天卖出(价格=5)，利润 = 4
     在第 4 天买入(价格=3)，第 5 天卖出(价格=6)，利润 = 3
     总利润 = 4 + 3 = 7
```

**代码模板**:
```python
def max_profit(prices: list[int]) -> int:
    # 在这里写你的代码
    pass
```

---

## 004. 合并两个有序数组

**题目**: 给你两个有序整数数组 nums1 和 nums2，请你将 nums2 合并到 nums1 中，使 nums1 成为一个有序数组。

**示例**:
```
输入: nums1 = [1,2,3], m = 3, nums2 = [2,5,6], n = 3
输出: [1,2,2,3,5,6]
```

**代码模板**:
```python
def merge(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    # 在这里写你的代码
    # 直接修改 nums1
    pass
```

---

## 005. 旋转数组

**题目**: 给你一个数组，将数组中的元素向右轮转 k 个位置，其中 k 是非负数。

**示例**:
```
输入: nums = [1,2,3,4,5,6,7], k = 3
输出: [5,6,7,1,2,3,4]
```

**代码模板**:
```python
def rotate(nums: list[int], k: int) -> None:
    # 在这里写你的代码
    # 直接修改 nums
    pass
```

---

## 进度追踪

| 题目 | 状态 | 难度 | 日期 |
|------|------|------|------|
| 001 两数之和 | ⬜ | ⭐ | - |
| 002 最大子数组和 | ⬜ | ⭐ | - |
| 003 买卖股票 | ⬜ | ⭐ | - |
| 004 合并有序数组 | ⬜ | ⭐ | - |
| 005 旋转数组 | ⬜ | ⭐ | - |

✅ = 已完成 | ⬜ = 未完成
