# agent_qlearn.py — Q-Learning drone (model-free)
#
# How it works:
#   After every step it updates one entry in the Q-table using the Bellman
#   equation:  Q[s,a] += alpha * (reward + gamma * max Q[s'] - Q[s,a])
#   It NEVER looks at the grid layout — it only learns from what it experiences.
#   That makes it flexible but it takes many episodes to warm up.

import numpy as np
from config import GRID_SIZE, ALPHA, GAMMA, EPSILON_START, EPSILON_MIN, EPSILON_DECAY

N_STATES  = GRID_SIZE * GRID_SIZE
N_ACTIONS = 4


class QLearningAgent:
    def __init__(self):
        self.alpha   = ALPHA
        self.gamma   = GAMMA
        self.epsilon = EPSILON_START         # starts fully random, decays over time
        self.Q = np.zeros((N_STATES, N_ACTIONS))

    def choose_action(self, state):
        """Epsilon-greedy: explore randomly or exploit best known action."""
        if np.random.random() < self.epsilon:
            return np.random.randint(N_ACTIONS)
        return int(np.argmax(self.Q[state]))

    def update(self, state, action, reward, next_state, done):
        """One-step Q-Learning update (off-policy Bellman equation)."""
        current = self.Q[state, action]
        target  = reward if done else reward + self.gamma * np.max(self.Q[next_state])
        self.Q[state, action] += self.alpha * (target - current)

    def decay_epsilon(self):
        self.epsilon = max(EPSILON_MIN, self.epsilon * EPSILON_DECAY)

    def get_v_values(self):
        """Best Q-value per state → used for heatmap."""
        return np.max(self.Q, axis=1).reshape(GRID_SIZE, GRID_SIZE)

    def get_best_actions(self):
        """Best action per state → used for policy arrows."""
        return np.argmax(self.Q, axis=1).reshape(GRID_SIZE, GRID_SIZE)
