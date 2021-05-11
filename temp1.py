# import threading
#
# def func1():
#     print(f"this is func1, threads = {threading.active_count()}")
#     threading.Thread(target=func2).start()
#     print(f"\nthis is func1 after, threads = {threading.active_count()}")
#
#
# def func2():
#     print(f"this is func2, threads = {threading.active_count()}")
#     print(f"this is func2 again")
#     threading.Thread(target=func3).start()
#     print(f"\nthis is func2 after, threads = {threading.active_count()}")
#
#
# def func3():
#     print(f"this is func3, threads = {threading.active_count()}")
#
# threading.Thread(target=func1()).start()
#
import asyncio

async def func1():
    print(f"this is func1, threads = {len(asyncio.all_tasks())}")
    await func2()
    print(f"\nthis is func1 after, threads = {len(asyncio.all_tasks())}")


async def func2():
    print(f"this is func2, threads = {len(asyncio.all_tasks())}")
    print(f"this is func2 again")
    await func3()
    print(f"\nthis is func2 after, threads = {len(asyncio.all_tasks())}")


async def func3():
    print(f"this is func3, threads = {len(asyncio.all_tasks())}")

asyncio.run(func1())