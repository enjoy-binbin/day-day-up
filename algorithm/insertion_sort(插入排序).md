#### 直接插入排序

##### 一、前言

直接插入排序是一种最简单的插入排序。

直接插入排序是稳定算法，因为在排序过程中，相同元素前后顺序不会改变



##### 二、排序思想

每一趟将一个待排序的元素，按照其值的大小插入到有序数组中的合适位置里，直到最后全部插入完成。时间复杂度O(n**2)，最好的情况下是正序的O(n)，空间复杂度O(1)

![bubble_sort](./images/insertion_sort.gif)



##### 三、代码实现

```python
def insertion_sort(array):
    length = len(array)
    if length < 2:
        return array

    for i in range(1, length):
        temp = array[i]  # 每轮取出的元素
        j = i - 1  # 跟前面的有序数组对比

        while j >= 0 and temp < array[j]:
            # 满足while循环指针则前移, 元素后移
            array[j + 1] = array[j]
            j -= 1
        # 然后将元素插入到合适的位置
        array[j + 1] = temp
    return array


if __name__ == '__main__':
    my_list = [5, 1, 0, 66, 32, 52, 10]
    print(insertion_sort(my_list))
```



##### 四、说明点

直接的优化，上面在查找合适位置的时候，前面都是有序的，所以其实可以使用二分查找加速查找的速度，二分查找中返回合适位置的索引。理解是好理解，代码就会有点难看懂

```python
def binary_search(array, end, value):
    left = 0
    right = end - 1
    while left <= right:
        middle = left + (right - left) // 2
        if array[middle] >= value:
            right = middle - 1
        else:
            left = middle + 1

    return left if left < end else -1


def insertion_sort(array):
    length = len(array)
    if length < 2:
        return array

    for i in range(1, length):
        j = i - 1
        temp = array[i]
        insert_index = binary_search(array, i, temp)
        
        if insert_index != -1:
            while j >= insert_index:
                array[j + 1] = array[j]
                j -= 1
            array[j + 1] = temp
    return array


if __name__ == '__main__':
    my_list = [5, 1, 0, 66, 32, 52, 10]
    print(insertion_sort(my_list))
```



