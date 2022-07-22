import time


def profiler(func):
    """
    The function measures the operating time
    """

    def wrapper(*args, **kwargs):
        before = time.time()
        retval = func(*args, **kwargs)
        after = time.time()
        print(f"Time work of function {func.__name__}: {after - before} \n")
        return retval

    return wrapper
