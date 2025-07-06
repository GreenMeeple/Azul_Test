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
    moves = get_legal_moves(game, player)
    scored = []
    for move in moves:
        factory, color, line = move
        score = 0
        if line >= 0:
            # Prefer filling lines closer to completion
            score += len(player.pattern_lines[line])
            # Bonus: avoid overflow
            if len(player.pattern_lines[line]) + factory.count(color) > line + 1:
                score -= 3
        else:
            score -= 5  # avoid floor
        scored.append((score, move))
    return max(scored)[1]
