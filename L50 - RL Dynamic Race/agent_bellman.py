# agent_bellman.py — Value Iteration drone (model-based)
#
# How it works:
#   Value Iteration applies the Bellman equation to EVERY state at once,
#   repeating until the value estimates stop changing.  It needs to KNOW the
#   grid layout (buildings, wind, pits, bridges) to compute transition probs.
#   When the environment changes, it re-solves from scratch — expensive, but
#   the resulting policy is provably optimal for the CURRENT known world.

import numpy as np
from config import (
    GRID_SIZE, GOAL, GAMMA,
    REWARD_GOAL, REWARD_STEP, REWARD_BUILDING, REWARD_WIND,
    REWARD_PIT, REWARD_BRIDGE, VI_THETA, VI_MAX_ITER,
)

N_STATES  = GRID_SIZE * GRID_SIZE
N_ACTIONS = 4
ACTION_DELTAS = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}


class BellmanAgent:
    def __init__(self):
        self.gamma   = GAMMA
        self.V       = np.zeros(N_STATES)
        self.policy  = np.zeros(N_STATES, dtype=int)
        self._env_hash = None   # fingerprint of last known environment

    # ------------------------------------------------------------------ helpers

    def _encode(self, r, c): return r * GRID_SIZE + c
    def _decode(self, s):    return s // GRID_SIZE, s % GRID_SIZE

    def _env_fingerprint(self, env):
        return (frozenset(env.buildings), frozenset(env.wind_zones),
                frozenset(env.pits),      frozenset(env.bridges))

    def _transitions(self, r, c, action, env):
        """Return list of (probability, next_state, reward, done) for one step."""
        dr, dc = ACTION_DELTAS[action]
        nr = max(0, min(GRID_SIZE - 1, r + dr))
        nc = max(0, min(GRID_SIZE - 1, c + dc))
        new_pos = (nr, nc)

        # Hit a wall → stay in place
        if new_pos in env.buildings:
            return [(1.0, self._encode(r, c), REWARD_BUILDING, False)]

        # Pit → episode ends
        if new_pos in env.pits:
            return [(1.0, self._encode(*new_pos), REWARD_PIT, True)]

        # Wind → uniform push to any valid neighbor
        if new_pos in env.wind_zones:
            neighbors = [
                (new_pos[0] + dr2, new_pos[1] + dc2)
                for dr2, dc2 in ACTION_DELTAS.values()
                if (self._is_valid(new_pos[0]+dr2, new_pos[1]+dc2)
                    and (new_pos[0]+dr2, new_pos[1]+dc2) not in env.buildings)
            ]
            if not neighbors:
                neighbors = [new_pos]
            p = 1.0 / len(neighbors)
            return [(p, self._encode(*n), REWARD_WIND, n == GOAL) for n in neighbors]

        # Bridge → bonus
        if new_pos in env.bridges:
            return [(1.0, self._encode(*new_pos), REWARD_BRIDGE, new_pos == GOAL)]

        # Goal
        if new_pos == GOAL:
            return [(1.0, self._encode(*new_pos), REWARD_GOAL, True)]

        return [(1.0, self._encode(*new_pos), REWARD_STEP, False)]

    def _is_valid(self, r, c):
        return 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE

    # ------------------------------------------------------------------ solver

    def solve(self, env):
        """Run Value Iteration to convergence, then extract greedy policy."""
        V = np.zeros(N_STATES)
        for _ in range(VI_MAX_ITER):
            delta = 0.0
            for s in range(N_STATES):
                r, c = self._decode(s)
                if (r, c) == GOAL or (r, c) in env.buildings:
                    continue
                q_vals = [
                    sum(p * (rew + (0.0 if done else self.gamma * V[ns]))
                        for p, ns, rew, done in self._transitions(r, c, a, env))
                    for a in range(N_ACTIONS)
                ]
                best = max(q_vals)
                delta = max(delta, abs(best - V[s]))
                V[s] = best
            if delta < VI_THETA:
                break

        # Derive greedy policy from converged V
        for s in range(N_STATES):
            r, c = self._decode(s)
            if (r, c) == GOAL:
                continue
            self.policy[s] = int(np.argmax([
                sum(p * (rew + (0.0 if done else self.gamma * V[ns]))
                    for p, ns, rew, done in self._transitions(r, c, a, env))
                for a in range(N_ACTIONS)
            ]))

        self.V = V
        self._env_hash = self._env_fingerprint(env)

    def check_and_solve(self, env):
        """Re-solve only if the environment layout has changed."""
        if self._env_fingerprint(env) != self._env_hash:
            self.solve(env)

    # ------------------------------------------------------------------ API

    def choose_action(self, state, env):
        self.check_and_solve(env)
        return int(self.policy[state])

    def get_v_values(self):
        return self.V.reshape(GRID_SIZE, GRID_SIZE)

    def get_best_actions(self):
        return self.policy.reshape(GRID_SIZE, GRID_SIZE)
