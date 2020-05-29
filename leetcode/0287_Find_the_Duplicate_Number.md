# 287. Find the Duplicate Number 寻找重复数

**<font color=red>难度: Medium</font>**

## 刷题内容

> 原题链接

* https://leetcode-cn.com/problems/find-the-duplicate-number/

> 内容描述

```
给定一个包含 n + 1 个整数的数组 nums，其数字都在 1 到 n 之间（包括 1 和 n），可知至少存在一个重复的整数。假设只有一个重复的整数，找出这个重复的数。

示例 1:
输入: [1,3,4,2,2]
输出: 2

示例 2:
输入: [3,1,3,4,2]
输出: 3

说明：
不能更改原数组（假设数组是只读的）。
只能使用额外的 O(1) 的空间。
时间复杂度小于 O(n2) 。
数组中只有一个重复的数字，但它可能不止重复出现一次。
```

## 解题方案

> 方法一：排序后遍历，

```python
class Solution(object):
    def findDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        for i, v in enumerate(sorted(nums)):
            if i == v:
                return v
```



> 方法二：快慢双指针，有点绕，还有个二分法，算了算了。。。

```python
class Solution:
    def findDuplicate(self, nums):
        slow, fast = 0, 0
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break

        find = 0
        while True:
            find = nums[find]
            slow = nums[slow]
            if find == slow:
                return find
```