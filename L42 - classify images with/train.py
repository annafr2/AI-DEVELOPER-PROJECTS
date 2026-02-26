"""
train.py - Two-phase training pipeline for ResNet-50 HCP classifier.
Course: AI Developer Expert | Lesson 42

Phase 1: Frozen backbone — train only the new head (fast, safe warm-up).
Phase 2: Fine-tune top 30 ResNet layers with a tiny learning rate.
"""

import numpy as np
from config import EPOCHS, FINE_TUNE_EPOCHS, MODEL_PATH
from model import build_model, unfreeze_top_layers, get_callbacks, print_summary


# ── Phase 1 ───────────────────────────────────────────────────────────────────

def train_phase1(train_gen, val_data):
    """
    Train the classification head while the ResNet-50 backbone is FROZEN.
    This is safe and fast — we are only learning the new Dense layers.

    Returns: (model, history)
    """
    print("\n" + "=" * 55)
    print("  PHASE 1 — Training head  (backbone frozen)")
    print("=" * 55)

    model = build_model(trainable_backbone=False)
    print_summary(model)

    history = model.fit(
        train_gen,
        validation_data=val_data,
        epochs=EPOCHS,
        callbacks=get_callbacks(),
        verbose=1,
    )
    return model, history


# ── Phase 2 ───────────────────────────────────────────────────────────────────

def train_phase2(model, train_gen, val_data):
    """
    Unfreeze the top 30 ResNet-50 layers and continue training with a very
    small learning rate (fine-tuning). The lower layers keep their ImageNet
    features and are NOT updated.

    Returns: fine-tune history
    """
    print("\n" + "=" * 55)
    print("  PHASE 2 — Fine-tuning  (top 30 layers unfrozen)")
    print("=" * 55)

    model = unfreeze_top_layers(model, n_layers=30)

    ft_history = model.fit(
        train_gen,
        validation_data=val_data,
        epochs=FINE_TUNE_EPOCHS,
        callbacks=get_callbacks(),
        verbose=1,
    )
    return ft_history


# ── Evaluation ────────────────────────────────────────────────────────────────

def evaluate_model(model, test_data):
    """
    Run inference on the held-out test set and print accuracy / loss.

    Returns: (y_true, y_pred, accuracy_float)
    """
    X_test, y_test = test_data
    loss, acc = model.evaluate(X_test, y_test, verbose=0)

    print("\n" + "=" * 55)
    print("  TEST SET RESULTS")
    print(f"  Accuracy : {acc * 100:.2f}%")
    print(f"  Loss     : {loss:.4f}")
    print("=" * 55 + "\n")

    y_pred = np.argmax(model.predict(X_test, verbose=0), axis=1)
    y_true = np.argmax(y_test, axis=1)
    return y_true, y_pred, acc


def answer_research_question(accuracy: float):
    """Print a plain-English answer to the homework research question."""
    threshold = 0.80
    verdict   = "CAN" if accuracy >= threshold else "STRUGGLES TO"
    print("=" * 55)
    print("  RESEARCH QUESTION ANSWER")
    print(f"  'Can ResNet-50 classify cards by HCP?'")
    print(f"  → The model {verdict} do this accurately.")
    print(f"    (Test accuracy = {accuracy * 100:.2f}%  |  threshold = 80%)")
    print("=" * 55 + "\n")
