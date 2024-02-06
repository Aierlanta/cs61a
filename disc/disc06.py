# Tree ADT
def tree(label, branches=[]):
    """Construct a tree with the given label value and a list of branches."""
    for branch in branches:
        assert is_tree(branch), "branches must be trees"
    return [label] + list(branches)


def label(tree):
    """Return the label value of a tree."""
    return tree[0]


def branches(tree):
    """Return the list of branches of the given tree."""
    return tree[1:]


def is_tree(tree):
    """Returns True if the given tree is a tree, and False otherwise."""
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True


def is_leaf(tree):
    """Returns True if the given tree's list of branches is empty, and False
    otherwise.
    """
    return not branches(tree)


def print_tree(t, indent=0):
    """Print a representation of this tree in which each node is
    indented by two spaces times its depth from the root.

    >>> print_tree(tree(1))
    1
    >>> print_tree(tree(1, [tree(2)]))
    1
      2
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> print_tree(numbers)
    1
      2
      3
        4
        5
      6
        7
    """
    print("  " * indent + str(label(t)))
    for b in branches(t):
        print_tree(b, indent + 1)


def copy_tree(t):
    """Returns a copy of t. Only for testing purposes.

    >>> t = tree(5)
    >>> copy = copy_tree(t)
    >>> t = tree(6)
    >>> print_tree(copy)
    5
    """
    return tree(label(t), [copy_tree(b) for b in branches(t)])

############################################# 
               # start #
#############################################
def add_this_many(x: int, el: int, s: list):
    """Adds el to the end of s the number of times x occurs in s.
    >>> s = [1, 2, 4, 2, 1]
    >>> add_this_many(1, 5, s)
    >>> s
    [1, 2, 4, 2, 1, 5, 5]
    >>> add_this_many(2, 2, s)
    >>> s
    [1, 2, 4, 2, 1, 5, 5, 2, 2]
    """
    count = s.count(x)  # x出现的次数
    for _ in range(count):
        s.append(el)
    # # 使用列表推导式来生成一个包含 x 的列表，列表的长度是 x 在 s 中出现的次数
    # # s.extend([x for _ in range(s.count(x))])
    # # 在生成的列表的末尾添加 el 这个元素，添加的次数也是 x 在 s 中出现的次数
    # s.extend([el for _ in range(s.count(x))])



def filter_iter(iterable, f):
    """
    >>> is_even = lambda x: x % 2 == 0
    >>> list(filter_iter(range(5), is_even)) # a list of the values yielded from the call to filter_iter
    [0, 2, 4]
    >>> all_odd = (2*y-1 for y in range(5))
    >>> list(filter_iter(all_odd, is_even))
    []
    >>> naturals = (n for n in range(1, 100))
    >>> s = filter_iter(naturals, is_even)
    >>> next(s)
    2
    >>> next(s)
    4
    """
    # return iter(filter(f, iterable))

    iter_iterable = iter(iterable)
    # for x in filter(f, iter_iterable):
    #     yield x

    yield from filter(f, iter_iterable)


def is_prime(n):
    """Returns True if n is a prime number and False otherwise.
    >>> is_prime(2)
    True
    >>> is_prime(16)
    False
    >>> is_prime(521)
    True
    """

    def helper(i):
        if i > (n**0.5):  # Could replace with i == n
            return True
        elif n % i == 0:
            return False
        return helper(i + 1)

    return helper(2)


def primes_gen(n):
    """Generates primes in decreasing order.
    >>> pg = primes_gen(7)
    >>> list(pg)
    [7, 5, 3, 2]
    """
    if n <= 1:
        return
    assert n > 1
    if is_prime(n):
        yield n

    yield from primes_gen(n - 1)
########################################################
####                   升序                         #####
########################################################
    # if n <= 1:
    #     return  # 如果 n 小于等于 1，就结束函数
    # yield from primes_gen(n - 1)  # 先返回 n-1 以下的素数
    # if is_prime(n):
    #     yield n  # 再返回 n 本身，如果 n 是素数




def preorder(t):
    """Return a list of the entries in this tree in the order that they
    would be visited by a preorder traversal (see problem description).

    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> preorder(numbers)
    [1, 2, 3, 4, 5, 6, 7]
    >>> preorder(tree(2, [tree(4, [tree(6)])]))
    [2, 4, 6]
    """
    result = []
    def helper(t):
        # 如果树为空，就返回
        if t is None:
            return
        # 否则，先把根节点的值加入结果列表
        result.append(label(t))
        # 然后遍历树的每个分支，并递归地调用辅助函数
        for b in branches(t):
            helper(b)
    helper(t)
    return result


def generate_preorder(t):
    """Yield the entries in this tree in the order that they
    would be visited by a preorder traversal (see problem description).

    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> gen = generate_preorder(numbers)
    >>> next(gen)
    1
    >>> list(gen)
    [2, 3, 4, 5, 6, 7]
    """
    if t is None:
        return
    
    yield label(t) # root
    for b in branches(t):
        yield from generate_preorder(b) #child
