from time import sleep, perf_counter
from threading import Thread

# no Threading example starts
# def task():
#     print('Starting a task...')
#     sleep(1)
#     print('done')
#
#
# start_time = perf_counter()
#
# task()
# task()
#
# end_time = perf_counter()
#
# print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')

# no Threading example ends

# Threading example starts
def task(id, s):
    print(f'Starting the task {id}...')
    sleep(s)
    print(f'The task {id} completed')


start_time = perf_counter()
#
# # create multiple new threads
threads = []
for i in range(4):
    t = Thread(target=task, args=(i, i/2))
    # t = Thread(target=task, args=(i, i/2), daemon=True)
    # t = Thread(target=task, args=(i, ), daemon=True)
    threads.append(t)

# start the threads
for i in range(4):
    threads[i].start()

# wait for the threads to complete
# for i in range(4):
#     threads[i].join()

end_time = perf_counter()

print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')

# Threading example ends
