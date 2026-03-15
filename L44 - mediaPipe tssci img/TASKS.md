# TASKS — L44: MediaPipe TSSCI Image Generator

## Status legend
- [x] Done
- [ ] To do

---

## Phase 1 — Setup

- [x] Create project folder: `L44 - mediaPipe tssci img/`
- [x] Create `outputs/` directory
- [x] Read and summarize paper: Segal et al., JPM 2023

---

## Phase 2 — Core Code

- [x] `config.py` — paths, DFS_ORDER (49 entries), CONNECTIONS, constants
- [x] `skeleton.py` — MediaPipe Pose extraction + skeleton overlay GIF
- [x] `tssci.py` — frame sampling, DFS reordering, normalization, TSSCI builder, save PNG
- [x] `animate.py` — 3-panel animated flyer (skeleton + TSSCI + graph)
- [x] `main.py` — orchestrates all steps, copies video to local path

---

## Phase 3 — Documentation

- [x] `requirements.txt`
- [x] `README.md` — simple English explanation + output links
- [x] `PRD.md` — product requirements, specs, success criteria
- [x] `TASKS.md` — this file

---

## Phase 4 — Run & Verify

- [ ] Run `pip install -r requirements.txt`
- [ ] Run `python main.py`
- [ ] Verify `outputs/skeleton_overlay.gif` — skeleton visible on video
- [ ] Verify `outputs/tssci_image.png` — 49x49 px RGB, non-empty
- [ ] Verify `outputs/tssci_upscaled.png` — 392x392 px visible pattern
- [ ] Verify `outputs/animated_flyer.gif` — 49 frames, 3 panels animated

---

## Notes

- Video source: `C:/Users/annaf/OneDrive/Desktop/תוכן/כלי 2026 פלוס/0224.mp4`
- Video is copied to `input_video.mp4` to avoid Windows Unicode path issues
- MediaPipe 33 landmarks → DFS traversal → 49 columns (backtracking through parent joints)
- TSSCI paper: https://doi.org/10.3390/jpm13060874
- TSSCI code reference: https://github.com/yoramse/TSSCI.git
