"""
training.py
=========================================================
  Data loading and training functions:
    - load_datasets()  : download & split the dataset
    - train_epoch()    : one training epoch
    - evaluate()       : evaluate on test set
    - train_model()    : full training loop for one model
=========================================================
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Subset, random_split
from torchvision.datasets import OxfordIIITPet
import time

from config import (
    DATA_DIR, BATCH_SIZE, NUM_IMAGES, TRAIN_RATIO,
    EPOCHS, LEARN_RATE, SEED, train_transform
)


# ─────────────────────────────────────────────
#  DATASET LOADING
#
#  OxfordIIITPet: 37 pet breeds (cats & dogs)
#  target_types="binary_category" → 0=cat, 1=dog
#  We use only the first 3000 images (Subset).
# ─────────────────────────────────────────────
def load_datasets():
    print("📦 Loading Oxford-IIIT Pet Dataset...")

    full_dataset = OxfordIIITPet(
        root=DATA_DIR,
        split="trainval",
        target_types="binary_category",
        transform=train_transform,
        download=True,
    )

    # Take only NUM_IMAGES samples for speed
    indices = list(range(min(NUM_IMAGES, len(full_dataset))))
    dataset = Subset(full_dataset, indices)

    n_train = int(len(dataset) * TRAIN_RATIO)
    n_test  = len(dataset) - n_train
    train_set, test_set = random_split(
        dataset, [n_train, n_test],
        generator=torch.Generator().manual_seed(SEED)
    )

    train_loader = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True,  num_workers=2)
    test_loader  = DataLoader(test_set,  batch_size=BATCH_SIZE, shuffle=False, num_workers=2)

    print(f"   ✓ Total images  : {len(dataset)}")
    print(f"   ✓ Training set  : {n_train} images")
    print(f"   ✓ Test set      : {n_test} images")
    print(f"   ✓ Batch size    : {BATCH_SIZE}\n")

    return train_loader, test_loader


# ─────────────────────────────────────────────
#  TRAINING FUNCTION
# ─────────────────────────────────────────────
def train_epoch(model, loader, criterion, optimizer, device):
    """Train for one full epoch. Returns (avg_loss, accuracy)."""
    model.train()
    total_loss, correct, total = 0.0, 0, 0

    for images, labels in loader:
        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()           # clear old gradients
        outputs = model(images)         # forward pass
        loss = criterion(outputs, labels)
        loss.backward()                 # backward pass (compute gradients)
        optimizer.step()                # update weights

        total_loss += loss.item() * images.size(0)
        _, predicted = outputs.max(1)
        correct += predicted.eq(labels).sum().item()
        total   += labels.size(0)

    return total_loss / total, correct / total


# ─────────────────────────────────────────────
#  EVALUATION FUNCTION
# ─────────────────────────────────────────────
def evaluate(model, loader, criterion, device):
    """Evaluate on test set. Returns (avg_loss, accuracy)."""
    model.eval()
    total_loss, correct, total = 0.0, 0, 0

    with torch.no_grad():               # no need to track gradients when testing
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            loss    = criterion(outputs, labels)

            total_loss += loss.item() * images.size(0)
            _, predicted = outputs.max(1)
            correct += predicted.eq(labels).sum().item()
            total   += labels.size(0)

    return total_loss / total, correct / total


# ─────────────────────────────────────────────
#  TRAINING LOOP — runs one model end-to-end
# ─────────────────────────────────────────────
def train_model(model, model_name, train_loader, test_loader, device):
    """Full training loop for one model. Returns history dict."""
    model = model.to(device)
    criterion = nn.CrossEntropyLoss()   # measures how wrong the predictions are
    optimizer = optim.Adam(model.parameters(), lr=LEARN_RATE, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS)

    history = {
        "train_loss": [], "train_acc": [],
        "test_loss":  [], "test_acc":  [],
        "epoch_times": [],
    }

    print(f"\n{'='*55}")
    print(f"  Training: {model_name}")
    print(f"  Parameters: {sum(p.numel() for p in model.parameters()):,}")
    print(f"{'='*55}")
    print(f"  {'Epoch':>5} | {'TrainLoss':>9} | {'TrainAcc':>8} | "
          f"{'TestLoss':>8} | {'TestAcc':>7} | {'Time':>6}")
    print(f"  {'-'*55}")

    total_start = time.time()

    for epoch in range(1, EPOCHS + 1):
        t0 = time.time()

        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
        test_loss,  test_acc  = evaluate(model, test_loader, criterion, device)

        scheduler.step()
        elapsed = time.time() - t0

        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["test_loss"].append(test_loss)
        history["test_acc"].append(test_acc)
        history["epoch_times"].append(elapsed)

        print(f"  {epoch:>5} | {train_loss:>9.4f} | {train_acc*100:>7.2f}% | "
              f"{test_loss:>8.4f} | {test_acc*100:>6.2f}% | {elapsed:>5.1f}s")

    total_time = time.time() - total_start
    history["total_time"] = total_time
    history["model_name"] = model_name
    print(f"\n  ✅ Total training time: {total_time:.1f}s")
    print(f"  ✅ Best test accuracy:  {max(history['test_acc'])*100:.2f}%\n")

    return history
