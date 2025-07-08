import argparse
import sys

from baseGame.assets import *
from baseGame.game import Game
from baseGame.players import Player
from bots import greedy_agent, random_agent

from training.evaluate import Evaluate_Game
from training.train import Train_Game

def Auto_Game():
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

        game.end_game(players)
        log("\nGame Over!\n")
        for i, player in enumerate(players):
            log(f"Player {i+1} Score: {player.score}")
            log(player)


parser = argparse.ArgumentParser()
parser.add_argument(
    "m",
    help="options: 'h' (vs Human); 'b' (vs Bots); 't' (train a Bot); 'e' (Bot evaluation); 'a' (Bots vs Bots)",
    metavar="GAME_MODE",
    choices=["h", "b", "t", "e", "a"]
)

args = parser.parse_args()

if args.m == "t":
    model_name = input("Enter the name of the training model: ")
    learner_index = int(input("Enter the player position to train: "))
elif args.m == "e":    
    raw_input = input("Enter all 4 model names (separated by commas or spaces): ")
    # Normalize to a list
    opponent_models = [name.strip() for name in raw_input.replace(',', ' ').split() if name.strip()]


if __name__ == "__main__":
    if args.m == "a":
        Auto_Game()
    elif args.m == "t":
        Train_Game(model_name, learner_index = learner_index)
    elif args.m == "e":
        Evaluate_Game(opponent_models)
    elif args.m == "b":
        pass
    elif args.m == "h":
        pass
    else: print("bye")