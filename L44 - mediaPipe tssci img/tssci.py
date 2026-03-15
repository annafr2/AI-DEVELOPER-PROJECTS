"""
tssci.py — Build a 49x49x3 TSSCI image from extracted skeleton frames.

Paper reference: Segal et al., "Using EfficientNet-B7, VAE and Siamese Twins
Networks to Evaluate Human Exercises as Super Objects in TSSCI Images",
Journal of Personalized Medicine, 2023, 13, 874.

TSSCI = Tree Structure Skeleton Color Image
  - Rows    : sampled video frames  (time axis)
  - Columns : landmarks in DFS body-tree order
  - Channels: R = X coord, G = Y coord, B = Confidence
"""
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from config import (
    DFS_ORDER, NUM_FRAMES, NUM_KEYPOINTS,
    CONF_THRESH, TSSCI_PNG, TSSCI_UPSCALED_PNG, TSSCI_PLOT_PNG, TSSCI_UPSCALE,
)


def sample_frames(skeleton_data: list, n: int = NUM_FRAMES) -> list:
    """Sample n evenly-spaced frames from the full skeleton sequence."""
    total = len(skeleton_data)
    if total == 0:
        return []
    indices = np.linspace(0, total - 1, min(n, total), dtype=int)
    return [skeleton_data[i] for i in indices]


def _complement_missing(lm: np.ndarray) -> np.ndarray:
    """
    Replace low-confidence keypoints with their nearest left neighbour
    (paper Section 2.3, 'complement from the left' rule).
    """
    out = lm.copy()
    if out[0, 2] < CONF_THRESH and len(out) > 1:
        out[0] = out[1]
    for i in range(1, len(out)):
        if out[i, 2] < CONF_THRESH:
            out[i] = out[i - 1]
    return out


def _to_dfs_vector(landmarks: np.ndarray) -> np.ndarray:
    """Reorder 33 MediaPipe landmarks to 49-entry DFS sequence → shape (49, 3)."""
    lm = _complement_missing(landmarks)
    return np.array([lm[i] for i in DFS_ORDER], dtype=np.float32)


def build_tssci(sampled: list) -> np.ndarray:
    """
    Build the 49x49x3 TSSCI array (float32, values in [0, 1]).

    Steps (following paper):
      1. Reorder each frame's landmarks via DFS traversal.
      2. Global min-max normalise X and Y across all 49 frames.
      3. Clip confidence to [0, 1].
    Returns shape: (NUM_FRAMES, NUM_KEYPOINTS, 3)
    """
    raw = np.zeros((NUM_FRAMES, NUM_KEYPOINTS, 3), dtype=np.float32)
    for i, frame in enumerate(sampled[:NUM_FRAMES]):
        raw[i] = _to_dfs_vector(frame["landmarks"])

    # Global min-max normalisation for X (ch=0) and Y (ch=1) across all frames
    for ch in range(2):
        vmin = raw[:, :, ch].min()
        vmax = raw[:, :, ch].max()
        if vmax > vmin:
            raw[:, :, ch] = (raw[:, :, ch] - vmin) / (vmax - vmin)

    raw[:, :, 2] = np.clip(raw[:, :, 2], 0.0, 1.0)
    return raw


def save_tssci(tssci: np.ndarray, upscale: int = TSSCI_UPSCALE) -> None:
    """Save the TSSCI array as PNG — original (49x49) and upscaled."""
    img_u8 = (tssci * 255).astype(np.uint8)
    small = Image.fromarray(img_u8, mode="RGB")
    small.save(TSSCI_PNG)
    print(f"TSSCI image saved : {TSSCI_PNG}  (49x49 px)")

    big = small.resize((49 * upscale, 49 * upscale), resample=Image.NEAREST)
    big.save(TSSCI_UPSCALED_PNG)
    print(f"TSSCI upscaled    : {TSSCI_UPSCALED_PNG}  ({49*upscale}x{49*upscale} px)")


def plot_tssci(tssci: np.ndarray) -> None:
    """Save a labeled matplotlib figure of the TSSCI image."""
    fig, ax = plt.subplots(figsize=(6, 6), facecolor="#0d0d1a")
    ax.set_facecolor("#0d0d1a")
    ax.imshow(tssci, aspect="auto", interpolation="nearest")
    ax.set_title("TSSCI Image  (49 × 49 × 3)", color="white", fontsize=13, pad=10)
    ax.set_xlabel("Keypoint index  (DFS order)", color="#aaaacc", fontsize=10)
    ax.set_ylabel("Frame index  (time →)", color="#aaaacc", fontsize=10)
    ax.tick_params(colors="#aaaacc")
    for sp in ax.spines.values():
        sp.set_color("#444466")
    plt.tight_layout()
    plt.savefig(TSSCI_PLOT_PNG, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"TSSCI plot saved  : {TSSCI_PLOT_PNG}")
