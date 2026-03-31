# main.py — entry point for the RL Drone Navigation project

import argparse
import os
import numpy as np
import matplotlib.pyplot as plt

from config import NUM_EPISODES, START, GOAL, SAVE_PATH
from environment import DroneEnv
from agent import QLearningAgent
from train import train
from visualize import Visualizer


def parse_args():
    parser = argparse.ArgumentParser(description="RL Drone Navigation")
    parser.add_argument("--no-viz", action="store_true", help="Run without live visualization")
    return parser.parse_args()


def print_summary(results, agent):
    success_history = results["success_history"]
    best_path = results["best_path"]
    final_rate = np.mean(success_history[-100:]) if len(success_history) >= 100 else np.mean(success_history)
    print("\n" + "=" * 50)
    print("TRAINING COMPLETE")
    print("=" * 50)
    print(f"Total episodes    : {NUM_EPISODES}")
    print(f"Final goal rate   : {final_rate:.1%}  (last 100 episodes)")
    print(f"Best reward       : {results['best_reward']:.1f}")
    if best_path:
        print(f"Best path length  : {len(best_path) - 1} steps")
    print(f"Final epsilon     : {agent.epsilon:.4f}")
    print("=" * 50)


def show_best_path(env, agent, results, viz):
    best_path = results["best_path"]
    if not best_path:
        print("Drone never reached the goal.")
        return
    env.reset()
    env.path = list(best_path)
    env.pos = best_path[-1]
    goal_rate = np.mean(results["success_history"][-50:]) if len(results["success_history"]) >= 50 else np.mean(results["success_history"])
    stats = {
        "episode": NUM_EPISODES,
        "epsilon": agent.epsilon,
        "goal_rate": goal_rate,
        "last_reward": results["best_reward"],
        "last_steps": len(best_path) - 1,
        "best_reward": results["best_reward"],
    }
    viz.update(env, agent, results["reward_history"], stats)
    viz.save("drone_rl_final.png")


def main():
    args = parse_args()
    os.makedirs(SAVE_PATH, exist_ok=True)

    print(f"RL Drone Navigation | Grid: 12x12 | Start: {START} -> Goal: {GOAL}")
    print(f"Episodes: {NUM_EPISODES} | Visualization: {'OFF' if args.no_viz else 'ON'}")
    print("-" * 50)

    env = DroneEnv()
    agent = QLearningAgent()
    viz = None if args.no_viz else Visualizer()

    results = train(env, agent, visualizer=viz)
    print_summary(results, agent)

    if viz:
        show_best_path(env, agent, results, viz)
        plt.ioff()
        plt.show()


if __name__ == "__main__":
    main()
