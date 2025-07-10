import argparse
import numpy as np
from trainAgent.eval_single import EvaluateSingle_Game
from trainAgent.train_single import TrainSingle_Game
from trainAgent.eval_multi import EvaluateMulti
from playGame.pve import PVE_Game
from playGame.pvp import PVP_Game

parser = argparse.ArgumentParser()
parser.add_argument(
    "m",
    help="options: 'h' (vs Human); 'b' (vs Bots); 'gym' (train a with gym); 'e' (Bot evaluation)",
    metavar="GAME_MODE",
    choices=["ts", "es", "em", "h", "b"]
)

args = parser.parse_args()

if args.m == "ts":
    model_name = input("Enter the name of the training model: ")
    learner_index = int(input("Enter the player position to train: "))
elif args.m == "es": 
    model_name = input("Enter the name of the training model: ")
    learner_index = int(input("Enter the player position to train: "))
elif args.m == "em":    
    raw_input = input("Enter all 4 model names (separated by commas or spaces): ")
    models = [name.strip() for name in raw_input.replace(',', ' ').split() if name.strip()]
    learner_index = int(input("Enter the player position to train: "))

if __name__ == "__main__":
    if args.m == 'ts':
        TrainSingle_Game(model_name, learner_index)
    elif args.m == "es":
        # Evaluate_Game(opponent_models)
        EvaluateSingle_Game(model_name, learner_index)
    elif args.m == "em":
        model_paths = [ f"trainAgent/models/{name}.zip" for name in models ]

        results = []
        for _ in range(1):
            scores = EvaluateMulti(model_paths)
            results.append(scores)
            print("Scores:", scores)

        results = np.array(results)
        print("Average scores per player:", np.mean(results, axis=0))
    elif args.m == "b":
        PVE_Game()
    elif args.m == "h":
        PVP_Game()
    else: print("bye")