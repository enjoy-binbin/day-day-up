# 409. Longest Palindrome 最长回文串

**<font color=red>难度: Easy</font>**

## 刷题内容

> 原题链接

* https://leetcode-cn.com/problems/longest-palindrome/

> 内容描述

```
给定一个包含大写字母和小写字母的字符串，找到通过这些字母构造成的最长的回文串。

在构造过程中，请注意区分大小写。比如 "Aa" 不能当做一个回文字符串。

注意:
假设字符串的长度不会超过 1010。

示例 1:

输入:
"abccccdd"

输出:
7

解释:
我们可以构造的最长的回文串是"dccaccd", 它的长度是 7。
```

## 解题方案

> 方法一： 利用列表，如果元素出现两次就相互抵消，最后判断列表长度。
>

```python
class Solution:
    def longestPalindrome(self, s: str) -> int:
        single_list = []  # 用来存储只出现一次的字符
        count = 0
        for i in s:
            if i not in single_list:
                # 如果不在, 就将字符添加进列表
                single_list.append(i)
            else:
                # 如果在, 就移除这个字符, 同时count加2, 因为两个相同的字符可以构成回文
                single_list.remove(i)
                count += 2

        # 最后判断列表的长度, 里面存储的都是 只出现过一次的字符
        # 当长度大于等于1的时候, 说明可以有多一个字符可以 构成回文数的中心
        # 长度为0时, 直接返回count
        if len(single_list) >= 1:
            return count + 1
        else:
            return count
```



> 方法二： 使用Counter计数，然后判断元素出现次数的奇偶性。
>

```python
class Solution:
    def longestPalindrome(self, s):
        import collections

        # lookup: Counter({'c': 4, 'd': 2, 'a': 1, 'b': 1})
        lookup = collections.Counter(s)
        count, one = 0, 0  # one 代表是否存在一个char，其出现次数为奇数

        for k, v in lookup.items():
            if v % 2 == 0:
                count += v  # 出现偶数次数的可以全拿去回文
            else:
                count += v - 1  # 出现奇数次数的拿掉一个, 剩下的偶数次数就可以拿去回文
                one = 1  # 有出现过奇数元素
        return count + one  # 多的一个奇数元素, 可以放到回文数的中间
```