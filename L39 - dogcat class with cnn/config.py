"""
config.py
=========================================================
  Global settings, data transforms, and device setup.
  Import this module in all other files.
=========================================================
"""

import torch
import torchvision.transforms as transforms
import numpy as np
import os

# ─────────────────────────────────────────────
#  SETTINGS  (easy to change!)
# ─────────────────────────────────────────────
IMG_SIZE    = 64        # resize every image to 64×64 pixels
BATCH_SIZE  = 32        # process 32 images at a time
EPOCHS      = 15        # how many full passes through the data
LEARN_RATE  = 0.001     # how fast the network learns (step size)
NUM_IMAGES  = 3000      # use only 3000 images total
TRAIN_RATIO = 0.8       # 80% for training, 20% for testing
DATA_DIR    = "./data"  # where to save the downloaded dataset
OUT_DIR     = "./output_images"  # where to save visualization images
SEED        = 42        # for reproducible results

# ─────────────────────────────────────────────
#  REPRODUCIBILITY
# ─────────────────────────────────────────────
torch.manual_seed(SEED)
np.random.seed(SEED)

# ─────────────────────────────────────────────
#  DIRECTORIES
# ─────────────────────────────────────────────
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────
#  DEVICE  (GPU if available, else CPU)
# ─────────────────────────────────────────────
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"\n🖥️  Running on: {device}\n")

# ─────────────────────────────────────────────
#  DATA TRANSFORMS
#
#  Transform pipeline (think of it as a car wash for images):
#    1. Resize to 64×64 pixels
#    2. Random horizontal flip (data augmentation — mirrors the image)
#    3. Convert to a PyTorch tensor  → shape: [3, 64, 64]
#    4. Normalize each channel:
#         mean=[0.485, 0.456, 0.406]  ← average pixel values from ImageNet
#         std =[0.229, 0.224, 0.225]  ← standard deviation from ImageNet
#       This centers the data around 0, which helps the network train faster.
# ─────────────────────────────────────────────
train_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

test_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])
