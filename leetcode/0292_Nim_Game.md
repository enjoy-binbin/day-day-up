# 292. Nim Game Nim游戏

**<font color=red>难度: Easy</font>**

## 刷题内容

> 原题链接

* https://leetcode-cn.com/problems/nim-game/

> 内容描述

```
你和你的朋友，两个人一起玩 Nim游戏：桌子上有一堆石头，每次你们轮流拿掉 1 - 3 块石头。 拿掉最后一块石头的人就是获胜者。你作为先手。

你们是聪明人，每一步都是最优解。 编写一个函数，来判断你是否可以在给定石头数量的情况下赢得游戏。

示例:

输入: 4
输出: false 
解释: 如果堆中有 4 块石头，那么你永远不会赢得比赛；
     因为无论你拿走 1 块、2 块 还是 3 块石头，最后一块石头总是会被你的朋友拿走。
```

## 解题方案

> 思路和方法

```
对于总是优先开始的那方

    有一到三块，总是赢
    有四块，总是输

    五块：
    	总是赢，拿一块，对方剩四块，我方赢
    六块：
    	总是赢，拿两块，对方剩四块，我方赢
        拿一块，对方五块，对方赢
        拿三块，对方三块，对方赢
    七块：
    	总是赢，拿三块，对方剩四块，我方赢
    	拿一块，对方六块，对方赢
        拿三块，对方四块，对方赢
      
总结后：
    n <= 3 能赢 √
    n == 4 总输
    n = 5,6,7 总赢
    n == 8， 先手如何选，总可以转成5,6,7 对方总会赢

所以 n % 4 == 0 时候，先手必输
```

```python
class Solution(object):
    def canWinNim(self, n):
        """
        :type n: int
        :rtype: bool
        """
        return n % 4 != 0
```