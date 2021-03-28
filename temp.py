import datetime
import time
from pygame.time import Clock

# stamp = time.time()
# print(stamp)
# print(datetime.date.fromtimestamp(stamp))
clock = Clock()
while True:
    clock.tick(60)
    print(clock.get_fps())
