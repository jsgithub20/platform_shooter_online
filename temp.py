from queue import Queue

# Initializing a queue
q = Queue(maxsize=3)

# qsize() give the maxsize
# of the Queue
print(q.qsize())

# Adding of element to queue
q.put((100, 199))
q.put('b')
q.put('c')

# Return Boolean for Full
# Queue
print("\nFull: ", q.full())

# Removing element from queue
print("\nElements dequeued from the queue")
# print(type(q.get()))
# print(q.get())
# print(q.get())
# print(q.get_nowait())

a = "start"

try:
    a = q.get_nowait()
    print(f"a = {a}")
    a = q.get_nowait()
    print(f"a = {a}")
    a = q.get_nowait()
    print(f"a = {a}")
    a = q.get_nowait()
    print(f"a = {a}")
except:
    print("empty")
    print(f"finally a = {a}")

# Return Boolean for Empty
# Queue
print("\nEmpty: ", q.empty())

q.put(1)
print("\nEmpty: ", q.empty())
print("Full: ", q.full())