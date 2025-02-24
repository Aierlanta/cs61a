def sqare(n:int) -> int:  
    return n * n

def pow(base:int, exp:int):
    if base == exp:
        return
    #if base != exp:
    pow(sqare(base), exp)