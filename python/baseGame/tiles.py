import random
from collections import Counter
from baseGame.assets import *

class TileBag:
    def __init__(self):
        self.tiles = Counter({color: TILES_PER_COLOR for color in COLORS})
        self.discard = Counter()

    def draw(self, n):
        """
        Draw n tiles from the tile bag. If not enough tiles remain,
        refill from discard pile. Returns a list of drawn tile colors.
        """
        pool = []
        while len(pool) < n:
            if sum(self.tiles.values()) == 0:
                self.refill_from_discard()
                if sum(self.tiles.values()) == 0:
                    break  # still empty
            color = random.choice(list(self.tiles.elements()))
            self.tiles[color] -= 1
            pool.append(color)
        return pool

    def refill_from_discard(self):
        """Move all tiles from discard back into the bag."""
        self.tiles += self.discard
        self.discard.clear()

def get_wall_position(color, row_index):
    """
    Given a color and row, return the column index where the tile should be placed
    on the player's wall based on Azul's fixed wall pattern.
    """
    return (COLORS.index(color) + row_index) % 5
