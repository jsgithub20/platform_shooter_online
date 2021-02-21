state = {"player_id": 0, "role": 0, "pos_x": 0, "pos_y": 0, "img_idx": 0}
state1 = {"game_id": 1}



# values = (1, 2, 3, 4, 5)
# keys = tuple(state.keys())
# for i in range(len(keys)):
#     state[keys[i]] = values[i]

print({**state, **state1})