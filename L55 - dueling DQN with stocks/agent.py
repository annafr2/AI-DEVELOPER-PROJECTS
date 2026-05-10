"""Dueling DQN agent: replay buffer, epsilon-greedy policy, Double-DQN update."""
import random
import copy
from collections import deque

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

import config
from model import DuelingDQN


class ReplayBuffer:
    def __init__(self, capacity: int = config.REPLAY_BUFFER_SIZE):
        self._buf = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self._buf.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int):
        batch = random.sample(self._buf, batch_size)
        s, a, r, ns, d = zip(*batch)
        return (
            torch.tensor(np.array(s),  dtype=torch.float32),
            torch.tensor(a,            dtype=torch.long),
            torch.tensor(r,            dtype=torch.float32),
            torch.tensor(np.array(ns), dtype=torch.float32),
            torch.tensor(d,            dtype=torch.float32),
        )

    def __len__(self):
        return len(self._buf)


class DQNAgent:
    def __init__(self, n_actions: int = 3):
        self.n_actions  = n_actions
        self.epsilon    = config.EPSILON_START
        self.device     = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.policy_net = DuelingDQN(n_actions).to(self.device)
        self.target_net = copy.deepcopy(self.policy_net).to(self.device)
        self.target_net.eval()

        self.optimizer  = optim.Adam(self.policy_net.parameters(), lr=config.LEARNING_RATE)
        self.buffer     = ReplayBuffer()
        self.step_count = 0
        self.losses     = []

    def select_action(self, state: np.ndarray) -> int:
        if random.random() < self.epsilon:
            return random.randrange(self.n_actions)
        t = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(self.device)
        with torch.no_grad():
            return int(self.policy_net(t).argmax(dim=1).item())

    def store(self, state, action, reward, next_state, done):
        self.buffer.push(state, action, reward, next_state, done)

    def learn(self) -> float | None:
        if len(self.buffer) < config.BATCH_SIZE:
            return None

        s, a, r, ns, d = [x.to(self.device) for x in self.buffer.sample(config.BATCH_SIZE)]

        # Double DQN: policy net chooses best action, target net evaluates it
        with torch.no_grad():
            best_a  = self.policy_net(ns).argmax(dim=1, keepdim=True)
            tgt_q   = self.target_net(ns).gather(1, best_a).squeeze(1)
            y       = r + config.GAMMA * tgt_q * (1 - d)

        q_pred = self.policy_net(s).gather(1, a.unsqueeze(1)).squeeze(1)
        loss   = nn.SmoothL1Loss()(q_pred, y)

        self.optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(self.policy_net.parameters(), 1.0)
        self.optimizer.step()

        self.step_count += 1
        if self.step_count % config.TARGET_UPDATE_FREQ == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())

        loss_val = loss.item()
        self.losses.append(loss_val)
        return loss_val

    def decay_epsilon(self):
        self.epsilon = max(config.EPSILON_END, self.epsilon * config.EPSILON_DECAY)

    def save(self, path: str):
        torch.save(self.policy_net.state_dict(), path)

    def load(self, path: str):
        self.policy_net.load_state_dict(torch.load(path, map_location=self.device))
        self.target_net.load_state_dict(self.policy_net.state_dict())
