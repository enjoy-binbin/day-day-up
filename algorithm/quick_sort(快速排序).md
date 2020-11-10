#### 快速排序

##### 一、前言

快速排序是速度很快的一种排序，手写快排应该也是基本功了吧hh

快排是不稳定算法，因为在排序过程中，相同元素会根据基准值分区情况的不同，而改变顺序



##### 二、排序思想

先选择基准值(pivot)，根据基准值将数组分成两个小数组，再对这两数组进行快排，层数O(log n)，(最坏 O(n)层 )，每层需要时间O(n)，平均最佳情况复杂度为O(n * log n)，空间复杂度O(log n)

基准值左边都是比它小的数，右边都是比它大的数，然后对左右两边分别继续进行递归的快排

![bubble_sort](./images/quick_sort.gif)



##### 三、代码实现

```python
def quick_sort(array):
    """ 快速排序(升序), 时间复杂度O(n * log n) """
    if len(array) < 2:
        # 空或者只有一个元素, 就是有序的, 直接返回
        return array

    pivot = array[0]
    less = [i for i in array[1:] if i <= pivot]  # 小于基准值的子数组
    greater = [i for i in array[1:] if i > pivot]  # 大于基准值的子数组
    return quick_sort(less) + [pivot] + quick_sort(greater)  # 递归快排


if __name__ == '__main__':
    my_list = [1, 5, 7, 66, 32, 52, 10]
    print(quick_sort(my_list))

```



##### 四、说明点

快排的实现也有很多种方法，理解思想即可。
