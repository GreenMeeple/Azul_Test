import os
import numpy as np
from stable_baselines3 import PPO
from imitation.algorithms.bc import BC
from stable_baselines3.common.vec_env import DummyVecEnv
from imitation.data.types import Transitions

from trainAgent.oldAzul_env import AzulEnv
from baseGame.assets import *
from bots import greedy_agent

def TrainSingle_Game(model_name, learner_index=0, total_timesteps=10000, demo_path=None):
    env = DummyVecEnv([lambda: AzulEnv(learner_index)])
    demo_path = f"trainAgent/models/demo.npz"
    model_path = f"trainAgent/models/p{learner_index}{model_name}"

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
                legal = player.get_legal_moves(env_instance.game)
                move = greedy_agent(env_instance.game, player) if legal else (-1, "blue", -1)
                action = legal.index(move) if move in legal else 0

                obs_list.append(obs[0])
                acts_list.append(action)

                obs, _, done, _ = env.step([action])

        np.savez(demo_path, obs=np.array(obs_list), acts=np.array(acts_list))
        print("Saved demonstrations to", demo_path)
    else:
        print("Loading cached demonstrations from", demo_path)

    # Step 2: Behavior cloning (pretrain from expert)
    policy_kwargs = dict(net_arch=[64, 64])

    if os.path.exists(f"{model_path}.zip"):
        print(f"Loading existing model from {model_path}...")
        model = PPO.load(model_path, env=env)
    else:
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
        model = PPO("MlpPolicy", env, verbose=1, policy_kwargs=policy_kwargs)
        model.policy.load_state_dict(bc_trainer.policy.state_dict())

    # Step 3: Fine-tune with PPO
    print("Fine-tuning with PPO...")
    model.learn(total_timesteps=total_timesteps)
    model.save(model_path)
    print(f"Model saved to {model_path}")
