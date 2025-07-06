from game import *
from assets import *
from players import *
from bots import *

game = Game()
players = [Player() for _ in range(4)]
first_player_index = 0

with open("game_log.txt", "w") as log_file:
    def log(text=""):
        print(text)
        log_file.write(str(text) + "\n")

    while not game.is_game_over(players):
        current_index = first_player_index
        player_order = []

        while any(factory for factory in game.factories) or game.center:
            player = players[current_index % len(players)]
            choice = random_agent(game, player)
            log(f"Player {current_index % len(players) + 1} chooses: {choice}")
            game.play_turn(player, choice)
            player_order.append(current_index % len(players))
            log(player)
            current_index += 1
            
        for idx, player in enumerate(players):
            if "first_player" in player.floor:
                first_player_index = idx
                break

        game.end_round(players)

    log("\nGame Over!\n")
    for i, player in enumerate(players):
        log(f"Player {i+1} Score: {player.score}")
        log(player)
