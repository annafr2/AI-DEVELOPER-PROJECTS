"""
dataset.py - Load the Kaggle Cards dataset and remap to HCP labels.
Course: AI Developer Expert | Lesson 42

The dataset has 53 card classes (e.g. "ace of spades", "two of hearts").
We remap each folder name to an HCP point value (0-4) using RANK_TO_HCP.
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import kagglehub
from config import IMAGE_SIZE, BATCH_SIZE, RANK_TO_HCP, NUM_CLASSES, MAX_IMAGES_PER_CLASS


def download_dataset() -> str:
    """Download the Cards dataset from Kaggle via kagglehub."""
    print("Downloading Cards Image Dataset from Kaggle...")
    path = kagglehub.dataset_download(
        "gpiosenka/cards-image-datasetclassification"
    )
    print(f"Dataset ready at: {path}")
    return path


def _folder_to_hcp(folder_name: str) -> int:
    """
    Map a folder name like 'king of hearts' to its HCP value (0-4).
    Checks if any rank keyword appears in the lowercased folder name.
    """
    name = folder_name.lower()
    for rank, hcp in RANK_TO_HCP.items():
        if rank in name:
            return hcp
    return 0  # Two-Ten and joker are all worth 0 points


def _load_split(split_dir: str):
    """
    Load all images from one dataset split (train / valid / test).
    Returns: X (float32 array, normalised 0-1), y (one-hot, NUM_CLASSES).
    """
    images, labels = [], []
    folders = sorted(
        d for d in os.listdir(split_dir)
        if os.path.isdir(os.path.join(split_dir, d))
    )

    for folder in folders:
        hcp   = _folder_to_hcp(folder)
        fpath = os.path.join(split_dir, folder)
        all_files = [
            f for f in os.listdir(fpath)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]
        # Limit images per class when MAX_IMAGES_PER_CLASS is set (fast mode)
        if MAX_IMAGES_PER_CLASS is not None:
            all_files = all_files[:MAX_IMAGES_PER_CLASS]
        for fname in all_files:
            img = tf.keras.utils.load_img(
                os.path.join(fpath, fname), target_size=IMAGE_SIZE
            )
            images.append(tf.keras.utils.img_to_array(img) / 255.0)
            labels.append(hcp)

    X = np.array(images, dtype="float32")
    y = tf.keras.utils.to_categorical(labels, num_classes=NUM_CLASSES)
    print(f"  [{split_dir.split(os.sep)[-1]:5s}] {len(X):5d} images loaded")
    return X, y


def get_data_generators(dataset_root: str):
    """
    Build train generator (with augmentation) + validation / test arrays.

    Returns:
        train_gen  - augmented ImageDataGenerator flow
        val_data   - (X_val,  y_val)  tuple
        test_data  - (X_test, y_test) tuple
    """
    print("\nLoading dataset splits...")
    X_tr, y_tr = _load_split(os.path.join(dataset_root, "train"))
    X_va, y_va = _load_split(os.path.join(dataset_root, "valid"))
    X_te, y_te = _load_split(os.path.join(dataset_root, "test"))

    # Describe class distribution so we can spot imbalance early
    print("\nHCP class distribution in TRAIN set:")
    raw_labels = np.argmax(y_tr, axis=1)
    from config import HCP_CLASSES
    for cls, name in HCP_CLASSES.items():
        count = int((raw_labels == cls).sum())
        print(f"  Class {cls} | {name:14s} | {count:4d} images")

    # Augmentation applied only to training images
    aug = ImageDataGenerator(
        rotation_range=15,
        width_shift_range=0.10,
        height_shift_range=0.10,
        horizontal_flip=True,
        zoom_range=0.10,
        brightness_range=[0.85, 1.15],
    )
    train_gen = aug.flow(X_tr, y_tr, batch_size=BATCH_SIZE, shuffle=True)

    return train_gen, (X_va, y_va), (X_te, y_te)
