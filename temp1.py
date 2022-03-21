# freq = {"act": 3, "cg": 2}
# act_v = freq["act"]
# print(act_v)
# m = max(freq.values())
#
# print(max(freq.values()))
# print(freq.keys())
#
# words = []
#
# for key in freq:
#     if freq[key] == m:
#         words.append(key)
#
# print(words)

# a = list(range(5))
# b = a
# a[2] = 12
# print(b is a)

# motifs = ['GGC']
# print()
# for j in range(1, 3):
#     print(Motifs[0:j])

# dna = ["GCGCCCCGCCCGGACAGCCATGCGCTAACCCTGGCTTCGATGGCGCCGGCTCAGTTAGGGCCGGAAGTCCCCAATGTGGCAGACCTTTCGCCCCTGGCGGACGAATGACCCCAGTGGCCGGGACTTCAGGCCCTATCGGAGGGCTCCGGCGCGGTGGTCGGATTTGTCTGTGGAGGTTACACCCCAATCGCAAGGATGCATTATGACCAGCGAGCTGAGCCTGGTCGCCACTGGAAAGGGGAGCAACATC",
# "CCGATCGGCATCACTATCGGTCCTGCGGCCGCCCATAGCGCTATATCCGGCTGGTGAAATCAATTGACAACCTTCGACTTTGAGGTGGCCTACGGCGAGGACAAGCCAGGCAAGCCAGCTGCCTCAACGCGCGCCAGTACGGGTCCATCGACCCGCGGCCCACGGGTCAAACGACCCTAGTGTTCGCTACGACGTGGTCGTACCTTCGGCAGCAGATCAGCAATAGCACCCCGACTCGAGGAGGATCCCG",
# "ACCGTCGATGTGCCCGGTCGCGCCGCGTCCACCTCGGTCATCGACCCCACGATGAGGACGCCATCGGCCGCGACCAAGCCCCGTGAAACTCTGACGGCGTGCTGGCCGGGCTGCGGCACCTGATCACCTTAGGGCACTTGGGCCACCACAACGGGCCGCCGGTCTCGACAGTGGCCACCACCACACAGGTGACTTCCGGCGGGACGTAAGTCCCTAACGCGTCGTTCCGCACGCGGTTAGCTTTGCTGCC",
# "GGGTCAGGTATATTTATCGCACACTTGGGCACATGACACACAAGCGCCAGAATCCCGGACCGAACCGAGCACCGTGGGTGGGCAGCCTCCATACAGCGATGACCTGATCGATCATCGGCCAGGGCGCCGGGCTTCCAACCGTGGCCGTCTCAGTACCCAGCCTCATTGACCCTTCGACGCATCCACTGCGCGTAAGTCGGCTCAACCCTTTCAAACCGCTGGATTACCGACCGCAGAAAGGGGGCAGGAC",
# "GTAGGTCAAACCGGGTGTACATACCCGCTCAATCGCCCAGCACTTCGGGCAGATCACCGGGTTTCCCCGGTATCACCAATACTGCCACCAAACACAGCAGGCGGGAAGGGGCGAAAGTCCCTTATCCGACAATAAAACTTCGCTTGTTCGACGCCCGGTTCACCCGATATGCACGGCGCCCAGCCATTCGTGACCGACGTCCCCAGCCCCAAGGCCGAACGACCCTAGGAGCCACGAGCAATTCACAGCG",
# "CCGCTGGCGACGCTGTTCGCCGGCAGCGTGCGTGACGACTTCGAGCTGCCCGACTACACCTGGTGACCACCGCCGACGGGCACCTCTCCGCCAGGTAGGCACGGTTTGTCGCCGGCAATGTGACCTTTGGGCGCGGTCTTGAGGACCTTCGGCCCCACCCACGAGGCCGCCGCCGGCCGATCGTATGACGTGCAATGTACGCCATAGGGTGCGTGTTACGGCGATTACCTGAAGGCGGCGGTGGTCCGGA",
# "GGCCAACTGCACCGCGCTCTTGATGACATCGGTGGTCACCATGGTGTCCGGCATGATCAACCTCCGCTGTTCGATATCACCCCGATCTTTCTGAACGGCGGTTGGCAGACAACAGGGTCAATGGTCCCCAAGTGGATCACCGACGGGCGCGGACAAATGGCCCGCGCTTCGGGGACTTCTGTCCCTAGCCCTGGCCACGATGGGCTGGTCGGATCAAAGGCATCCGTTTCCATCGATTAGGAGGCATCAA",
# "GTACATGTCCAGAGCGAGCCTCAGCTTCTGCGCAGCGACGGAAACTGCCACACTCAAAGCCTACTGGGCGCACGTGTGGCAACGAGTCGATCCACACGAAATGCCGCCGTTGGGCCGCGGACTAGCCGAATTTTCCGGGTGGTGACACAGCCCACATTTGGCATGGGACTTTCGGCCCTGTCCGCGTCCGTGTCGGCCAGACAAGCTTTGGGCATTGGCCACAATCGGGCCACAATCGAAAGCCGAGCAG",
# "GGCAGCTGTCGGCAACTGTAAGCCATTTCTGGGACTTTGCTGTGAAAAGCTGGGCGATGGTTGTGGACCTGGACGAGCCACCCGTGCGATAGGTGAGATTCATTCTCGCCCTGACGGGTTGCGTCTGTCATCGGTCGATAAGGACTAACGGCCCTCAGGTGGGGACCAACGCCCCTGGGAGATAGCGGTCCCCGCCAGTAACGTACCGCTGAACCGACGGGATGTATCCGCCCCAGCGAAGGAGACGGCG",
# "TCAGCACCATGACCGCCTGGCCACCAATCGCCCGTAACAAGCGGGACGTCCGCGACGACGCGTGCGCTAGCGCCGTGGCGGTGACAACGACCAGATATGGTCCGAGCACGCGGGCGAACCTCGTGTTCTGGCCTCGGCCAGTTGTGTAGAGCTCATCGCTGTCATCGAGCGATATCCGACCACTGATCCAAGTCGGGGGCTCTGGGGACCGAAGTCCCCGGGCTCGGAGCTATCGGACCTCACGATCACC"]
# print(len(dna))

