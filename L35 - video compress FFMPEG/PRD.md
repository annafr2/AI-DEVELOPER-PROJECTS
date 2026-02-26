# PRD - Video Compression Analysis Tool

## Goal
Build a set of Python tools that analyze and visualize how video compression works, using FFmpeg.

## Background
Video compression (H.264/AVC) uses clever tricks to make video files small:
- **I-frames**: Full pictures (like a photo)
- **P-frames**: Only store what changed from the previous frame
- **B-frames**: Store differences from both past AND future frames
- **GOP**: Group of Pictures - the pattern of I, P, and B frames
- **Macroblocks**: Video is split into small blocks (16x16 pixels)
- **Motion Vectors**: Arrows showing where each block "came from"

## Features

### 1. Video Analyzer (`video_analyzer.py`)
- Extract codec, resolution, FPS, bitrate, duration
- Count I/P/B frames and their sizes
- Analyze GOP structure (size, pattern)
- Save report as text file + JSON data

### 2. Macroblock Visualizer (`macroblock_visualizer.py`)
- Draw motion vectors (arrows) on video frames
- Show macroblock types with color overlay
- Create side-by-side comparison (original vs motion vectors)
- Extract individual frames with MV overlay

### 3. Compression Experiment (`compression_experiment.py`)
- Add a red rectangle to the video
- Compress at different CRF levels (1, 18, 28, 40, 51)
- Rotate and shift the compressed video
- Show generation loss (re-compressing)
- Extract comparison frames

### 4. Visualization (`visualization.py`)
- Pie chart: frame type distribution
- Bar chart: average frame sizes by type
- Bar chart: GOP sizes
- Timeline: frame types + sizes over time
- Bar chart: CRF level vs file size

## Tech Stack
- Python 3
- FFmpeg / FFprobe (installed at C:\ffmpeg)
- matplotlib (for charts)

## Success Criteria
- All scripts run without errors
- Output folder contains videos, frames, charts, and reports
- Visual outputs clearly show how compression works
