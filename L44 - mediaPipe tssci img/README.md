# L44 — MediaPipe TSSCI Image Generator

## What is this project?

Imagine you are doing an exercise and someone records a video of you.
This project uses your video to create a very special tiny picture called a **TSSCI image**.

Think of it like this:
- The video is made of many still photos (called frames).
- In each frame, a computer "draws" a skeleton on you — it finds your shoulders, elbows, knees, etc.
- Then it takes all those skeletons (49 of them) and packs them into a single **49x49 pixel** colorful image.
- The colors are not random — **Red = where your joint is (left/right), Green = where it is (up/down), Blue = how sure the computer is it found the joint**.
- Time goes from top to bottom. Each row = one moment in time. Each column = one body joint.

This is the TSSCI method from a scientific paper (see reference below).

---

## What does this project do?

1. **Extracts your skeleton** from the video using MediaPipe (Google's pose tool).
2. **Saves a skeleton overlay GIF** — your video with a glowing skeleton on top.
3. **Builds a TSSCI image** — the tiny 49x49 colorful picture that represents your whole movement.
4. **Creates an animated flyer GIF** — a beautiful animation showing the skeleton and the TSSCI image being built frame by frame, plus a graph of your shoulder movement.

---

## Outputs

| File | Description |
|------|-------------|
| [outputs/skeleton_overlay.gif](outputs/skeleton_overlay.gif) | Video with MediaPipe skeleton drawn on you |
| [outputs/tssci_image.png](outputs/tssci_image.png) | TSSCI image (49x49 px — the original size) |
| [outputs/tssci_upscaled.png](outputs/tssci_upscaled.png) | TSSCI image zoomed 8x (392x392 px, easy to see) |
| [outputs/tssci_plot.png](outputs/tssci_plot.png) | Labeled figure with axis descriptions |
| [outputs/animated_flyer.gif](outputs/animated_flyer.gif) | Animated flyer: skeleton + TSSCI building + graph |

---

## Input Video

Source video: `כלי 2026 פלוס/0224.mp4`

The video is automatically copied to `input_video.mp4` in the project folder to avoid path issues.

---

## How does TSSCI work?

1. MediaPipe finds **33 body landmarks** in each frame (nose, shoulders, elbows, wrists, hips, knees, ankles, etc.).
2. The landmarks are re-ordered using a **tree traversal** (depth-first search, DFS) of the body skeleton graph. This expands 33 landmarks to **49** because we revisit parent joints on the way back up the tree.
3. We sample **49 frames** evenly from the video.
4. We normalize all X and Y coordinates to [0, 1] across the entire clip.
5. We stack everything into a **49 rows x 49 cols x 3 channels** array and save it as a PNG.

---

## How to run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python main.py
```

---

## Project structure

```
L44 - mediaPipe tssci img/
├── config.py          # paths, DFS order, constants
├── skeleton.py        # MediaPipe extraction + overlay GIF
├── tssci.py           # TSSCI image builder
├── animate.py         # animated flyer GIF
├── main.py            # main pipeline
├── requirements.txt
├── README.md
├── PRD.md
├── TASKS.md
└── outputs/
    ├── skeleton_overlay.gif
    ├── tssci_image.png
    ├── tssci_upscaled.png
    ├── tssci_plot.png
    └── animated_flyer.gif
```

---

## Paper Reference

Segal, Y.; Hadar, O.; Lhotska, L.
**"Using EfficientNet-B7 (CNN), VAE and Siamese Twins Networks to Evaluate Human Exercises as Super Objects in TSSCI Images."**
*Journal of Personalized Medicine* 2023, 13, 874.
DOI: https://doi.org/10.3390/jpm13060874

Paper PDF: `jpm-13-00874-v2.pdf`
Paper code: https://github.com/yoramse/TSSCI.git
