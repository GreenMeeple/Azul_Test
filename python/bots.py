import random
from assets import *

def get_legal_moves(game, player):
    legal_moves = []

    all_factories = game.factories + [game.center]

    for i, factory in enumerate(all_factories):
        if not factory:
            continue
        for color in set(factory):
            if color == "first_player":
                continue  # cannot choose first_player as a tile
            legal = False
            for line in range(5):
                if is_legal_move(player, color, line):
                    legal_moves.append((i, color, line))
                    legal = True
            if not legal:
                # No line can accept this color, so drop it to floor
                legal_moves.append((i, color, -1))  # -1 = floor line
    return legal_moves

def is_legal_move(player, color, line_index):
    pattern_line = player.pattern_lines[line_index]

    # Rule 1: Cannot mix colors in pattern line
    if pattern_line and pattern_line[0] != color:
        return False

    # Rule 2: Cannot place tile if wall already has that color in that row
    if color in player.wall[line_index]:
        return False

    # Rule 3: Cannot overfill the pattern line
    if len(pattern_line) >= line_index + 1:
        return False

    return True

def random_agent(game, player):
    legal_moves = get_legal_moves(game, player)
    if legal_moves:
        return random.choice(legal_moves)
    else:
        # No legal moves at all (shouldn’t happen in Azul, but just in case)
        return None

def greedy_agent(game, player):
    legal_moves = get_legal_moves(game, player)
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
