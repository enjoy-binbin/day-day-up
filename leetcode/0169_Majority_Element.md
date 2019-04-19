# 169. Majority Element 求众数

**<font color=red>难度: Easy</font>**

## 刷题内容

> 原题链接

* https://leetcode-cn.com/problems/majority-element/

> 内容描述

```
给定一个大小为 n 的数组，找到其中的众数。众数是指在数组中出现次数大于 ⌊ n/2 ⌋ 的元素。

你可以假设数组是非空的，并且给定的数组总是存在众数。

示例 1:

输入: [3,2,3]
输出: 3

示例 2:

输入: [2,2,1,1,1,2,2]
输出: 2

# 这个众数的定义emmmm，反正写就对了
```

## 解题方案

> 方法一：笨方法，循环遍历后将所有元素和出现的次数丢入字典，再根据字段的值排序。

```python
class Solution:
    def majorityElement(self, nums):
        # input: [2,2,1,1,1,2,2]
        lookup = {}  # {2: 4, 1: 3}
        for num in nums:
            if num not in lookup:  # lookup.get(num) == None
                lookup.update({num: 1})
            else:
                lookup[num] += 1

        # sorted后得到: [(2, 4), (1, 3)], 取[0][0]
        return sorted(lookup.items(), key=lambda x: x[1], reverse=True)[0][0]
```



> 方法二：取巧方法，排序后返回中间值。

```python
class Solution:
    def majorityElement(self, nums):
        return sorted(nums)[len(nums) // 2]
```



> 方法三：摩尔投票法，两两相互抵消，总是会留下那个众数。

```python
class Solution:
    def majorityElement(self, nums):
        cnt, ret = 0, 0  # count, return
        for num in nums:
            if cnt == 0:
                ret = num
            if num != ret:
                cnt -= 1
            else:
                cnt += 1
        return ret
```



> 方法四：使用Counter计数。

```python
class Solution:
    def majorityElement(self, nums) -> int:
        import collections
        ret = collections.Counter(nums)
        # print(ret)  # Counter({2: 4, 1: 3})
        # print(ret.most_common(1))  # [(2, 4)]
        return ret.most_common(1)[0][0]
```

