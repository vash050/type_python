import time


def profiler(func):
    def wrapper(*args, **kwargs):
        before = time.time()
        retval = func(*args, **kwargs)
        after = time.time()
        print(f"Function {func.__name__}: {after - before} \n")
        return retval

    return wrapper
