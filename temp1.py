import json

lt = [("name1", False, 1), ("name2", True, 2)]

ltde = json.dumps(lt).encode()

ltld = json.loads(ltde.decode())

ltld = [tuple(lst) for lst in ltld]


def test(a, **kwargs):
    print(a)
    if kwargs:
        print(kwargs["key"])


# test("a")
# test("a", key="content")

# print(f"{lt == ltld}")

d = {0: "this is 0", 1: "this is 1"}

print(d)
print(type([*d][0]))