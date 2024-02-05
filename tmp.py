def tree(label, branches=[]):
    """Construct a tree with the given label value and a list of branches."""
    return [label] + list(branches)


def label(tree) -> int:
    """Return the label value of a tree."""
    return tree[0]


def branches(tree):
    """Return the list of branches of the given tree."""
    return tree[1:]


def is_leaf(tree):
    """Returns True if the given tree's list of branches is empty, and False
    otherwise.
    """
    return not branches(tree)


def print_tree(t, indent=0):
    print(
        "     " * indent + str(label(t))
    )  # 通过空格串来控制缩进，缩进长度取决于indent
    for b in branches(t):
        print_tree(b, indent + 1)  # 递归控制缩进+1


def height(t):
    """Return the height of a tree.

    >>> t = tree(3, [tree(5, [tree(1)]), tree(2)])
    >>> height(t)
    2
    >>> t = tree(3, [tree(1), tree(2, [tree(5, [tree(6)]), tree(1)])])
    >>> height(t)
    3
    """

    def helper(t, h):
        if is_leaf(t):
            return h
        assert not is_leaf(t)
        return max(helper(branch, h) for branch in branches(t)) + 1

    return helper(t, 0)


def max_path_sum(t):
    """Return the maximum path sum of the tree.

    >>> t = tree(1, [tree(5, [tree(1), tree(3)]), tree(10)])
    >>> max_path_sum(t)
    11
    """
    if is_leaf(t):
        return label(t)
    else:
        return label(t) + max(max_path_sum(branch) for branch in branches(t))


def find_path(t, x):
    """
    >>> t = tree(2, [tree(7, [tree(3), tree(6, [tree(5), tree(11)])] ), tree(15)])
    >>> find_path(t, 5)
    [2, 7, 6, 5]
    >>> find_path(t, 10)  # returns None
    """
    if label(t) == x:
        return [x]
    for b in branches(t):
        path = find_path(b, x)
        if path:
            return [label(t)] + path
    return None


def sum_tree(t):
    """
    Add all elements in a tree.
    >>> t = tree(4, [tree(2, [tree(3)]), tree(6)])
    >>> sum_tree(t)
    15
    """
    if t is None:
        return 0
    return label(t) + sum(sum_tree(b) for b in branches(t))


def balanced(t):
    """
    Checks if each branch has same sum of all elements and
    if each branch is balanced.
    >>> t = tree(1, [tree(3), tree(1, [tree(2)]), tree(1, [tree(1), tree(1)])])
    >>> balanced(t)
    True
    >>> t = tree(1, [t, tree(1)])
    >>> balanced(t)
    False
    >>> t = tree(1, [tree(4), tree(1, [tree(2), tree(1)]), tree(1, [tree(3)])])
    >>> balanced(t)
    False
    """
    if is_leaf(t):
        return True
    # suppose there are many children
    # each branch is balanced:
    each_is_balanced = all(balanced(t) for t in branches(t))
    if not each_is_balanced:
        return False
    # each branch has same sum of all elements
    all_branches_sum = [sum_tree(t) for t in branches(t)]
    if len(set(all_branches_sum)) != 1:
        return False
    return True

def sprout_leaves(t, leaves):
    """Sprout new leaves containing the data in leaves at each leaf in
    the original tree t and return the resulting tree.

    >>> t1 = tree(1, [tree(2), tree(3)])
    >>> print_tree(t1)
    1
      2
      3
    >>> new1 = sprout_leaves(t1, [4, 5])
    >>> print_tree(new1)
    1
      2
        4
        5
      3
        4
        5

    >>> t2 = tree(1, [tree(2, [tree(3)])])
    >>> print_tree(t2)
    1
      2
        3
    >>> new2 = sprout_leaves(t2, [6, 1, 2])
    >>> print_tree(new2)
    1
      2
        3
          6
          1
          2
    """
    if is_leaf(t):
        return tree(label(t), [tree(lv) for lv in leaves])
    else:

        return tree(label(t), [sprout_leaves(b, leaves) for b in branches(t)])

if __name__ == '__main__':
    import doctest
#    doctest.testmod()
    doctest.run_docstring_examples(balanced, globals())