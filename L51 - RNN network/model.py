import torch
import torch.nn as nn
from config import DEFAULT_EMBED_SIZE, DEFAULT_HIDDEN_SIZE, DEFAULT_NUM_LAYERS, DEFAULT_DROPOUT


class RNNLanguageModel(nn.Module):
    """
    Vanilla RNN language model.
    Predicts the next word given a sequence of previous words.
    Uses nn.RNN (not LSTM/GRU) to clearly demonstrate the vanishing gradient effect.
    """

    def __init__(self, vocab_size, embed_size=DEFAULT_EMBED_SIZE,
                 hidden_size=DEFAULT_HIDDEN_SIZE, num_layers=DEFAULT_NUM_LAYERS,
                 dropout=DEFAULT_DROPOUT):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.embedding = nn.Embedding(vocab_size, embed_size, padding_idx=0)
        self.rnn = nn.RNN(
            input_size=embed_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
            nonlinearity="tanh",
        )
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, vocab_size)
        self._init_weights()

    def _init_weights(self):
        nn.init.uniform_(self.embedding.weight, -0.1, 0.1)
        nn.init.xavier_uniform_(self.fc.weight)
        nn.init.zeros_(self.fc.bias)

    def forward(self, x, hidden=None):
        embed = self.dropout(self.embedding(x))
        output, hidden = self.rnn(embed, hidden)
        output = self.dropout(output)
        logits = self.fc(output)
        return logits, hidden

    def init_hidden(self, batch_size, device):
        return torch.zeros(self.num_layers, batch_size, self.hidden_size, device=device)

    def count_parameters(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


def create_model(vocab_size, hidden_size=DEFAULT_HIDDEN_SIZE, num_layers=DEFAULT_NUM_LAYERS):
    return RNNLanguageModel(vocab_size=vocab_size, hidden_size=hidden_size, num_layers=num_layers)
