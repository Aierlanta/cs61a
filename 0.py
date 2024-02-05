# arr: A i,j, i < j => arr[i] < arr[j]
# arr: A i,j, i <= j => arr[i] <= arr[j]
# low <= high low = 0, high = len(arr) - 1, x \in arr[low..high]

# S P R


def binary_search(arr: list[int], x: int) -> bool:
    low = 0
    high = len(arr) - 1
    while True:
        if low > high:
            return False
        mid = (low + high) // 2
        if arr[mid] == x:
            return True
        if arr[mid] < x:
            # low      mid   x   high
            low = mid + 1
        if arr[mid] > x:
            # low  x  mid    high
            high = mid - 1


assert binary_search([1, 2, 2], 2)
assert not binary_search([1, 2, 2], 3)
assert binary_search([1, 2, 2], 1)
assert not binary_search([1, 2, 2], 0)
