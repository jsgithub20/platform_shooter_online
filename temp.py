import json
from queue import Queue

rooms = [[False, "Amy"], [True, "Dora"]]
j = json.dumps(rooms)
jd = j.encode()

d = jd.decode()
ds = json.loads(d)

q = Queue()
q.put(rooms)

print(q.get())
