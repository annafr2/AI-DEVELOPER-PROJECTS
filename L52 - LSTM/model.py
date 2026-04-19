# model.py — LSTM filter network definition

import torch
import torch.nn as nn
import config


class LSTMFilter(nn.Module):
    """
    LSTM-based frequency filter.

    Given a window of WINDOW_SIZE noisy mixed-signal samples,
    predicts the next clean value of the target frequency.

    Architecture
    ------------
    Input  : (batch, WINDOW_SIZE, 1)
    LSTM   : hidden_size units, num_layers stacked layers
    Linear : hidden_size → 1
    Output : (batch, 1)
    """

    def __init__(
        self,
        hidden_size: int = config.HIDDEN_SIZE,
        num_layers: int = config.NUM_LAYERS,
        dropout: float = config.DROPOUT,
    ):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=1,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.head = nn.Linear(hidden_size, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        x : (batch, window_size, 1)
        returns : (batch, 1)
        """
        out, _ = self.lstm(x)       # (batch, window_size, hidden)
        last = out[:, -1, :]        # take last timestep: (batch, hidden)
        return self.head(last)      # (batch, 1)


def build_model() -> LSTMFilter:
    """Instantiate the model and move to available device."""
    model = LSTMFilter()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return model.to(device)


def count_parameters(model: nn.Module) -> int:
    return sum(p.numel() for p in model.parameters() if p.requires_grad)
