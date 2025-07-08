import gymnasium as gym
import numpy as np
import random
from gymnasium import spaces
from stable_baselines3 import PPO

from baseGame.game import Game
from baseGame.players import Player
from bots import greedy_agent
from baseGame.assets import COLORS, FLOOR_PENALTIES, ACTIONS

class AzulEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, agent_types):
        super().__init__()

        self.num_players = 4
        self.agent_types = agent_types  # List of 4 entries: "learn", "greedy", or model_name
        self.models = []
        self.players = [Player() for _ in range(self.num_players)]
        self.game = Game()
        self.turn_index = 0
        self.first_player_index = 0
        self.done = False

        self.agents = []
        for agent_type in agent_types:
            if agent_type == "learn":
                self.agents.append(None)
            elif agent_type == "greedy":
                self.agents.append(greedy_agent)
            else:
                model = PPO.load(f"training/models/{agent_type}")
                self.agents.append(self.make_model_agent(model))

        # Observation and Action spaces (shared structure)
        obs_sample = self.get_obs(0)
        fixed_obs_shape = (210,)  # Replace with actual known shape

        # Sanity check
        if obs_sample.shape != fixed_obs_shape:
            raise ValueError(f"Observation shape mismatch! Expected {fixed_obs_shape}, got {obs_sample.shape}")

        self.observation_space = spaces.Box(
            low=0,
            high=np.max(obs_sample),
            shape=fixed_obs_shape,
            dtype=np.int32
        )
        self.action_space = spaces.Discrete(len(ACTIONS))

        # Internal tracking for reward components
        self.prev_scores = [0] * self.num_players
        self.prev_rows = [set() for _ in range(self.num_players)]
        self.prev_cols = [set() for _ in range(self.num_players)]
        self.prev_colors = [set() for _ in range(self.num_players)]

    def make_model_agent(self, model):
        def agent_fn(game, player, player_index):
            obs = self.get_obs(player_index)
            action, _ = model.predict(obs, deterministic=True)
            action_tuple = ACTIONS[action]

            legal_moves = player.get_legal_moves(game)
            if action_tuple not in legal_moves:
                return random.choice(legal_moves) if legal_moves else greedy_agent(game, player)
            return action_tuple
        return agent_fn

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.players = [Player() for _ in range(self.num_players)]
        self.game = Game()
        self.first_player_index = random.randint(0, 3)
        self.turn_index = self.first_player_index
        self.done = False
        self.prev_scores = [0] * self.num_players
        self.prev_rows = [set() for _ in range(self.num_players)]
        self.prev_cols = [set() for _ in range(self.num_players)]
        self.prev_colors = [set() for _ in range(self.num_players)]
        return self.get_obs(self.turn_index), {}

    def step(self, action_index):
        if self.done:
            return self.get_obs(self.turn_index), 0, True, False, {}

        player_index = self.turn_index % self.num_players
        player = self.players[player_index]

        if self.agents[player_index] is None:
            move = ACTIONS[action_index]
            if move not in player.get_legal_moves(self.game):
                move = greedy_agent(self.game, player, player_index)
        else:
            move = self.agents[player_index](self.game, player, player_index)

        self.game.play_turn(player, move)
        self.turn_index += 1

        # Round ends
        if all(not f for f in self.game.factories) and not self.game.center:
            self.game.end_round(self.players)
            for i, p in enumerate(self.players):
                if "first_player" in p.floor:
                    self.first_player_index = i
                    break
            self.turn_index = self.first_player_index

        self.done = self.game.is_game_over(self.players)
        if self.done:
            self.game.end_game(self.players)

        obs = self.get_obs(self.turn_index % self.num_players)
        reward = self.compute_reward(player_index)
        return obs, reward, self.done, False, {}

    def get_obs(self, player_index):
        player = self.players[player_index]
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

        center_encoding = np.array([self.game.center.count(c) for c in COLORS] + [self.game.center.count("first_player")])

        opp_encoding = []
        other_indices = [(player_index + i) % self.num_players for i in range(1, self.num_players)]
        for i in other_indices:
            p = self.players[i]
            wall = [1 if tile else 0 for row in p.wall for tile in row]
            opp_encoding.extend(wall)
            opp_encoding.append(p.score / 100.0)
        opp_encoding = np.array(opp_encoding)

        turn_info = np.array([0])
        fp_token = np.array([1 if "first_player" in player.floor else 0])

        obs = np.concatenate([
            wall_flat, pattern_flat, floor,
            factory_encoding, center_encoding,
            opp_encoding, turn_info, fp_token
        ])
        return obs.astype(np.int32)

    def compute_reward(self, player_index):
        player = self.players[player_index]
        reward = 0

        delta_score = player.score - self.prev_scores[player_index]
        reward += delta_score / 2.0
        self.prev_scores[player_index] = player.score

        actual_floors = [tile for tile in player.floor if tile != "first_player"]
        penalty = -sum(FLOOR_PENALTIES[i] for i in range(len(actual_floors)))
        reward += penalty 

        for i, line in enumerate(player.pattern_lines):
            if len(line) == i + 1:
                reward += 1.5
            elif 0 < len(line) < i + 1:
                reward -= 1.0

        if "first_player" in player.floor:
            reward += 1.0

        if self.done:
            others = [p.score for i, p in enumerate(self.players) if i != player_index]
            reward += (player.score - np.mean(others)) / 10.0

        wall = player.wall

        for i, row in enumerate(wall):
            if i not in self.prev_rows[player_index] and all(tile is not None for tile in row):
                reward += 1.0
                self.prev_rows[player_index].add(i)

        for j in range(5):
            if j not in self.prev_cols[player_index] and all(wall[i][j] is not None for i in range(5)):
                reward += 3.0
                self.prev_cols[player_index].add(j)

        for color in COLORS:
            if color not in self.prev_colors[player_index]:
                count = sum(1 for row in wall if color in row)
                if count == 5:
                    reward += 5.0
                    self.prev_colors[player_index].add(color)

        return reward

    def render(self):
        for i, player in enumerate(self.players):
            print(f"\nPlayer {i + 1} (Score: {player.score}):")
            print(player)
