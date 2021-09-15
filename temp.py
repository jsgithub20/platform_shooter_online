

def pos2str(pos: tuple):
    # the returned string is like "100,100" from tuple (100, 100)
    return ','.join(map(str, pos))


def str2pos(string):
    # string must be "100,100" or "100, 100" which will be converted to (100, 100)
    return tuple(map(int, string.split(',')))


print(str2pos("100,100"))
print(pos2str((200, 200)))