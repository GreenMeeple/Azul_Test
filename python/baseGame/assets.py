COLORS = ["blue", "yellow", "red", "dark", "cyan"]
TILES_PER_COLOR = 20
FACTORY_SIZE = 4
NUM_PLAYER = 4
NUM_FACTORIES = 9  # 2 players
FLOOR_PENALTIES = [1, 1, 2, 2] + [3] * 96

ACTIONS = []
for f in range(10):  # 0-8 factories + 9=center
    for c in COLORS:
        for l in range(-1, 5):  # -1 is floor, 0–4 are pattern lines
            ACTIONS.append((f, c, l))

