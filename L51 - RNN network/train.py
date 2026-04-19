import torch
import torch.nn as nn
import numpy as np
import time
from config import EPOCHS, LEARNING_RATE, CLIP_GRAD


def _run_epoch(model, loader, optimizer, criterion, device, training=True):
    model.train(training)
    total_loss, correct, total = 0.0, 0, 0
    ctx = torch.enable_grad() if training else torch.no_grad()

    with ctx:
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            hidden = model.init_hidden(x.size(0), device)
            if training:
                hidden = hidden.detach()
                optimizer.zero_grad()

            logits, hidden = model(x, hidden)
            loss = criterion(logits.view(-1, logits.size(-1)), y.view(-1))

            if training:
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), CLIP_GRAD)
                optimizer.step()

            n = y.numel()
            total_loss += loss.item() * n
            correct += (logits.argmax(-1) == y).sum().item()
            total += n

    avg_loss = total_loss / total
    perplexity = float(np.exp(min(avg_loss, 20)))  # cap to avoid inf
    return avg_loss, correct / total, perplexity


def train_model(model, train_loader, val_loader, device, epochs=EPOCHS, lr=LEARNING_RATE):
    criterion = nn.CrossEntropyLoss(ignore_index=0)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)

    keys = ["train_loss", "val_loss", "train_acc", "val_acc", "train_ppl", "val_ppl"]
    history = {k: [] for k in keys}

    for epoch in range(1, epochs + 1):
        t0 = time.time()
        tr_loss, tr_acc, tr_ppl = _run_epoch(model, train_loader, optimizer, criterion, device, True)
        vl_loss, vl_acc, vl_ppl = _run_epoch(model, val_loader, None, criterion, device, False)
        scheduler.step()

        for k, v in zip(keys, [tr_loss, vl_loss, tr_acc, vl_acc, tr_ppl, vl_ppl]):
            history[k].append(v)

        print(f"  Epoch {epoch:2d}/{epochs} | "
              f"Loss {tr_loss:.3f}/{vl_loss:.3f} | "
              f"Acc {tr_acc:.3f}/{vl_acc:.3f} | "
              f"PPL {tr_ppl:.1f}/{vl_ppl:.1f} | {time.time() - t0:.1f}s")

    return history


def evaluate_test(model, test_tokens, seq_len, device):
    """Final evaluation on the 20% held-out test set."""
    from dataset import SequenceDataset
    from torch.utils.data import DataLoader
    test_ds = SequenceDataset(test_tokens, seq_len, max_sequences=10000)
    test_loader = DataLoader(test_ds, batch_size=64, num_workers=0)
    criterion = nn.CrossEntropyLoss(ignore_index=0)
    loss, acc, ppl = _run_epoch(model, test_loader, None, criterion, device, False)
    print(f"  TEST SET: Loss={loss:.4f} | Acc={acc:.4f} | PPL={ppl:.1f}")
    return loss, acc, ppl
