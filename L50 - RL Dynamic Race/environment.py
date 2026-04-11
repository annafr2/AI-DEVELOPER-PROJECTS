# environment.py — dynamic 12x12 grid world with random events

import numpy as np
from config import (
    GRID_SIZE, START, GOAL, BUILDINGS, WIND_ZONES,
    REWARD_GOAL, REWARD_STEP, REWARD_BUILDING, REWARD_WIND,
    REWARD_PIT, REWARD_BRIDGE, MAX_STEPS,
    EVENT_INTERVAL, MAX_DYNAMIC, EVENT_TYPES, EVENT_WEIGHTS, EVENT_LIFETIME,
)

ACTION_DELTAS = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}

# Cell type codes (used by visualizer)
CELL_FREE       = 0
CELL_BUILDING   = 1
CELL_WIND       = 2
CELL_START      = 3
CELL_GOAL       = 4
CELL_PATH       = 5
CELL_DRONE      = 6
CELL_PIT        = 7   # dynamic: drone falls in, big penalty, episode ends
CELL_BRIDGE     = 8   # dynamic: bonus points
CELL_DYN_BARRIER = 9  # dynamic: temporary wall
CELL_DYN_WIND   = 10  # dynamic: extra wind zone


class DroneEnv:
    def __init__(self):
        self.grid_size    = GRID_SIZE
        self.static_buildings = set(BUILDINGS)
        self.static_wind      = set(WIND_ZONES)
        self.start = START
        self.goal  = GOAL
        self._events = {}   # {pos: (event_type, birth_episode)}
        self.pos   = START
        self.steps = 0
        self.path  = []
        self._refresh_sets()

    def _refresh_sets(self):
        """Recompute active cell sets from static + dynamic events."""
        self.buildings  = set(self.static_buildings)
        self.wind_zones = set(self.static_wind)
        self.pits    = set()
        self.bridges = set()
        for pos, (etype, _) in self._events.items():
            if etype == "barrier": self.buildings.add(pos)
            elif etype == "wind":  self.wind_zones.add(pos)
            elif etype == "pit":   self.pits.add(pos)
            elif etype == "bridge": self.bridges.add(pos)

    def _random_free_cell(self):
        reserved = self.buildings | self.pits | self.bridges | {self.start, self.goal}
        cells = [(r, c) for r in range(self.grid_size)
                 for c in range(self.grid_size) if (r, c) not in reserved]
        return cells[np.random.randint(len(cells))] if cells else None

    def maybe_spawn_event(self, episode):
        """Expire old events; maybe add a new one every EVENT_INTERVAL episodes."""
        expired = [p for p, (_, born) in self._events.items()
                   if episode - born >= EVENT_LIFETIME]
        for p in expired:
            del self._events[p]
        if episode % EVENT_INTERVAL == 0 and len(self._events) < MAX_DYNAMIC:
            pos = self._random_free_cell()
            if pos:
                etype = np.random.choice(EVENT_TYPES, p=EVENT_WEIGHTS)
                self._events[pos] = (etype, episode)
        self._refresh_sets()

    def reset(self):
        self.pos   = self.start
        self.steps = 0
        self.path  = [self.start]
        return self._encode(self.pos)

    def _encode(self, pos):
        return pos[0] * self.grid_size + pos[1]

    def _is_valid(self, r, c):
        return 0 <= r < self.grid_size and 0 <= c < self.grid_size

    def _wind_push(self, r, c):
        candidates = [
            (r + dr, c + dc) for dr, dc in ACTION_DELTAS.values()
            if self._is_valid(r + dr, c + dc) and (r + dr, c + dc) not in self.buildings
        ]
        return candidates[np.random.randint(len(candidates))] if candidates else (r, c)

    def step(self, action):
        dr, dc = ACTION_DELTAS[action]
        nr = max(0, min(self.grid_size - 1, self.pos[0] + dr))
        nc = max(0, min(self.grid_size - 1, self.pos[1] + dc))
        new_pos = (nr, nc)

        # Building: bounce back, pay penalty
        if new_pos in self.buildings:
            self.steps += 1
            return self._encode(self.pos), REWARD_BUILDING, self.steps >= MAX_STEPS

        self.pos = new_pos

        # Pit: fall in → episode ends immediately
        if self.pos in self.pits:
            self.path.append(self.pos)
            self.steps += 1
            return self._encode(self.pos), REWARD_PIT, True

        # Wind: enter cell, then get pushed to a random neighbor
        if self.pos in self.wind_zones:
            self.pos = self._wind_push(*self.pos)
            reward = REWARD_WIND
        elif self.pos in self.bridges:
            reward = REWARD_BRIDGE
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
        if pos in self._events:
            etype = self._events[pos][0]
            return {
                "pit": CELL_PIT, "bridge": CELL_BRIDGE,
                "barrier": CELL_DYN_BARRIER, "wind": CELL_DYN_WIND,
            }.get(etype, CELL_FREE)
        if pos in self.static_buildings: return CELL_BUILDING
        if pos in self.static_wind:      return CELL_WIND
        if pos == self.start:            return CELL_START
        if pos == self.goal:             return CELL_GOAL
        return CELL_FREE

    def get_grid_matrix(self):
        mat = np.array([[self.get_cell_type(r, c) for c in range(self.grid_size)]
                        for r in range(self.grid_size)], dtype=int)
        for p in self.path[1:-1]:
            if mat[p] == CELL_FREE:
                mat[p] = CELL_PATH
        if mat[self.pos] not in (CELL_START, CELL_GOAL):
            mat[self.pos] = CELL_DRONE
        return mat
