"""Dueling DQN: shared encoder → Value stream V(s) + Advantage stream A(s,a)."""
import torch
import torch.nn as nn
import config


class DuelingDQN(nn.Module):
    """
    Q(s,a) = V(s) + A(s,a) - mean_a(A(s,a'))

    Input : (batch, WINDOW_SIZE, FEATURES_COUNT)  — flattened internally
    Output: (batch, n_actions=3)
    """

    def __init__(self, n_actions: int = 3):
        super().__init__()
        input_dim = config.WINDOW_SIZE * config.FEATURES_COUNT

        # Shared feature extractor
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, config.HIDDEN_DIM),
            nn.ReLU(),
            nn.Linear(config.HIDDEN_DIM, config.HIDDEN_DIM),
            nn.ReLU(),
        )

        # Value stream: scalar V(s)
        self.value_stream = nn.Sequential(
            nn.Linear(config.HIDDEN_DIM, config.HIDDEN_DIM // 2),
            nn.ReLU(),
            nn.Linear(config.HIDDEN_DIM // 2, 1),
        )

        # Advantage stream: A(s,a) per action
        self.advantage_stream = nn.Sequential(
            nn.Linear(config.HIDDEN_DIM, config.HIDDEN_DIM // 2),
            nn.ReLU(),
            nn.Linear(config.HIDDEN_DIM // 2, n_actions),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x.reshape(x.size(0), -1)
        features   = self.encoder(x)
        value      = self.value_stream(features)
        advantage  = self.advantage_stream(features)
        q = value + advantage - advantage.mean(dim=1, keepdim=True)
        return q

    def value_advantage(self, x: torch.Tensor):
        """Return (value, advantage) tensors — used for visualisation."""
        x = x.reshape(x.size(0), -1)
        features  = self.encoder(x)
        value     = self.value_stream(features)
        advantage = self.advantage_stream(features)
        return value, advantage
