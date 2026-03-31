# train.py — training loop for the RL drone agent

import numpy as np
from config import NUM_EPISODES, MAX_STEPS, VIZ_UPDATE_INTERVAL


def run_episode(env, agent):
    state = env.reset()
    total_reward = 0.0
    success = False

    for _ in range(MAX_STEPS):
        action = agent.choose_action(state)
        next_state, reward, done = env.step(action)
        agent.update(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward
        if done:
            success = (env.pos == env.goal)
            break

    agent.decay_epsilon()
    return total_reward, env.steps, success, list(env.path)


def train(env, agent, visualizer=None):
    reward_history = []
    success_history = []
    best_path = None
    best_reward = float("-inf")

    for episode in range(1, NUM_EPISODES + 1):
        reward, steps, success, path = run_episode(env, agent)
        reward_history.append(reward)
        success_history.append(int(success))

        if success and reward > best_reward:
            best_reward = reward
            best_path = path

        if episode % 100 == 0:
            recent_rate = np.mean(success_history[-100:])
            print(
                f"Episode {episode:4d} | "
                f"Reward: {reward:7.1f} | "
                f"Steps: {steps:3d} | "
                f"Epsilon: {agent.epsilon:.3f} | "
                f"Goal rate (100ep): {recent_rate:.1%}"
            )

        if visualizer and episode % VIZ_UPDATE_INTERVAL == 0:
            goal_rate = np.mean(success_history[-50:]) if len(success_history) >= 50 else np.mean(success_history)
            stats = {
                "episode": episode,
                "epsilon": agent.epsilon,
                "goal_rate": goal_rate,
                "last_reward": reward,
                "last_steps": steps,
                "best_reward": best_reward,
            }
            visualizer.update(env, agent, reward_history, stats)

    return {
        "reward_history": reward_history,
        "success_history": success_history,
        "best_path": best_path,
        "best_reward": best_reward,
    }
