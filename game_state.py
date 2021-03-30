class GameState:
    def __init__(self, game_id):
        self.game = {"game_id": game_id}
        self.player_id = 0  # this id will be useless after being received by bthe client during connection acceptance
        self.roles = ["shooter", "chopper"]
        self.match_types = ["Deathmatch", "1st23", "Best of 3"]
        self.match_type_idx = 0
        self.map_idx = 0
        self.role0_idx = 0
        self.role1_idx = 0
        self.selection = "000000"
        '''
        match_type_idx, map_idx, player0 role_idx, player1 role_idx, player_id, player0 ready flag: 0: not ready, 1: ready
        '''
        self.match_score = {"match_type": self.match_types[self.match_type_idx], "round": 0, "map": self.map_idx,
                            "player0 role": self.roles[self.role0_idx],
                            "player1 role": self.roles[self.role1_idx],
                            "shooter": 0, "chopper": 0, "game_finished": False}
        self.state0 = {"role0": self.roles[0], "pos0_x": 0, "pos0_y": 0, "img_dict_key0": "run_R", "img_idx0": 0}
        self.state1 = {"role1": self.roles[1], "pos1_x": 600, "pos1_y": 200, "img_dict_key1": "run_R", "img_idx1": 0}
        self.player0_ready = False
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

    def update_selection(self, selection_lst):
        self.match_score["match_type"] = selection_lst[0]
        self.match_score["map"] = selection_lst[1]
        self.match_score["player0 role"] = self.roles[selection_lst[2]]
        self.match_score["player1 role"] = self.roles[selection_lst[3]]