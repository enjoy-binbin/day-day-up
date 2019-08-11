### Dict() or {}

一点疑问，在Python中构造字典，使用dict()或者{}，都是可以的，但是 哪个会更好一些嘞。



以前我一直都是用的 {}，构造字典，不过在某个Pycharm版本中（现在用的2019.1.3就没），它对我 使用{}构造字典进行了提示，对于稍微有点强迫症的我来讲，看到那些都是会想办法去掉，跳过这些，在那时Pycharm中希翼的构造方式应该是 dict()，起码我那时这样构造便没有了提示，所以这个问题印象深刻直到现在。



那构造字典到底是用哪种好呢?

直接说结论，{}的构造方式会比dict()快，dict()审美可读性较好

具体参考下面这篇文章，大佬对结论的印证的严谨性，不过是篇老文章了，我没看完。

https://doughellmann.com/blog/2012/11/12/the-performance-impact-of-using-dict-instead-of-in-cpython-2-7-2/



#### 在timeit模块下的表现

有点惊讶，在创建空字典的情况下，速度差异差不多有三倍

```powershell
>>> from timeit import timeit
>>>
>>> timeit("dic = dict()")
0.07471252002504566
>>>
>>> timeit("dic = {}")
0.025534691055437264

>>> timeit("dic = dict()")
0.07536528272464693
>>>
>>> timeit("dic = {}")
0.025898268938931324
>>>
```

在填充字典的情况下，速度差距还是挺大的

```powershell
>>> timeit("dic = dict(name='binbin', age=22, gender='man')")    
0.20612860300389002                                              
>>>                                                              
>>> timeit("dic = {'name':'binbin', 'age':22, 'gender':'man'}")  
0.08020666685877131                                              
                  
>>> timeit("dic = dict(name='binbin', age=22, gender='man')")
0.20618913853923004
>>>
>>> timeit("dic = {'name':'binbin', 'age':22, 'gender':'man'}")
0.08063843838749563
>>>
```



#### 语法差异

对于写法可读性来看，在我看来其实相差不大

```python
dic = dict(
	name='binbin',
	age=22,
	gender='man'
)

dic = {
    'name': 'binbin',
    'age': 22,
    'gender': 'man'
}
```



#### 结论

当然对于两者的比较，还需要从更多方面去比较，所以我用{}