# p = {'A': 0.1, 'C': 0.1, 'G': 0.1, 'T': 0.1}
#
# keys = [k for k in p]
# print(keys)
#
# values = [v for v in p.values()]
# # print(values)
#
# sum = 0
# for v in p.values():
#     sum += v
#
# # print(sum)
#
# kv = [(k, v) for k, v in p.items()]
# # for k, v in p.items():
# #     kv =
#
# print(kv)
from dataclasses import dataclass, field

# @dataclass
# class RoomState:
#     # player0: player[0], player1: player[1]
#     room_id: int = 0
#     player_joined: bool = False  # True if the chosen game room is received from 2nd player
#     game_set: bool = False  # True if player0 finished setting map, match, role
#     map_id: int = 0
#     match_id: int = 0
#     running = False
#     winner = None  # the winner name of the round
#     player_names: list[str] = field(default_factory=list)  # name:str, room name will be f"{player_name[0]}'s game"
#
# rs = RoomState()
#
# rs.player_names.append("aaa")
# rs.player_names.append("bbb")


# class Test:
#     def __init__(self):
#         self.self_var = "self_var"
#
#     def foo(self, room):
#         i = 1
#
#         def bar():
#             print(f"room = {room} in def bar(i)")
#             print(f"i = {i}")
#             print(f"self.self_var = {self.self_var}")
#         a = bar()
#
#
# c = Test()
# f = c.foo("test_room")

import pygame
import pygame.freetype
import pygame.examples.freetype_misc as fm
from platform_shooter_sprites import DrawText


pygame.init()

font1 = pygame.freetype.SysFont("Arial", 30)
window = pygame.display.set_mode((700, 400))

def drawTextCentered(surface, text, text_size, color):
    text_rect = font.get_rect(text, size = text_size)
    # print(text_rect)
    # text_rect.center = surface.get_rect().center
    # font.render_to(surface, (0, 0), text, color, (128, 128, 128), size = text_size)
    # font.render_to(surface, (0, 0), text, color, (128, 128, 128), size = text_size)

# font = pygame.freetype.SysFont("comicsansms", 30)
font = pygame.freetype.Font("resources/OvOV20.ttf", 50)
# font.origin = True

# fm.run()

# a = DrawText(window, 20, (255, 255, 255), 25, 300, "your_name", "self.your_name", alignment="right")
# b = DrawText(window, 20, (255, 255, 255), 25, 300, "your_name", "self.my_name", alignment="left")
# grp = pygame.sprite.Group()
# grp.add(a, b)
fr = font.render("hello g a", (255, 0, 0), (128, 128, 128))[0]
print(fr.get_rect())

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill(0)
    window.blit(fr, (0, 0))
    window.blit(fr, (0, 45))
    # drawTextCentered(window, "Hello g World", 50, (255, 0, 0))
    # grp.update()
    # grp.draw(window)
    pygame.display.flip()

pygame.quit()
exit()
#
# def word_wrap(surf, text, font, color=(0, 0, 0)):
#     font.origin = True
#     words = text.split(' ')
#     width, height = surf.get_size()
#     line_spacing = font.get_sized_height() + 2
#     # x, y = 0, line_spacing
#     x, y = 0, 0
#     space = font.get_rect(' ')
#     for word in words:
#         bounds = font.get_rect(word)
#         print(word, bounds)
#         if x + bounds.width + bounds.x >= width:
#             x, y = 0, y + line_spacing
#         if x + bounds.width + bounds.x >= width:
#             raise ValueError("word too wide for the surface")
#         if y + bounds.height - bounds.y >= height:
#             raise ValueError("text to long for the surface")
#         font.render_to(surf, (x, y), None, color)
#         x += bounds.width + space.width
#     return x, y
#
#
# text = "this is a test to find out the use of .origin, when it's true or false"
#
# while True:
#     draw = word_wrap(screen, text, font1, (255, 255, 255))
#     pygame.display.flip()