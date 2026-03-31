# environment.py — 12x12 grid world for the drone RL agent

import numpy as np
from config import (
    GRID_SIZE, START, GOAL, BUILDINGS, WIND_ZONES,
    REWARD_GOAL, REWARD_STEP, REWARD_BUILDING, REWARD_WIND, MAX_STEPS
)

# Action index -> (row_delta, col_delta)
ACTION_DELTAS = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}
ACTION_NAMES = {0: "UP", 1: "DOWN", 2: "LEFT", 3: "RIGHT"}

# Cell type codes (used for visualization)
CELL_FREE = 0
CELL_BUILDING = 1
CELL_WIND = 2
CELL_START = 3
CELL_GOAL = 4
CELL_PATH = 5
CELL_DRONE = 6


class DroneEnv:
    def __init__(self):
        self.grid_size = GRID_SIZE
        self.buildings = set(BUILDINGS)
        self.wind_zones = set(WIND_ZONES)
        self.start = START
        self.goal = GOAL
        self.pos = START
        self.steps = 0
        self.path = []

    def reset(self):
        self.pos = self.start
        self.steps = 0
        self.path = [self.start]
        return self._encode(self.pos)

    def _encode(self, pos):
        return pos[0] * self.grid_size + pos[1]

    def _is_valid(self, r, c):
        return 0 <= r < self.grid_size and 0 <= c < self.grid_size

    def _wind_push(self, r, c):
        candidates = []
        for dr, dc in ACTION_DELTAS.values():
            nr, nc = r + dr, c + dc
            if self._is_valid(nr, nc) and (nr, nc) not in self.buildings:
                candidates.append((nr, nc))
        if candidates:
            return candidates[np.random.randint(len(candidates))]
        return (r, c)

    def step(self, action):
        dr, dc = ACTION_DELTAS[action]
        nr, nc = self.pos[0] + dr, self.pos[1] + dc

        # Out of bounds -> clamp
        nr = max(0, min(self.grid_size - 1, nr))
        nc = max(0, min(self.grid_size - 1, nc))
        new_pos = (nr, nc)

        # Building: stay in place
        if new_pos in self.buildings:
            reward = REWARD_BUILDING
            self.steps += 1
            done = self.steps >= MAX_STEPS
            return self._encode(self.pos), reward, done

        # Move drone
        self.pos = new_pos

        # Wind zone: random push
        if self.pos in self.wind_zones:
            self.pos = self._wind_push(*self.pos)
            reward = REWARD_WIND
        elif self.pos == self.goal:
            reward = REWARD_GOAL
        else:
            reward = REWARD_STEP

        self.path.append(self.pos)
        self.steps += 1
        done = (self.pos == self.goal) or (self.steps >= MAX_STEPS)
        return self._encode(self.pos), reward, done

    def get_cell_type(self, r, c):
        pos = (r, c)
        if pos in self.buildings:
            return CELL_BUILDING
        if pos in self.wind_zones:
            return CELL_WIND
        if pos == self.start:
            return CELL_START
        if pos == self.goal:
            return CELL_GOAL
        return CELL_FREE

    def get_grid_matrix(self):
        mat = np.zeros((self.grid_size, self.grid_size), dtype=int)
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                mat[r, c] = self.get_cell_type(r, c)
        for p in self.path[1:-1]:
            if mat[p] == CELL_FREE:
                mat[p] = CELL_PATH
        if mat[self.pos] not in (CELL_START, CELL_GOAL):
            mat[self.pos] = CELL_DRONE
        return mat
