"""
@title: Selection Sort 选择排序
@file: selection_sort(选择排序).py
@desc: 利用选择排序对传进来的列表进行排序
@思路: 先选择找出最小的元素, 然后找第二小的, 依次类推直到最后排好序, 就为选择排序
        第一次需要检查n次, 之后的次数是n-1, n-2, ... , 2, 1, 平均检查次数为 0.5n
        时间复杂度O(n * 0.5 * n) 省略常数后等于 O(n**2)
"""


def find_smallest_item(array):
    """ 辅助函数, 查找列表中最小的元素, 返回下标 """
    smallest_item = array[0]  # 假定第一个元素是最小值
    smallest_index = 0
    for i in range(1, len(array)):
        if array[i] < smallest_item:
            smallest_item = array[i]
            smallest_index = i

    return smallest_index


def selection_sort(array):
    """ 选择排序, 时间复杂度O(n * 0.5 * n) == O(n**2) """
    new_array = []
    for i in range(len(array)):
        # pop出原数组中最小值, 并append到新数组中
        smallest_index = find_smallest_item(array)
        new_array.append(array.pop(smallest_index))

    return new_array

if __name__ == '__main__':
    my_list = [1, 5, 7, 66, 32, 52, 10]
    print(selection_sort(my_list))
