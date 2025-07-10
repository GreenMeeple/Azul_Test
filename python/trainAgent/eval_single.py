import numpy as np
from stable_baselines3 import PPO
from trainAgent.oldAzul_env import AzulEnv


def EvaluateSingle_Game(model, player_index):
    env = AzulEnv(player_index)
    model = PPO.load(f"trainAgent/models/p{player_index}{model}")  # or your final model path

    n_games = 1
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