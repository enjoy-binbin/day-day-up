# 945. Minimum Increment to Make Array Unique 使数字唯一的最小增量

**<font color=red>难度: Midumn</font>**

## 刷题内容

> 原题链接

* https://leetcode-cn.com/problems/minimum-increment-to-make-array-unique/

> 内容描述

```
给定整数数组 A，每次 move 操作将会选择任意 A[i]，并将其递增 1。

返回使 A 中的每个值都是唯一的最少操作次数。

示例 1:
输入：[1,2,2]
输出：1
解释：经过一次 move 操作，数组将变为 [1, 2, 3]。

示例 2:
输入：[3,2,1,2,1,7]
输出：6
解释：经过 6 次 move 操作，数组将变为 [3, 4, 1, 2, 5, 7]。
可以看出 5 次或 5 次以下的 move 操作是不能让数组的每个值唯一的。

提示：
  0 <= A.length <= 40000
  0 <= A[i] < 40000
```

## 解题方案

> 方法一：排序后遍历数组，若当前元素小于等于它前一个元素，则将其变为前一个数+1，贪心算法

```python
class Solution:
    def minIncrementForUnique(self, A):
        A.sort()
        res = 0
        for i in range(1, len(A)):
            if A[i] <= A[i - 1]:
                # 小于或者相等就把当前数字变成前一个数字+1
                res += A[i - 1] - A[i] + 1
                A[i] = A[i - 1] + 1
        return res
```