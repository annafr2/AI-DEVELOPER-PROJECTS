"""
config.py — All constants and paths for L44 MediaPipe TSSCI project.
"""
from pathlib import Path

# --- Input ---
VIDEO_PATH = (
    "C:/Users/annaf/OneDrive/Desktop/\u05ea\u05d5\u05db\u05df"
    "/\u05db\u05dc\u05d9 2026 \u05e4\u05dc\u05d5\u05e1/0224.mp4"
)
LOCAL_VIDEO = "input_video.mp4"   # local copy (avoids Unicode path issues)

# --- Output directory ---
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

SKELETON_GIF       = OUTPUT_DIR / "skeleton_overlay.gif"
TSSCI_PNG          = OUTPUT_DIR / "tssci_image.png"
TSSCI_UPSCALED_PNG = OUTPUT_DIR / "tssci_upscaled.png"
TSSCI_PLOT_PNG     = OUTPUT_DIR / "tssci_plot.png"
ANIMATED_FLYER_GIF = OUTPUT_DIR / "animated_flyer.gif"

# --- TSSCI parameters (from paper: Segal et al., JPM 2023) ---
NUM_FRAMES    = 49          # frames sampled per clip  → rows in TSSCI
NUM_KEYPOINTS = 49          # DFS-expanded landmarks   → cols in TSSCI
CONF_THRESH   = 0.3         # below this → use left-neighbour complement
TSSCI_UPSCALE = 8           # 49 * 8 = 392 px display size

# --- MediaPipe Pose DFS traversal → 49 entries ---
# MediaPipe provides 33 landmarks (0-32).
# We do a depth-first traversal of the body skeleton tree,
# revisiting parent nodes on backtrack (exactly as in the paper).
# Result: 49-entry sequence used as the column axis of the TSSCI image.
DFS_ORDER = [
    # Head subtree
    0, 2, 0, 5, 0, 7, 0, 8,
    # Left arm:  shoulder → elbow → wrist → fingers → backtrack
    11, 13, 15, 17, 15, 19, 15, 21, 15, 13, 11,
    # Right arm: shoulder → elbow → wrist → fingers → backtrack
    12, 14, 16, 18, 16, 20, 16, 22, 16, 14, 12,
    # Left leg:  hip → knee → ankle → heel/foot → backtrack
    23, 25, 27, 29, 27, 31, 27, 25, 23,
    # Right leg: hip → knee → ankle → heel/foot → backtrack
    24, 26, 28, 30, 28, 32, 28, 26, 24,
    # Return to root
    0,
]
assert len(DFS_ORDER) == NUM_KEYPOINTS, "DFS_ORDER must have exactly 49 entries"

# --- Skeleton connections for drawing overlays ---
CONNECTIONS = [
    (0, 2), (0, 5), (0, 7), (0, 8),
    (11, 12), (11, 13), (13, 15),
    (15, 17), (15, 19), (15, 21),
    (12, 14), (14, 16),
    (16, 18), (16, 20), (16, 22),
    (11, 23), (12, 24), (23, 24),
    (23, 25), (25, 27), (27, 29), (27, 31),
    (24, 26), (26, 28), (28, 30), (28, 32),
]
