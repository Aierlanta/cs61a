from itertools import islice
from typing import Iterator


HW_SOURCE_FILE = __file__


def insert_items(lst: list, entry: int, elem: int):
    """Inserts elem into lst after each occurrence of entry and then returns lst.

    >>> test_lst = [1, 5, 8, 5, 2, 3]
    >>> new_lst = insert_items(test_lst, 5, 7)
    >>> new_lst
    [1, 5, 7, 8, 5, 7, 2, 3]
    >>> test_lst
    [1, 5, 7, 8, 5, 7, 2, 3]
    >>> double_lst = [1, 2, 1, 2, 3, 3]
    >>> double_lst = insert_items(double_lst, 3, 4)
    >>> double_lst
    [1, 2, 1, 2, 3, 4, 3, 4]
    >>> large_lst = [1, 4, 8]
    >>> large_lst2 = insert_items(large_lst, 4, 4)
    >>> large_lst2
    [1, 4, 4, 8]
    >>> large_lst3 = insert_items(large_lst2, 4, 6)
    >>> large_lst3
    [1, 4, 6, 4, 6, 8]
    >>> large_lst3 is large_lst
    True
    >>> # Ban creating new lists
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'insert_items',
    ...       ['List', 'ListComp', 'Slice'])
    True
    """
    i = 0  # 初始化一个索引变量
    while i < len(lst):  # 循环遍历列表
        if lst[i] == entry:  # 如果当前元素等于 entry
            lst.insert(i + 1, elem)  # 在它后面插入 elem
            i += 1  # 增加索引，跳过插入的元素
        i += 1  # 增加索引，继续遍历
    return lst  # 返回修改后的列表


def count_occurrences(t, n, x):
    """Return the number of times that x appears in the first n elements of iterator t.

    >>> s = iter([10, 9, 10, 9, 9, 10, 8, 8, 8, 7])
    >>> count_occurrences(s, 10, 9)
    3
    >>> s2 = iter([10, 9, 10, 9, 9, 10, 8, 8, 8, 7])
    >>> count_occurrences(s2, 3, 10)
    2
    >>> s = iter([3, 2, 2, 2, 1, 2, 1, 4, 4, 5, 5, 5])
    >>> count_occurrences(s, 1, 3)
    1
    >>> count_occurrences(s, 3, 2)
    3
    >>> next(s)
    1
    >>> s2 = iter([4, 1, 6, 6, 7, 7, 8, 8, 2, 2, 2, 5])
    >>> count_occurrences(s2, 6, 6)
    2
    """
    return sum(i == x for i in islice(t, 0, n))


def repeated(t, k):
    """Return the first value in iterator T that appears K times in a row.
    Iterate through the items such that if the same iterator is passed into
    the function twice, it continues in the second call at the point it left
    off in the first.

    >>> s = iter([10, 9, 10, 9, 9, 10, 8, 8, 8, 7])
    >>> repeated(s, 2)
    9
    >>> s2 = iter([10, 9, 10, 9, 9, 10, 8, 8, 8, 7])
    >>> repeated(s2, 3)
    8
    >>> s = iter([3, 2, 2, 2, 1, 2, 1, 4, 4, 5, 5, 5])
    >>> repeated(s, 3)
    2
    >>> repeated(s, 3)
    5
    >>> s2 = iter([4, 1, 6, 6, 7, 7, 8, 8, 2, 2, 2, 5])
    >>> repeated(s2, 3)
    2
    """
    assert k > 1
    # it = next(t)
    # bak = k

    # def helper(t,k,it):
    #     if k == 1:
    #         return it
    #     else:
    #         i = next(t)
    #         if it == i:
    #             k -= 1
    #         if it != i:
    #             k = bak
    #             it = i
    #         return helper(t,k,it)
    # return helper(t,k,it)

    it = next(t)
    bak = k

    def helper(t: Iterator[int], k: int, it: int):
        if k == 1:
            return it
        i = next(t)
        if it == i:
            return helper(t, k - 1, it)
        if it != i:
            return helper(t, bak, i)

    return helper(t, k, it)

    """
    assert k > 1
    # 定义一个辅助函数，它接受一个迭代器，一个计数器，和一个上一个值作为参数
    def helper(t, count, prev):
        # 从迭代器中获取下一个值，如果没有则抛出异常
        try:
            i = next(t)
        except StopIteration:
            raise ValueError("No value appears {} times in a row".format(k))
        # 如果当前值和上一个值相同，那么计数器加一
        if i == prev:
            count += 1
        # 否则，计数器重置为一
        else:
            count = 1
        # 如果计数器达到了 k，那么返回当前值
        if count == k:
            return i
        # 否则，递归调用辅助函数，继续查找
        else:
            return helper(t, count, i)

    # 调用辅助函数，初始计数器为零，初始上一个值为 None
    return helper(t, 0, None)
    """

    # cur = 1 # 相同数
    # it = next(t) # “第一个元素”
    # for i in t: # line 25 <- current line in the debugger
    #     # assert cur < k
    #     if it == i: # 如果第一个元素等于遍历元素
    #         cur += 1 # 相同数 +1
    #     if it != i:  # 如果第一个元素不等于遍历元素
    #         cur = 1  # 相同数还是等于1（不变）
    #         it = i # “第一个元素”后移（变成第二个元素）
    #     if cur == k: # cur等于k ，返回cur
    #         return it


def partial_reverse(lst, start):
    """Reverse part of a list in-place, starting with start up to the end of
    the list.

    >>> a = [1, 2, 3, 4, 5, 6, 7]
    >>> partial_reverse(a, 2)
    >>> a
    [1, 2, 7, 6, 5, 4, 3]
    >>> partial_reverse(a, 5)
    >>> a
    [1, 2, 7, 6, 5, 3, 4]
    """
    "*** YOUR CODE HERE ***"


def index_largest(seq):
    """Return the index of the largest element in the sequence.

    >>> index_largest([8, 5, 7, 3 ,1])
    0
    >>> index_largest((4, 3, 7, 2, 1))
    2
    """
    assert len(seq) > 0
    "*** YOUR CODE HERE ***"


def pizza_sort(lst):
    """Perform an in-place pizza sort on the given list, resulting in
    elements in descending order.

    >>> a = [8, 5, 7, 3, 1, 9, 2]
    >>> pizza_sort(a)
    >>> a
    [9, 8, 7, 5, 3, 2, 1]
    """
    pizza_sort_helper(________, ________)


def pizza_sort_helper(lst, start):
    if _______________:
        partial_reverse(________, ________)
        partial_reverse(________, ________)
        _______________(________, ________)
