# state0 = {"player_id": 0, "role": "shooter", "pos_x": 0, "pos_y": 0, "img_dict_key": "1", "img_idx": 0}
# state1 = {"player_id": 1, "role": "chopper", "pos_x": 0, "pos_y": 0, "img_dict_key": "1", "img_idx": 0}
# state = {}
# state = {**state0, **state1}
# print(state)

profile = {"role0": "self.roles[0]", "pos0_x": 0, "pos0_y": 0, "img_dict_key0": "", "img_idx0": 0}
ext_info = {"role1": "self.roles[1]", "pos1_x": 0, "pos1_y": 0, "img_dict_key1": "", "img_idx1": 0}
full_profile01 = {**profile, **ext_info}
print(full_profile01)