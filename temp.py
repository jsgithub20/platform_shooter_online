import asyncio, time

# test 1 starts here:
# async def main():
#     print(f'start: {time.strftime("%X")}')
#     task = asyncio.create_task(foo('text'))
#     print("task not started?")
#     print("it seems task is not executed when created")
#     await asyncio.sleep(1)
#     print(f'main() sleep done: {time.strftime("%X")}')
#     await task
#     print(f'await task done: {time.strftime("%X")}')
#
#
# async def foo(text):
#     print(f'foo() print(text) starting: {time.strftime("%X")}')
#     print(text)
#     print(f'foo() sleep starting: {time.strftime("%X")}')
#     await asyncio.sleep(3)
#     print(f'foo() completed: {time.strftime("%X")}')
#
# asyncio.run(main())
# test 1 ends here.


# test2 starts here:
async def fetch_data():
    print("start fetching")
    await asyncio.sleep(2)
    print("done fetching")
    return {"data": 1}


async def print_numbers():
    for i in range(10):
        print(i)
        await asyncio.sleep(0.25)


async def main():
    task1 = asyncio.create_task(fetch_data())
    task2 = asyncio.create_task(print_numbers())

    value = await task1
    print(value)
    await task2


asyncio.run(main())
# test2 ends here
