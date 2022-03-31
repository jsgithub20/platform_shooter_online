from time import time, sleep

now = time()
i = 0
while True:
    e = time() - now
    if e < 0.016:
        sleep(0.016 - e)
    now = time()
    i += 1
    print(i, e)