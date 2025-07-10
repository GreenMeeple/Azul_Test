import gymnasium as gym
import numpy as np
import random
from gymnasium import spaces

from baseGame.game import Game
from baseGame.players import Player
from bots import greedy_agent
from baseGame.assets import COLORS, FLOOR_PENALTIES

ACTIONS = []
for f in range(10):  # 0-8 factories + 9=center
    for c in COLORS:
        for l in range(-1, 5):  # -1 is floor, 0–4 are pattern lines
            ACTIONS.append((f, c, l))

class AzulEnv(gym.Env):
    def __init__(self, learner_index):
        super().__init__()
        self.num_players = 4
        self.current_learning_player = learner_index
        self.players = [Player() for _ in range(self.num_players)]
        self.game = Game()
        self.first_player_index = random.randint(0, 3)
        self.turn_index = 0
        self.bots = [None if i == self.current_learning_player else greedy_agent for i in range(self.num_players)]
        self.prev_score = 0
        self.prev_completed_rows = set()
        self.prev_completed_cols = set()
        self.prev_completed_colors = set()

        obs_sample = self.get_obs()
        self.observation_space = spaces.Box(
            low=0,
            high=np.max(obs_sample),
            shape=obs_sample.shape,
            dtype=np.int32
        )
        self.action_space = spaces.Discrete(len(ACTIONS))
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.players = [Player() for _ in range(self.num_players)]
        self.game = Game()
        self.turn_index = self.first_player_index
        self.done = False
        self.prev_score = 0

        # Reset bonus trackers
        self.prev_completed_rows.clear()
        self.prev_completed_cols.clear()
        self.prev_completed_colors.clear()

        return self.get_obs(), {}


    def get_obs(self):
        player = self.players[self.current_learning_player]
        color_map = {c: i + 1 for i, c in enumerate(COLORS)}

        wall_flat = np.array([1 if tile else 0 for row in player.wall for tile in row])

        pattern_flat = np.array([
            color_map.get(tile, 0)
            for line in player.pattern_lines
            for tile in line + [0] * (5 - len(line))
        ])

        floor = [color_map[tile] for tile in player.floor if tile != "first_player"]
        floor += [0] * (20 - len(floor))
        floor = np.array(floor)

        factory_encoding = []
        for factory in self.game.factories:
            counts = [factory.count(c) for c in COLORS]
            counts.append(factory.count("first_player"))
            factory_encoding.extend(counts)
        while len(factory_encoding) < 9 * 6:
            factory_encoding.extend([0] * 6)
        factory_encoding = np.array(factory_encoding)

        center = self.game.center
        center_encoding = np.array([center.count(c) for c in COLORS] + [center.count("first_player")])

        opp_encoding = []
        for i, p in enumerate(self.players):
            if i == self.current_learning_player:
                continue
            wall = [1 if tile else 0 for row in p.wall for tile in row]
            opp_encoding.extend(wall)
            opp_encoding.append(p.score / 100.0)
        opp_encoding = np.array(opp_encoding)

        turn_info = np.array([self.current_learning_player])
        fp_token = np.array([1 if "first_player" in player.floor else 0])

        obs = np.concatenate([
            wall_flat, pattern_flat, floor,
            factory_encoding, center_encoding,
            opp_encoding, turn_info, fp_token
        ])
        return obs.astype(np.int32)

    def step(self, action_index):
        if self.done:
            return self.get_obs(), 0, True, False, {}

        while any(f for f in self.game.factories) or self.game.center:
            player_index = self.turn_index % self.num_players
            player = self.players[player_index]

            if player_index == self.current_learning_player:
                factory_index, color, line_index = ACTIONS[action_index]
                move = (factory_index, color, line_index)
                if move not in player.get_legal_moves(self.game):
                    move = greedy_agent(self.game, player)
            else:
                move = self.bots[player_index](self.game, player)

            self.game.play_turn(player, move)
            self.turn_index += 1

            if player_index == self.current_learning_player:
                break

        if all(f == [] for f in self.game.factories) and not self.game.center:
            self.game.end_round(self.players)
            for i, p in enumerate(self.players):
                if "first_player" in p.floor:
                    self.first_player_index = i
                    break
            self.turn_index = self.first_player_index

        self.done = self.game.is_game_over(self.players)
        obs = self.get_obs()
        if self.done:
            self.game.end_game(self.players)
        reward = self.compute_reward()
        return obs, reward, self.done, False, {}

    def compute_reward(self):
        player = self.players[self.current_learning_player]
        reward = 0

        # 1. Score Gain (same as before)
        delta_score = player.score - self.prev_score
        reward += delta_score / 2.0
        self.prev_score = player.score

        # 2. Nonlinear Floor Penalty
        actual_floors = [tile for tile in player.floor if tile != "first_player"]
        penalty = -sum(FLOOR_PENALTIES[i] for i in range(len(actual_floors)))
        reward += penalty 

        # 3. Bonus for completing a pattern line
        for i, line in enumerate(player.pattern_lines):
            if len(line) == i + 1:
                reward += 1.5  # Slightly reduced to avoid duplicate with delta_score

        # 4. Penalty for incomplete pattern lines (they will be wiped at end of game)
        for i, line in enumerate(player.pattern_lines):
            if 0 < len(line) < i + 1:
                reward -= 1.0  # missed opportunity

        # 5. Bonus for taking first player token
        if "first_player" in player.floor:
            reward += 1.0  # Encourage early-round move advantage

        # 6. End-of-game bonus vs opponents
        if self.done:
            others = [p.score for i, p in enumerate(self.players) if i != self.current_learning_player]
            reward += (player.score - np.mean(others)) / 10.0

        wall = player.wall

        # 7.1 Completed rows
        for i, row in enumerate(wall):
            if i not in self.prev_completed_rows and all(tile is not None for tile in row):
                reward += 1.0
                self.prev_completed_rows.add(i)

        # 7.2 Completed columns
        for j in range(5):
            if j not in self.prev_completed_cols and all(wall[i][j] is not None for i in range(5)):
                reward += 3.0
                self.prev_completed_cols.add(j)

        # 7.3 Completed color sets
        for color in COLORS:
            if color not in self.prev_completed_colors:
                count = sum(1 for row in wall if color in row)
                if count == 5:
                    reward += 5.0
                    self.prev_completed_colors.add(color)

        return reward

    def render(self):
        print(f"\nPlayer {self.current_learning_player + 1}'s board:")
        print(self.players[self.current_learning_player])