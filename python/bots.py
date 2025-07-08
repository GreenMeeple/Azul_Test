import random
from baseGame.assets import *
from baseGame.players import *

def random_agent(game, player):
    legal_moves = player.get_legal_moves(game)
    if legal_moves:
        return random.choice(legal_moves)
    else:
        # No legal moves at all (shouldn’t happen in Azul, but just in case)
        return None

def greedy_agent(game, player, idx):
    legal_moves = player.get_legal_moves(game)
    best_score = float('-inf')
    best_move = None

    for move in legal_moves:
        factory_index, color, line_index = move
        value = 0

        # How many tiles of that color in the chosen source?
        source = game.factories[factory_index] if factory_index < len(game.factories) else game.center
        count = source.count(color)

        # Avoid floor unless absolutely necessary
        if line_index == -1:
            value -= 10  # big penalty for sending to floor
        else:
            current_line = player.pattern_lines[line_index]
            max_line_size = line_index + 1
            free_space = max_line_size - len(current_line)
            fits = min(free_space, count)
            overflow = max(0, count - free_space)

            value += fits * 2  # prefer placing tiles
            value -= overflow * 3  # penalize floor risk

            # Slight bonus if this move will complete the pattern line
            if len(current_line) + count >= max_line_size:
                value += 3

        if value > best_score:
            best_score = value
            best_move = move

    return best_move