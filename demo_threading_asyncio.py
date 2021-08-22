import asyncio
from concurrent.futures import CancelledError, TimeoutError
from threading import Thread


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
    await asyncio.sleep(number)
    return number


event_loop = EventLoop()
# tasks = [event_loop.create_task(some_func(number)) for number in range(3)]

tasks = [event_loop.create_task(some_func(0)),
         event_loop.create_task(some_func(1)),
         event_loop.create_task(some_func(4))]

tasks[1].cancel()

# test case 1: to demonstrate timeout
# for i, task in enumerate(tasks):
#     try:
#         print(f'Task {i} result: {task.result(1)}')
#     except TimeoutError:
#         print(f'Task {i} timeout')
#     except CancelledError:
#         print(f'Task {i} cancelled')
# test case 1 ends here

# test case 2: to demonstrate a way to run it without blocking
cnt = 0
while cnt < 3:
    print("If you see this line, the tasks are not blocking")
    for i, task in enumerate(tasks):
        if task.done():  # task.done() is also true if the task is cancelled
            cnt += 1
            tasks.remove(task)
            try:
                print(f'Task {i} result: {task.result(1)}')
            except CancelledError:
                print(f'Task {i} is cancelled')
# test case 2 ends here

event_loop.stop()
