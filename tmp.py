import itertools


def trade(first: list[int], second: list[int]):
    """Exchange the smallest prefixes of first and second that have equal sum.

    >>> a = [1, 1, 3, 2, 1, 1, 4]
    >>> b = [4, 3, 2, 7]
    >>> trade(a, b) # Trades 1+1+3+2=7 for 4+3=7
    'Deal!'
    >>> a
    [4, 3, 1, 1, 4]
    >>> b
    [1, 1, 3, 2, 2, 7]
    >>> c = [3, 3, 2, 4, 1]
    >>> trade(b, c)
    'No deal!'
    """

    prefix_sum_first = [0] + list(itertools.accumulate(first))
    prefix_sum_second = [0] + list(itertools.accumulate(second))

    i = j = 1
    while i < len(prefix_sum_first) and j < len(prefix_sum_second):
        if prefix_sum_first[i] == prefix_sum_second[j]:
            first[:i], second[:j] = second[:j], first[:i]
            return "Deal!"
        elif prefix_sum_first[i] < prefix_sum_second[j]:
            i += 1
        else:
            j += 1

    return "No deal!"
