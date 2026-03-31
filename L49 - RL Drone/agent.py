# agent.py — Q-learning agent for the drone

import numpy as np
from config import (
    GRID_SIZE, ALPHA, GAMMA,
    EPSILON_START, EPSILON_MIN, EPSILON_DECAY
)

N_STATES = GRID_SIZE * GRID_SIZE
N_ACTIONS = 4


class QLearningAgent:
    def __init__(self):
        self.alpha = ALPHA
        self.gamma = GAMMA
        self.epsilon = EPSILON_START
        self.Q = np.zeros((N_STATES, N_ACTIONS))

    def choose_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.randint(N_ACTIONS)
        return int(np.argmax(self.Q[state]))

    def update(self, state, action, reward, next_state, done):
        current = self.Q[state, action]
        target = reward if done else reward + self.gamma * np.max(self.Q[next_state])
        self.Q[state, action] += self.alpha * (target - current)

    def decay_epsilon(self):
        self.epsilon = max(EPSILON_MIN, self.epsilon * EPSILON_DECAY)

    def get_v_values(self):
        return np.max(self.Q, axis=1).reshape(GRID_SIZE, GRID_SIZE)

    def get_best_actions(self):
        return np.argmax(self.Q, axis=1).reshape(GRID_SIZE, GRID_SIZE)
