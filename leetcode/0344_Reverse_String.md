# 344. Reverse String 反转字符串

**<font color=red>难度: Easy</font>**

## 刷题内容

> 原题链接

* https://leetcode-cn.com/problems/reverse-string/

> 内容描述

```
编写一个函数，其作用是将输入的字符串反转过来。输入字符串以字符数组 char[] 的形式给出。

不要给另外的数组分配额外的空间，你必须原地修改输入数组、使用 O(1) 的额外空间解决这一问题。

你可以假设数组中的所有字符都是 ASCII 码表中的可打印字符。

示例 1：

输入：["h","e","l","l","o"]
输出：["o","l","l","e","h"]

示例 2：

输入：["H","a","n","n","a","h"]
输出：["h","a","n","n","a","H"]
```

## 解题方案

> 方法一： 用reverse()，不过就没有练习的意义了。
>

```python
class Solution:
    def reverseString(self, s) -> None:
        """
        :param s: List:
        :return:
        """
        # 当然最简单的方法就是使用reverse
        # 但是就没有练习的意义了+
        s.reverse()
```



> 方法二： 利用双指针，进行头尾交换。
>

```python
class Solution:
    def reverseString(self, s) -> None:
        """
        :param s: List:
        :return:
        """
        i = 0
        j = len(s) - 1
        while i < j:
            s[i], s[j] = s[j], s[i]
            i += 1
            j -= 1
```



> 方法三：也是头尾交换，只不过只用到了一个指针。

```python
class Solution:
    def reverseString(self, s) -> None:

        length = len(s)
        for i in range(length // 2):
            s[i], s[length - 1 - i] = s[length - 1 - i], s[i]
```



> 方法四：同方法三，取末尾的值可以直接list[-1 - i]。

```python
class Solution:
    def reverseString(self, s) -> None:
        """
        :param s: List:
        :return:
        """
        length = len(s)
        for i in range(length // 2):
            s[i], s[-1 - i] = s[-1 - i], s[i]
```

