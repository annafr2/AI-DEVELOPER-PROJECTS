# train.py — dual-agent training loop (Q-Learning vs Bellman)

import numpy as np
from config import NUM_EPISODES, MAX_STEPS, VIZ_UPDATE_INTERVAL


def _run_qlearn(env, agent):
    """One episode: Q-Learning agent steps, observes, updates Q-table."""
    state = env.reset()
    total = 0.0
    for _ in range(MAX_STEPS):
        action = agent.choose_action(state)
        next_state, reward, done = env.step(action)
        agent.update(state, action, reward, next_state, done)
        state = next_state
        total += reward
        if done:
            break
    agent.decay_epsilon()
    return total, env.steps, env.pos == env.goal, list(env.path)


def _run_bellman(env, agent):
    """One episode: Bellman/VI agent uses its computed policy (no Q-table update)."""
    state = env.reset()
    total = 0.0
    for _ in range(MAX_STEPS):
        action = agent.choose_action(state, env)   # may re-solve if env changed
        next_state, reward, done = env.step(action)
        state = next_state
        total += reward
        if done:
            break
    return total, env.steps, env.pos == env.goal, list(env.path)


def _make_stats():
    return {"rewards": [], "successes": [], "best_reward": float("-inf"), "best_path": None}


def _record(stats, reward, success, path):
    stats["rewards"].append(reward)
    stats["successes"].append(int(success))
    if success and reward > stats["best_reward"]:
        stats["best_reward"] = reward
        stats["best_path"]   = path


def build_viz_stats(episode, agent_q, sq, sb, env_q):
    """Pack all numbers the visualizer needs into one dict."""
    def rate(s): return np.mean(s["successes"][-50:]) if len(s["successes"]) >= 50 else np.mean(s["successes"] or [0])
    return {
        "episode":  episode,
        "epsilon":  agent_q.epsilon,
        "rate_q":   rate(sq),
        "rate_b":   rate(sb),
        "best_q":   sq["best_reward"],
        "best_b":   sb["best_reward"],
        "cum_q":    sum(sq["rewards"]),
        "cum_b":    sum(sb["rewards"]),
        "n_events": len(env_q._events),
    }


def train(env_q, env_b, agent_q, agent_b, visualizer=None):
    sq, sb = _make_stats(), _make_stats()

    for ep in range(1, NUM_EPISODES + 1):

        # --- Sync dynamic events: both drones face the exact same world ---
        env_q.maybe_spawn_event(ep)
        env_b._events = dict(env_q._events)
        env_b._refresh_sets()

        # --- Run one episode for each agent ---
        r_q, steps_q, ok_q, path_q = _run_qlearn(env_q, agent_q)
        r_b, steps_b, ok_b, path_b = _run_bellman(env_b, agent_b)

        _record(sq, r_q, ok_q, path_q)
        _record(sb, r_b, ok_b, path_b)

        if ep % 100 == 0:
            rate_q = np.mean(sq["successes"][-100:])
            rate_b = np.mean(sb["successes"][-100:])
            print(
                f"Ep {ep:4d} | "
                f"Q: {r_q:7.1f} ({rate_q:.0%}) | "
                f"Bell: {r_b:7.1f} ({rate_b:.0%}) | "
                f"Events: {len(env_q._events)} | "
                f"e={agent_q.epsilon:.3f}"
            )

        if visualizer and ep % VIZ_UPDATE_INTERVAL == 0:
            viz_stats = build_viz_stats(ep, agent_q, sq, sb, env_q)
            visualizer.update(
                env_q, env_b, agent_q, agent_b,
                sq["rewards"], sb["rewards"], viz_stats,
            )

    return sq, sb
