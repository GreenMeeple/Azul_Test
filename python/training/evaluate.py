import numpy as np
from stable_baselines3 import PPO

from baseGame.assets import *
from training.azul_env import AzulEnv
from bots import greedy_agent


def Evaluate_Game(agent_configs, n_games=10):
    """
    agent_configs: list of 4 items. Each item can be:
        - a string (model name in training/models/)
        - the callable `greedy_agent`
        - the string "greedy" (alias for greedy_agent)
        - the string "learn" (used only if training, not for evaluation)

    Example:
        agent_configs = ["azul_gen3", "azul_gen1", greedy_agent, "azul_gen2"]
    """

    if len(agent_configs) > 4:
        raise ValueError("You provided more than 4 agents. Please provide exactly 4.")
    while len(agent_configs) < 4:
        agent_configs.append("greedy")  # Pad with "greedy"

    # Convert string shortcuts
    agents = []
    for cfg in agent_configs:
        if cfg == "greedy":
            agents.append(greedy_agent)
        elif isinstance(cfg, str):
            # Load PPO model from file
            model = PPO.load(f"training/models/{cfg}")
            agents.append(model)
        else:
            # Callable (like greedy_agent) passed directly
            agents.append(cfg)

    env = AzulEnv(agent_types=agent_configs)  # Note: passed config strings
    scores_across_games = [[] for _ in range(4)]

    for game_idx in range(n_games):
        obs, _ = env.reset()
        done = False

        while not done:
            current_player = env.turn_index % env.num_players
            agent = agents[current_player]

            if isinstance(agent, PPO):
                action, _ = agent.predict(obs, deterministic=True)
            else:
                move = agent(env.game, env.players[current_player], current_player)
                try:
                    action = ACTIONS.index(move)
                except ValueError:
                    action = env.action_space.sample()

            obs, reward, done, _, _ = env.step(action)

        print(f"\n--- Game {game_idx + 1} Results ---")
        for i, player in enumerate(env.players):
            print(f"  Player {i + 1}: {player.score}")
            scores_across_games[i].append(player.score)

    print("\n=== Average Scores Over", n_games, "Games ===")
    for i, scores in enumerate(scores_across_games):
        label = agent_configs[i] if isinstance(agent_configs[i], str) else "greedy_agent"
        print(f"  Player {i + 1} ({label}): {np.mean(scores):.2f}")

