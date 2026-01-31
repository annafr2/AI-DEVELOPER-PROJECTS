"""
Macroblock & Motion Vector Visualizer.
Uses ffmpeg codecview filter to draw macroblocks and motion vectors on frames.
"""
import subprocess
import os
import sys

FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"
OUTPUT_DIR = "output"


def run_ffmpeg(cmd):
    """Run ffmpeg command and print progress."""
    print(f"Running: {' '.join(cmd[:6])}...")
    result = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if result.returncode != 0:
        print(f"STDERR: {result.stderr[-500:]}")
    return result.returncode == 0


def extract_motion_vectors_video(video_path):
    """Create a video with motion vectors drawn on each frame."""
    out = os.path.join(OUTPUT_DIR, "motion_vectors.mp4")
    cmd = [FFMPEG, "-flags2", "+export_mvs", "-i", video_path,
           "-vf", "codecview=mv=pf+bf+bb",
           "-c:v", "libx264", "-crf", "18", "-an", out, "-y"]
    ok = run_ffmpeg(cmd)
    if ok:
        print(f"Saved: {out}")
    return ok


def extract_macroblock_types_video(video_path):
    """Create video showing macroblock types with color overlay."""
    out = os.path.join(OUTPUT_DIR, "macroblock_types.mp4")
    # codecview with mv_type shows block partitions
    cmd = [FFMPEG, "-flags2", "+export_mvs", "-i", video_path,
           "-vf", "codecview=mv=pf+bf+bb:mv_type=fp+bp",
           "-c:v", "libx264", "-crf", "18", "-an", out, "-y"]
    ok = run_ffmpeg(cmd)
    if ok:
        print(f"Saved: {out}")
    return ok


def extract_motion_vector_frames(video_path, num_frames=5):
    """Extract individual frames with motion vectors for comparison."""
    frames_dir = os.path.join(OUTPUT_DIR, "mv_frames")
    os.makedirs(frames_dir, exist_ok=True)

    # Get total frame count first
    for i in range(num_frames):
        # Extract specific frames spread across the video
        time_offset = i * 2  # every 2 seconds
        out = os.path.join(frames_dir, f"mv_frame_{i:03d}.png")
        cmd = [FFMPEG, "-flags2", "+export_mvs", "-i", video_path,
               "-vf", f"codecview=mv=pf+bf+bb,select=gte(t\\,{time_offset})",
               "-frames:v", "1", "-update", "1", out, "-y"]
        run_ffmpeg(cmd)
    print(f"Saved {num_frames} frames to {frames_dir}/")


def extract_qp_visualization(video_path):
    """Create video showing quantization parameter (QP) values."""
    out = os.path.join(OUTPUT_DIR, "qp_overlay.mp4")
    cmd = [FFMPEG, "-flags2", "+export_mvs", "-i", video_path,
           "-vf", "codecview=mv=pf+bf+bb:qp=true",
           "-c:v", "libx264", "-crf", "18", "-an", out, "-y"]
    ok = run_ffmpeg(cmd)
    if ok:
        print(f"Saved: {out}")
    return ok


def create_side_by_side(video_path):
    """Create side-by-side: original vs motion vectors."""
    out = os.path.join(OUTPUT_DIR, "side_by_side_mv.mp4")
    cmd = [FFMPEG, "-flags2", "+export_mvs", "-i", video_path, "-i", video_path,
           "-filter_complex",
           "[0:v]codecview=mv=pf+bf+bb[mv];"
           "[1:v][mv]hstack=inputs=2[out]",
           "-map", "[out]", "-c:v", "libx264", "-crf", "18", out, "-y"]
    ok = run_ffmpeg(cmd)
    if ok:
        print(f"Saved: {out}")
    return ok


def main(video_path):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("=" * 50)
    print("MACROBLOCK & MOTION VECTOR VISUALIZATION")
    print("=" * 50)

    print("\n[1/4] Creating motion vectors video...")
    extract_motion_vectors_video(video_path)

    print("\n[2/4] Creating macroblock types video...")
    extract_macroblock_types_video(video_path)

    print("\n[3/4] Extracting individual MV frames...")
    extract_motion_vector_frames(video_path)

    print("\n[4/4] Creating side-by-side comparison...")
    create_side_by_side(video_path)

    print("\n" + "=" * 50)
    print("DONE! Check the 'output' folder.")
    print("=" * 50)


if __name__ == "__main__":
    video = sys.argv[1] if len(sys.argv) > 1 else "sample_video.mp4"
    main(video)
