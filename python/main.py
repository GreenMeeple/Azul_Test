
import torch
import pickle
import argparse
import os
import numpy as np
from stable_baselines3 import PPO
from azul_env import AzulEnv
from imitation.algorithms.bc import BC
from stable_baselines3.common.vec_env import DummyVecEnv
from imitation.data.types import Transitions
from assets import *
from game import Game
from players import Player
from bots import greedy_agent, random_agent, get_legal_moves

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

def Train_Game():
    env = DummyVecEnv([lambda: AzulEnv()])
    demo_path = "greedy_data.npz"

    # Step 1: Generate and save expert demonstrations
    if not os.path.exists(demo_path):
        print("Generating greedy demonstrations...")
        obs_list, acts_list = [], []
        env_instance = env.envs[0]

        for _ in range(1000):
            obs = env.reset()
            done = False
            while not done:
                player = env_instance.players[env_instance.current_learning_player]
                legal = get_legal_moves(env_instance.game, player)
                move = greedy_agent(env_instance.game, player) if legal else (-1, "blue", -1)
                action = legal.index(move) if move in legal else 0

                obs_list.append(obs[0])
                acts_list.append(action)

                obs, _, done, _, _ = env.step([action])

        np.savez(demo_path, obs=np.array(obs_list), acts=np.array(acts_list))
        print("Saved demonstrations to", demo_path)
    else:
        print("Loading cached demonstrations from", demo_path)

    # Step 2: Behavior cloning (pretrain from expert)
    print("Pretraining from greedy policy...")
    data = np.load(demo_path)
    transitions = Transitions(
        obs=data["obs"],
        acts=data["acts"],
        dones=np.zeros(len(data["obs"]), dtype=bool),
        infos=[{}] * len(data["obs"]),
        next_obs=data["obs"]
    )

    # Define architecture and manually create the policy via PPO
    policy_kwargs = dict(net_arch=[64, 64])
    ppo_temp = PPO("MlpPolicy", env, policy_kwargs=policy_kwargs, verbose=0)
    policy = ppo_temp.policy

    # Inject policy into BC
    bc_trainer = BC(
        observation_space=env.observation_space,
        action_space=env.action_space,
        demonstrations=transitions,
        rng=np.random.default_rng(0),
        policy=policy,
    )
    bc_trainer.train(n_epochs=20)

    # Save the policy weights
    torch.save(bc_trainer.policy.state_dict(), "ppo_from_greedy.pt")

    # Step 3: Fine-tune with PPO
    print("Fine-tuning with PPO...")
    model = PPO("MlpPolicy", env, verbose=1, policy_kwargs=policy_kwargs)
    model.policy.load_state_dict(torch.load("ppo_from_greedy.pt"))
    model.learn(total_timesteps=10_000_000)
    model.save("ppo_azul")

def Evaluate_Game():
    env = AzulEnv()
    model = PPO.load("ppo_azul")  # or your final model path

    n_games = 10
    total_rewards = []

    for game in range(n_games):
        obs, _ = env.reset()
        done = False
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, _, _ = env.step(action)
        total_rewards.append(reward)
        env.render()

    print("Average final reward over", n_games, "games:", np.mean(total_rewards))

parser = argparse.ArgumentParser()
parser.add_argument("m", help="choose game mode", metavar="GAME_MODE")
args = parser.parse_args()

if __name__ == "__main__":
    if args.m == "auto":
        Auto_Game()
    elif args.m == "train":
        Train_Game()
    elif args.m == "evaluate":
        Evaluate_Game()
    else: print("Invalid mode")