# main.py — entry point for L50 RL Dynamic Race

import argparse
import os
import numpy as np
import matplotlib.pyplot as plt

from config import NUM_EPISODES, START, GOAL, SAVE_PATH
from environment import DroneEnv
from agent_qlearn import QLearningAgent
from agent_bellman import BellmanAgent
from train import train, build_viz_stats
from visualize import Visualizer


def parse_args():
    p = argparse.ArgumentParser(description="Dynamic Drone Race: Bellman vs Q-Learning")
    p.add_argument("--no-viz", action="store_true", help="Run without live visualization")
    return p.parse_args()


def print_summary(sq, sb):
    rate_q = np.mean(sq["successes"][-100:]) if len(sq["successes"]) >= 100 else np.mean(sq["successes"] or [0])
    rate_b = np.mean(sb["successes"][-100:]) if len(sb["successes"]) >= 100 else np.mean(sb["successes"] or [0])
    cum_q  = sum(sq["rewards"])
    cum_b  = sum(sb["rewards"])

    print("\n" + "=" * 57)
    print("  RACE RESULTS")
    print("=" * 57)
    print(f"  {'Metric':<26} {'Q-Learning':>12} {'Bellman (VI)':>13}")
    print("  " + "-" * 53)
    print(f"  {'Goal Rate (last 100 ep)':<26} {rate_q:>11.1%} {rate_b:>12.1%}")
    print(f"  {'Best Single Reward':<26} {sq['best_reward']:>12.1f} {sb['best_reward']:>13.1f}")
    print(f"  {'Cumulative Score':<26} {cum_q:>12.0f} {cum_b:>13.0f}")
    print("=" * 57)
    if cum_q > cum_b:
        winner = "Q-Learning WINS!"
    elif cum_b > cum_q:
        winner = "Bellman (VI) WINS!"
    else:
        winner = "It's a TIE!"
    print(f"  WINNER: {winner}")
    print("=" * 57)


def show_final_frame(env_q, env_b, agent_q, agent_b, sq, sb, viz):
    """Display the best paths and save the final image."""
    for env, agent, stats, label in [
        (env_q, agent_q, sq, "Q-Learning"),
        (env_b, agent_b, sb, "Bellman (VI)"),
    ]:
        if stats["best_path"]:
            env.reset()
            env.path = list(stats["best_path"])
            env.pos  = stats["best_path"][-1]
        print(f"  {label} best path length: "
              f"{len(stats['best_path']) - 1 if stats['best_path'] else 'N/A'} steps")

    viz_stats = build_viz_stats(NUM_EPISODES, agent_q, sq, sb, env_q)
    viz.update(env_q, env_b, agent_q, agent_b, sq["rewards"], sb["rewards"], viz_stats)
    viz.save("race_final.png")


def main():
    args = parse_args()
    os.makedirs(SAVE_PATH, exist_ok=True)

    print(f"Dynamic Drone Race | Grid: {12}x{12} | Episodes: {NUM_EPISODES}")
    print(f"Start: {START}  ->  Goal: {GOAL}")
    print(f"Algorithms: Q-Learning  vs  Bellman (Value Iteration)")
    print(f"Visualization: {'OFF' if args.no_viz else 'ON'}")
    print("-" * 57)

    env_q   = DroneEnv()
    env_b   = DroneEnv()
    agent_q = QLearningAgent()
    agent_b = BellmanAgent()

    # Bellman needs an initial solve before the first episode
    agent_b.solve(env_q)

    viz = None if args.no_viz else Visualizer()
    sq, sb = train(env_q, env_b, agent_q, agent_b, visualizer=viz)

    print_summary(sq, sb)

    if viz:
        show_final_frame(env_q, env_b, agent_q, agent_b, sq, sb, viz)
        plt.ioff()
        plt.show()


if __name__ == "__main__":
    main()
