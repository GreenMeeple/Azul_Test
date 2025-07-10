from baseGame.assets import *
from baseGame.tiles import *

class Game:
    def __init__(self):
        self.tilebag = TileBag()
        self.factories = []
        self.center = []
        self.reset_factories()

    def reset_factories(self):
        self.factories = []
        for _ in range(NUM_FACTORIES):
            self.factories.append(self.tilebag.draw(FACTORY_SIZE))
        self.center = ["first_player"]

    def play_turn(self, player, choice):
        factory_index, color, line = choice

        if factory_index < len(self.factories):
            factory = self.factories[factory_index]
            self.factories[factory_index] = []
        else:
            factory = self.center
            if "first_player" in factory:
                player.floor.append("first_player")

        picked, leftovers = player.choose_tiles(factory, color)

        if factory_index >= len(self.factories):
            self.center = [tile for tile in self.center if tile != color and tile != "first_player"]
        else:
            self.center.extend(leftovers)

        player.place_tiles(picked, line)

    def end_round(self, players):
        for player in players:
            for row_index, line in enumerate(player.pattern_lines):
                if len(line) == row_index + 1:
                    # Completed line — move to wall
                    color = line[0]
                    col_index = get_wall_position(color, row_index)
                    if player.wall[row_index][col_index] is None:
                        player.wall[row_index][col_index] = color
                        player.score += self.score_tile(player.wall, row_index, col_index)
                    num_discard = len(line) - 1
                    self.tilebag.discard[color] += num_discard
                    line.clear()
                # ❌ Do not touch incomplete lines anymore

            # Floor penalty
            penalty = sum(FLOOR_PENALTIES[:len(player.floor)])
            player.score = max(0, player.score - penalty)

            # Discard floor tiles (except first_player token)
            for tile in player.floor:
                if tile != "first_player":
                    self.tilebag.discard[tile] += 1
            player.floor.clear()

        self.reset_factories()

    def is_game_over(self, players):
        for player in players:
            for row in player.wall:
                if all(cell is not None for cell in row):
                    return True
        return False

    def score_tile(self, wall, row, col):
        # Simple scoring: 1 base point + adjacency bonuses
        score = 1
        horiz = 0
        for dc in [-1, 1]:
            c = col + dc
            while 0 <= c < 5 and wall[row][c] is not None:
                horiz += 1
                c += dc

        vert = 0
        for dr in [-1, 1]:
            r = row + dr
            while 0 <= r < 5 and wall[r][col] is not None:
                vert += 1
                r += dr

        if horiz > 0: score += horiz
        if vert > 0: score += vert
        return score
    
    def end_game(self, players):
        for player in players:
            # Full row = 2 points (already checked during scoring usually)
            for row in range(5):
                if all(player.wall[row][col] is not None for col in range(5)):
                    player.score += 2

            # Full column
            for col in range(5):
                if all(player.wall[row][col] is not None for row in range(5)):
                    player.score += 7

            # Full color (one tile of same color in all rows)
            for color in COLORS:
                count = sum(
                    any(tile == color for tile in row if tile is not None)
                    for row in player.wall
                )
                if count == 5:
                    player.score += 10
