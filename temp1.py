import json

g = [("Amy", True), ("Dora", False)]

gj = json.dumps(g).encode()

jg = gj.decode()

j = json.loads(jg)

jt = [tuple(i) for i in iter(j)]

print(jt)