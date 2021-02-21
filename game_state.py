class GameState:
    def __init__(self, game_id):
        self.game = {"game_id": game_id}
        self.player_id = 0  # player_id will be changed to 1 on server if needed
        self.roles = ["shooter", "chopper"]
        self.match_types = ["Deathmatch", "1st23", "Best of 3"]
        self.match_score = {"match_type": self.match_types[0], "round": 0, "shooter": 0, "chopper": 0,
                            "map": 0, "game_finished": False}
        self.state0 = {"player_id": 0, "role": self.roles[0], "pos_x": 0, "pos_y": 0, "img_dict_key": "", "img_idx": 0}
        self.state0_full = {**self.game, **self.state0}
        self.state1 = {"player_id": 1, "role": self.roles[1], "pos_x": 0, "pos_y": 0, "img_dict_key": "", "img_idx": 0}
        self.state1_full = {**self.game, **self.state1}
        self.state_full = {}
        self.ready = False

    def update(self, player_id, role, pos_x, pos_y, img_dict_key, img_idx):
        values = (player_id, role, pos_x, pos_y, img_dict_key, img_idx)
        keys = tuple(self.state0.keys())
        for i in range(len(keys)):
            if player_id == 0:
                self.state0[keys[i]] = values[i]
                self.state0_full = {**self.game, **self.state0}
            else:
                self.state1[keys[i]] = values[i]
                self.state1_full = {**self.game, **self.state0}
