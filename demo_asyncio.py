import asyncio, logging, time, datetime
#
# logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logging.basicConfig(format='\033[92m%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
# logging.addLevelName(logging.INFO, "\x1b[32m%s\x1b[32m" % logging.getLevelName(logging.INFO)) # change the color

# test 1 starts here:
# async def main():
#     logging.info(f'starting')
#     task = asyncio.create_task(foo('text'))
#     # print("task not started?")
#     # print("it seems task is not executed when created")
#     await asyncio.sleep(1)
#     logging.info(f'main() sleep done')
#     await task
#     logging.info(f'await task done')
#
#
# async def foo(text):
#     logging.info(f'foo() print(text) starting')
#     print(text)
#     logging.info(f'foo() sleep starting')
#     await asyncio.sleep(3)
#     logging.info(f'foo() completed')
#
# asyncio.run(main())
# test 1 ends here.


# test2 starts here:
async def fetch_data():
    print("start fetching")
    # await asyncio.sleep(2)
    time.sleep(2)  # this is a blocking call because it's not asyncio.sleep!
    print("done fetching")
    return {"data": 1}


async def print_numbers(loop):
    for i in range(10):
        print(i)
        if i == 3:
            print(f"current task: {asyncio.current_task()}")
            asyncio.current_task().cancel()
            loop.stop()
            return
        await asyncio.sleep(0.25)
    loop.stop()
    # await asyncio.sleep()  # it seems loop.stop() needs a little time to complete the job
    print(loop.is_running(1))
    loop.close()


# async def main():
#     task1 = asyncio.create_task(fetch_data())
#     task2 = asyncio.create_task(print_numbers())
#     # print(f"all tasks: {len(asyncio.all_tasks())}")
#     # value = await task1
#     # print(task1)
#     # print(f"all tasks: {len(asyncio.all_tasks())}")
#
#     # print(f"fetched value: {value}")
#
#     await task2
#     # print(f"all tasks: {len(asyncio.all_tasks())}")


# asyncio.run(main())

loop = asyncio.get_event_loop()
asyncio.gather(fetch_data(), print_numbers(loop))
loop.run_forever()

# test2 ends here

# test3 starts here
# async def main():
#     print('tim')
#     task = asyncio.create_task(foo('text'))
#     print('finished')
#
#
# async def foo(text):
#     print(f"{text}1")
#     await asyncio.sleep(3)
#     print(f"{text}2")
#
# asyncio.run(main())

# test3 ends here

# test4 starts here:
# async def fetch_data():
#     print("start fetching")
#     # await asyncio.sleep(2)
#     await asyncio.sleep(2)
#     print("done fetching")
#     return {"data": 1}
#
#
# async def print_numbers():
#     for i in range(10):
#         print(i)
#         if i == 3:
#             print(f"current task: {asyncio.current_task()}")
#             asyncio.current_task().cancel()
#             return
#         await asyncio.sleep(0.25)
#
#
# async def main():
#     await fetch_data()  # await a coroutine is blocking
#     await print_numbers()
    # task1 = asyncio.create_task(fetch_data())
    # task2 = asyncio.create_task(print_numbers())
    # # print(f"all tasks: {len(asyncio.all_tasks())}")
    # value = await task1
    # # print(task1)
    # # print(f"all tasks: {len(asyncio.all_tasks())}")
    #
    # # print(f"fetched value: {value}")
    #
    # await task2
    # print(f"all tasks: {len(asyncio.all_tasks())}")


# asyncio.run(main())

# test4 ends here


# from typing import *
# from dataclasses import dataclass
# from collections import defaultdict
#
#
# @dataclass
# class Room:
#     key: str
#     clients: Dict[int,Client] = field(default_factory=dict)
#     new_clients: List[Client] = field(default_factory=list)
#     msg_id: int = 0
#     event_queue: asyncio.Queue = field(default_factory=asyncio.Queue)
#     listening: bool = False
#     future: Any = None # What Type?
#
#     def client_count(self) -> int:
#         return len([c.id for c in self.clients.values() if not c.disconnected])
#
#
# ConnectionOptions = dict[str, str]
# Address = tuple[str, int]
# Server = tuple[Address, ConnectionOptions]
#
# game = {}
# game[0] = (1, 2)
# print(game[0])
# game[0] += (3, 4)
# print(game[0])

# def succ(x):
#     return x + 1
#
# successor = succ
# print(successor(10))

import json

# a = 1
# d = {1:"a", 2:"b", 3:"b"}
# d1 = {"x":"a", "y":"b", "z":"c"}
# # for key in [*d]:
# #     print(key)
# # print(type(*d))
