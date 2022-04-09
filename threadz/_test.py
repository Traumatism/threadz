import time

from . import threadify, gather


def huge_time_function(i: int) -> int:
    time.sleep(1)
    print("done! (%d)" % i)
    return i**2


def threadify_test():
    TEST = True

    f = threadify(huge_time_function) if TEST else huge_time_function

    for _ in range(10):
        f(1)


def gather_test():
    tasks = [
        (huge_time_function, (i,))
        for i in range(50)
    ]

    results = gather(tasks, 10)

    print(results)


if __name__ == "__main__":
    # threadify_test()
    gather_test()
