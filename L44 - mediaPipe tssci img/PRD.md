# PRD — L44: MediaPipe TSSCI Image Generator

## 1. Overview

**Course:** AI Developer Expert
**Lesson:** L44
**Topic:** Human Pose Estimation + TSSCI Image Generation
**Technologies:** Python, MediaPipe, OpenCV, NumPy, Matplotlib, Pillow

---

## 2. Goal

Build a Python pipeline that:
1. Takes a short video of a person.
2. Extracts body skeleton landmarks using **MediaPipe Pose**.
3. Generates a **TSSCI image** (49x49x3 RGB) following the method from Segal et al. (2023).
4. Produces an **animated flyer GIF** showing the skeleton, TSSCI being built, and a joint movement graph.

---

## 3. Background

TSSCI (Tree Structure Skeleton Color Image) is a technique that converts a time-series of body pose frames into a single compact image. This image can then be fed into standard CNNs (e.g., EfficientNet-B7) for exercise classification or scoring.

Key idea: represent an entire movement as one "super object" image, the same way a CNN sees a photo of a cat.

---

## 4. Input

| Item | Details |
|------|---------|
| Video | `0224.mp4` (personal recording, ~few seconds) |
| Pose estimator | MediaPipe Pose (33 landmarks per frame) |
| Frames sampled | 49 (evenly spaced from full video) |

---

## 5. Outputs

| Output | Format | Description |
|--------|--------|-------------|
| `skeleton_overlay.gif` | GIF | MediaPipe skeleton drawn on original video |
| `tssci_image.png` | PNG | 49x49x3 TSSCI image (original size) |
| `tssci_upscaled.png` | PNG | TSSCI zoomed 8x (392x392 px) |
| `tssci_plot.png` | PNG | TSSCI with labeled axes (matplotlib figure) |
| `animated_flyer.gif` | GIF | 3-panel animation: skeleton + TSSCI + graph |

---

## 6. TSSCI Specification

| Parameter | Value |
|-----------|-------|
| Frames (rows) | 49 |
| Keypoints (cols) | 49 (DFS traversal of 33 MediaPipe landmarks) |
| Channels | 3 — R=X, G=Y, B=Confidence |
| Normalization | Global min-max across all frames for X and Y |
| Missing keypoints | Replaced by nearest left neighbour in DFS sequence |

---

## 7. Technical Constraints

- Each Python file: max 150 lines
- All code, comments, and prints: English
- Outputs saved to `outputs/` folder as PNG/GIF
- No GPU required (MediaPipe runs on CPU)
- Compatible with Windows 11

---

## 8. Non-Goals (out of scope for L44)

- Training a classifier on the TSSCI image (L45+)
- VAE generation of synthetic TSSCI images
- Siamese network exercise scoring
- Multi-person pose estimation

---

## 9. Success Criteria

- [ ] `main.py` runs end-to-end without errors
- [ ] `outputs/skeleton_overlay.gif` shows skeleton on video
- [ ] `outputs/tssci_image.png` is a valid 49x49 RGB image
- [ ] `outputs/animated_flyer.gif` plays smoothly with all 3 panels
- [ ] All Python files are 150 lines or fewer
