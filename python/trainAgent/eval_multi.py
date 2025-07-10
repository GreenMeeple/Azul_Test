import numpy as np
import random
from stable_baselines3 import PPO
from baseGame.game import Game
from baseGame.players import Player
from bots import greedy_agent
from baseGame.assets import COLORS, ACTIONS

def EvaluateMulti(model_paths):
    num_players = 4
    players = [Player() for _ in range(num_players)]
    models = [PPO.load(path) if path else None for path in model_paths]  # None = use greedy agent
    game = Game()
    first_player_index = 0
    turn_index = random.randint(0, 3)

    while not game.is_game_over(players):
        player_index = turn_index % num_players
        player = players[player_index]
        print_factories(game)
        # Build observation manually (like get_obs)
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
        for factory in game.factories:
            counts = [factory.count(c) for c in COLORS]
            counts.append(factory.count("first_player"))
            factory_encoding.extend(counts)
        while len(factory_encoding) < 9 * 6:
            factory_encoding.extend([0] * 6)
        factory_encoding = np.array(factory_encoding)
        center_encoding = np.array([game.center.count(c) for c in COLORS] + [game.center.count("first_player")])
        opp_encoding = []
        for i, p in enumerate(players):
            if i == player_index:
                continue
            wall = [1 if tile else 0 for row in p.wall for tile in row]
            opp_encoding.extend(wall)
            opp_encoding.append(p.score / 100.0)
        opp_encoding = np.array(opp_encoding)
        turn_info = np.array([player_index])
        fp_token = np.array([1 if "first_player" in player.floor else 0])
        obs = np.concatenate([
            wall_flat, pattern_flat, floor,
            factory_encoding, center_encoding,
            opp_encoding, turn_info, fp_token
        ])
        obs = obs.astype(np.int32)

        legal_moves = player.get_legal_moves(game)
        if models[player_index]:
            action_idx, _ = models[player_index].predict(obs, deterministic=True)
            move = ACTIONS[action_idx]
            if move not in legal_moves:
                move = greedy_agent(game, player)
        else:
            move = greedy_agent(game, player)

        factory, color, line = move
        src = "center" if factory == 9 else f"factory {factory}"
        dest = "floor" if line == -1 else f"pattern line {line}"
        print(f"Player {player_index + 1} plays: {color.upper()} from {src} → {dest}")

        game.play_turn(player, move)
        turn_index += 1


        # Check end of round
        if all(f == [] for f in game.factories) and not game.center:
            game.end_round(players)
            print_walls_side_by_side(players)
            for i, p in enumerate(players):
                if "first_player" in p.floor:
                    first_player_index = i
                    break
            turn_index = first_player_index

    game.end_game(players)
    scores = [p.score for p in players]
    return scores

def print_factories(game):
    print("\nFactories:")
    factory_strs = []
    for i, factory in enumerate(game.factories):
        tiles = " ".join(tile[0].upper() for tile in factory)
        factory_strs.append(f"F{i}: [{tiles}]")

    center_tiles = " ".join(tile[0].upper() for tile in game.center)
    factory_strs.append(f"Center: [{center_tiles}]")

    print(" | ".join(factory_strs))


def print_walls_side_by_side(players):
    headers = [f"Player {i+1}" for i in range(len(players))]
    print("   |  ".join(headers))
    scores = [f"Score: {p.score}" for p in players]
    print("  |  ".join(scores))
    print("-" * (len(players) * 14))  # optional separator

    for row_idx in range(5):  # 5 rows in Azul wall
        row_strs = []
        for p in players:
            row = p.wall[row_idx]
            row_str = ' '.join(tile[0].upper() if tile else '.' for tile in row)
            row_strs.append(row_str)
        print("  |  ".join(row_strs))
    print("-" * (len(players) * 14))