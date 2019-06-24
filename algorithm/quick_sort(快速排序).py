"""
@title: Quick Sort 快速排序
@file: quick_sort(快速排序).py
@desc: 利用快速排序对传进来的列表进行排序, 时间复杂度O(n * log n), 最坏: O(n**2)
@思路: 先选择基准值(pivot), 根据基准值将数组分成两个小数组, 再对这两数组进行快排
        层数O(log n), (最坏 O(n)层 ), 每层需要时间O(n), 平均最佳情况复杂度为O(n * log n)
"""


def quick_sort(array):
    """ 快速排序, 时间复杂度O(n * log n) """
    if len(array) < 2:
        # 空或者只有一个元素, 就是有序的, 直接返回
        return array

    pivot = array[0]
    less = [i for i in array[1:] if i <= pivot]  # 小于基准值的子数组
    greater = [i for i in array[1:] if i > pivot]  # 大于基准值的子数组
    return quick_sort(less) + [pivot] + quick_sort(greater)


if __name__ == '__main__':
    my_list = [1, 5, 7, 66, 32, 52, 10]
    print(quick_sort(my_list))
