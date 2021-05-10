import threading

def func1():
    print(f"this is func1, threads = {threading.active_count()}")
    threading.Thread(target=func2).start()
    print(f"\nthis is func1 after, threads = {threading.active_count()}")


def func2():
    print(f"this is func2, threads = {threading.active_count()}")
    threading.Thread(target=func3).start()
    print(f"\nthis is func2 after, threads = {threading.active_count()}")


def func3():
    print(f"this is func3, threads = {threading.active_count()}")

threading.Thread(target=func1()).start()