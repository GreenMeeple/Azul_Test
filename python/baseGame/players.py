from baseGame.assets import *

class Player:
    def __init__(self):
        self.wall = [[None] * 5 for _ in range(5)]
        self.pattern_lines = [[] for _ in range(5)]
        self.floor = []
        self.score = 0

    def __str__(self):
        s = f"Score: {self.score}\n"
        # s += "Pattern Lines:\n"
        # for i, line in enumerate(self.pattern_lines):
        #     s += f"{i + 1}: {line}\n"
        # s += f"Floor: {self.floor}\n"
        s += 'Wall:\n'
        for row in self.wall:
            s += ' '.join(tile[0].upper() if tile else '.' for tile in row) + '\n'
        return s

    def choose_tiles(self, source, color):
        """
        Picks all tiles of a given color from the source.
        Returns (picked_tiles, leftover_tiles)
        """
        picked = [tile for tile in source if tile == color]
        leftovers = [tile for tile in source if tile != color]
        return picked, leftovers

    def place_tiles(self, picked, line_index):
        picked = [tile for tile in picked if tile != "first_player"]  # 👈 filter it out here

        if line_index == -1:
            self.floor.extend(picked)
            return

        max_len = line_index + 1
        current_line = self.pattern_lines[line_index]
        space_left = max_len - len(current_line)

        if space_left > 0:
            to_place = picked[:space_left]
            overflow = picked[space_left:]
            self.pattern_lines[line_index].extend(to_place)
            self.floor.extend(overflow)
        else:
            self.floor.extend(picked)


    def get_state(self):
        return {
            "wall": [row[:] for row in self.wall],
            "pattern_lines": [line[:] for line in self.pattern_lines],
            "floor": self.floor[:],
            "score": self.score
        }

    def can_place(self, color, line_index):
        if line_index < 0 or line_index > 4:
            return False
        line = self.pattern_lines[line_index]
        if line and line[0] != color:
            return False
        if color in self.wall[line_index]:  # already completed
            return False
        if len(line) >= line_index + 1:
            return False
        return True
    
    def get_legal_moves(self, game):
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
                    if self.is_legal_move(color, line):
                        legal_moves.append((i, color, line))
                        legal = True
                if not legal:
                    # No line can accept this color, so drop it to floor
                    legal_moves.append((i, color, -1))  # -1 = floor line
        return legal_moves

    def is_legal_move(self, color, line_index):
        pattern_line = self.pattern_lines[line_index]

        # Rule 1: Cannot mix colors in pattern line
        if pattern_line and pattern_line[0] != color:
            return False

        # Rule 2: Cannot place tile if wall already has that color in that row
        if color in self.wall[line_index]:
            return False

        # Rule 3: Cannot overfill the pattern line
        if len(pattern_line) >= line_index + 1:
            return False

        return True

