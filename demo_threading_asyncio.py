import asyncio
from concurrent.futures import CancelledError
from threading import Thread
import datetime


class EventLoop(Thread):
    def __init__(self):
        self._loop = asyncio.get_event_loop()
        super().__init__(target=self._loop.run_forever)
        self.start()

    def stop(self):
        self._loop.call_soon_threadsafe(self._loop.stop)

    def create_task(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self._loop)


async def some_func(number):
    await asyncio.sleep(3)
    return number


event_loop = EventLoop()
tasks = [event_loop.create_task(some_func(number)) for number in range(3)]

# tasks[1].cancel()

cnt = 0

while cnt < 3:
    print("If you see this, the tasks are not blocking.")
    for i, task in enumerate(tasks):
        if task.done():
            cnt += 1
            print(f'Task {i} result: {task.result()}')

# for i, task in enumerate(tasks):
#     try:
#         print(f'Task {i} result: {task.result()}')
#     except CancelledError:
#         print(f'Task {i} cancelled')

event_loop.stop()
