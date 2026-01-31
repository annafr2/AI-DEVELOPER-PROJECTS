# TASKS - Video Compression Analysis

## Completed Tasks

- [x] Create sample test video using ffmpeg testsrc
- [x] Write `video_analyzer.py` - extract video metadata and frame info
- [x] Write `macroblock_visualizer.py` - draw motion vectors and macroblocks
- [x] Write `compression_experiment.py` - rectangle + compress + rotate/shift
- [x] Write `visualization.py` - create charts and graphs
- [x] Write PRD.md
- [x] Write TASKS.md
- [x] Write README.md with results and explanations
- [x] Run all scripts and capture output
- [x] Add output images to README

## Script Execution Order

1. `python video_analyzer.py` - Must run first (creates frame_data.json)
2. `python macroblock_visualizer.py` - Creates MV videos and frames
3. `python compression_experiment.py` - Creates compressed versions
4. `python visualization.py` - Must run last (needs data from steps 1+3)
