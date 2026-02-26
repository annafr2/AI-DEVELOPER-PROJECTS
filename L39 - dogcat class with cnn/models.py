"""
models.py
=========================================================
  Model definitions:
    - CNNModel  : Convolutional Neural Network
    - FCModel   : Fully Connected (MLP) Network
=========================================================
"""

import torch.nn as nn
from config import IMG_SIZE


# ─────────────────────────────────────────────
#  MODEL 1: CNN  (Convolutional Neural Network)
#
#  How a CNN works (like a detective looking for clues):
#    Conv Layer 1 → looks for simple patterns (edges, colors)
#    Conv Layer 2 → combines simple patterns into shapes (ears, noses)
#    Conv Layer 3 → recognizes complex features (faces!)
#    Fully Connected → decides: "this is a cat" or "this is a dog"
#
#  INPUT  TENSOR SHAPE: [batch, 3, 64, 64]
#  LAYER BY LAYER:
#    Conv1(3→32):   [32, 3, 64, 64] → [32, 32, 64, 64]
#    Pool:          [32, 32, 64, 64] → [32, 32, 32, 32]
#    Conv2(32→64):  [32, 32, 32, 32] → [32, 64, 32, 32]
#    Pool:          [32, 64, 32, 32] → [32, 64, 16, 16]
#    Conv3(64→128): [32, 64, 16, 16] → [32, 128, 16, 16]
#    Pool:          [32, 128,16, 16] → [32, 128, 8, 8]
#    Flatten:       [32, 128, 8, 8]  → [32, 8192]
#    FC1(8192→512): [32, 8192]       → [32, 512]
#    FC2(512→2):    [32, 512]        → [32, 2]  ← cat or dog!
# ─────────────────────────────────────────────
class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()

        # ---- FEATURE EXTRACTOR (convolutional part) ----
        self.features = nn.Sequential(
            # Block 1: detect basic edges and colors
            nn.Conv2d(in_channels=3,  out_channels=32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),     # 64→32
            nn.Dropout2d(p=0.1),

            # Block 2: detect shapes and textures
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),     # 32→16
            nn.Dropout2d(p=0.2),

            # Block 3: detect complex features (facial structure)
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),     # 16→8
            nn.Dropout2d(p=0.3),
        )

        # ---- CLASSIFIER (fully connected part) ----
        # After feature extraction: 128 channels × 8×8 pixels = 8192 values
        self.classifier = nn.Sequential(
            nn.Flatten(),                              # [batch, 128, 8, 8] → [batch, 8192]
            nn.Linear(128 * 8 * 8, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.5),
            nn.Linear(512, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.3),
            nn.Linear(128, 2),                        # 2 outputs: cat, dog
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x   # raw logits — softmax applied during loss calculation


# ─────────────────────────────────────────────
#  MODEL 2: Fully Connected Network  (FC / MLP)
#
#  How FC works (like a flat list of neurons):
#    - Takes the ENTIRE image as a flat list of numbers
#    - No spatial awareness (doesn't know that pixels are neighbors)
#    - Each neuron connects to EVERY neuron in the next layer
#
#  INPUT TENSOR SHAPE: [batch, 3, 64, 64]
#    → Flatten first: [batch, 3×64×64] = [batch, 12288]
#  LAYER BY LAYER:
#    Flatten:        [32, 3, 64, 64] → [32, 12288]
#    FC1(12288→512): [32, 12288]     → [32, 512]
#    FC2(512→256):   [32, 512]       → [32, 256]
#    FC3(256→128):   [32, 256]       → [32, 128]
#    FC4(128→2):     [32, 128]       → [32, 2]  ← cat or dog!
# ─────────────────────────────────────────────
class FCModel(nn.Module):
    def __init__(self):
        super(FCModel, self).__init__()

        self.network = nn.Sequential(
            nn.Flatten(),                              # [batch, 3, 64, 64] → [batch, 12288]

            nn.Linear(3 * IMG_SIZE * IMG_SIZE, 512),  # 12288 → 512
            nn.BatchNorm1d(512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.4),

            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.4),

            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.3),

            nn.Linear(128, 2),                        # final: 2 classes
        )

    def forward(self, x):
        return self.network(x)
