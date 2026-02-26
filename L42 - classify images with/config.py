"""
config.py - Configuration constants for Bridge Card HCP Classifier
Course: AI Developer Expert | Lesson 42
"""

import os

# ── Output paths ──────────────────────────────────────────────────────────────
OUTPUT_DIR             = "outputs"
MODEL_PATH             = os.path.join(OUTPUT_DIR, "resnet50_hcp_model.keras")
HISTORY_PLOT           = os.path.join(OUTPUT_DIR, "training_history.png")
CONFUSION_MATRIX_PLOT  = os.path.join(OUTPUT_DIR, "confusion_matrix.png")
SAMPLE_PREDICTIONS_PLOT= os.path.join(OUTPUT_DIR, "sample_predictions.png")

# ── Mode switch ───────────────────────────────────────────────────────────────
# Set FAST_MODE = True for CPU training (~45-90 min).
# Set FAST_MODE = False for full quality run (GPU recommended, ~30-45 min).
FAST_MODE = True

# ── Model hyper-parameters ────────────────────────────────────────────────────
# FAST_MODE: smaller images + fewer epochs = much quicker on CPU
IMAGE_SIZE       = (112, 112) if FAST_MODE else (224, 224)
BATCH_SIZE       = 64         if FAST_MODE else 32
EPOCHS           = 8          if FAST_MODE else 20   # Phase 1: frozen backbone
LEARNING_RATE    = 1e-4
FINE_TUNE_EPOCHS = 5          if FAST_MODE else 10   # Phase 2: unfrozen top layers
FINE_TUNE_LR     = 1e-5

# Max images loaded per folder in train split (None = load all)
# 40 imgs/folder × 53 folders ≈ 2,100 train images total
MAX_IMAGES_PER_CLASS = 40 if FAST_MODE else None

# ── HCP (High Card Points) Rules ──────────────────────────────────────────────
# Bridge scoring: Ace=4, King=3, Queen=2, Jack=1, all others=0
# We classify INDIVIDUAL card images into 5 point-value classes.
#
# Class 0: cards worth 0 pts  (Two through Ten, Joker)
# Class 1: Jacks   → 1 pt
# Class 2: Queens  → 2 pts
# Class 3: Kings   → 3 pts
# Class 4: Aces    → 4 pts

NUM_CLASSES = 5

HCP_CLASSES = {
    0: "0 pts  (2–10)",
    1: "J = 1 pt",
    2: "Q = 2 pts",
    3: "K = 3 pts",
    4: "A = 4 pts",
}

# Map rank keyword (found in folder name) → HCP value
RANK_TO_HCP = {
    "ace":   4,
    "king":  3,
    "queen": 2,
    "jack":  1,
    # Two-through-Ten + joker fall through to default → 0
}

# One color per HCP class (used in all plots)
CLASS_COLORS = ["#4472C4", "#ED7D31", "#70AD47", "#FFC000", "#E63946"]
