class GameState:
    def __init__(self, game_id):
        self.game = {"game_id": game_id}
        self.player_id = 0  # player_id will be changed to 1 on server if needed
        self.roles = ["shooter", "chopper"]
        self.match_types = ["Deathmatch", "1st23", "Best of 3"]
        self.match_score = {"match_type": self.match_types[0], "round": 0, "shooter": 0, "chopper": 0,
                            "map": 0, "game_finished": False}
        self.state0 = {"role0": self.roles[0], "pos0_x": 0, "pos0_y": 0, "img_dict_key0": "run_R", "img_idx0": 0}
        self.state1 = {"role1": self.roles[1], "pos1_x": 600, "pos1_y": 200, "img_dict_key1": "run_R", "img_idx1": 0}
        self.state_send = {}
        self.ready = False

    def update(self, player_id, role, pos_x, pos_y, img_dict_key, img_idx):
        values = (role, pos_x, pos_y, img_dict_key, img_idx)
        if player_id == 0:
            keys = tuple(self.state0.keys())
            for i in range(len(keys)):
                self.state0[keys[i]] = values[i]
        else:
            keys = tuple(self.state1.keys())
            for i in range(len(keys)):
                self.state1[keys[i]] = values[i]
        self.state_send = {**self.state0, **self.state1}
