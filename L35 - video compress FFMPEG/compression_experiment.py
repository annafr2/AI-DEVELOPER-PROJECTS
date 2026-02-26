"""
Compression Experiment - Add rectangle overlay, compress, then rotate/move.
Shows how compression artifacts behave when you transform compressed video.
"""
import subprocess
import os
import sys

FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"
OUTPUT_DIR = "output"


def run_ffmpeg(cmd, label=""):
    """Run ffmpeg command."""
    print(f"  {label}..." if label else f"  Running ffmpeg...")
    result = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr[-300:]}")
    return result.returncode == 0


def get_file_size(path):
    """Get file size in KB."""
    return os.path.getsize(path) / 1024 if os.path.exists(path) else 0


def step1_add_rectangle(video_path):
    """Add a bright red rectangle overlay to the video."""
    out = os.path.join(OUTPUT_DIR, "with_rectangle.mp4")
    cmd = [FFMPEG, "-i", video_path, "-vf",
           "drawbox=x=200:y=150:w=200:h=150:color=red:t=fill,"
           "drawtext=text='RECTANGLE':x=230:y=210:fontsize=24:fontcolor=white",
           "-c:v", "libx264", "-crf", "23", "-c:a", "copy", out, "-y"]
    run_ffmpeg(cmd, "Adding red rectangle")
    return out


def step2_compress_levels(rect_video):
    """Compress the rectangle video at different quality levels."""
    results = []
    for crf in [1, 18, 28, 40, 51]:
        out = os.path.join(OUTPUT_DIR, f"compressed_crf{crf}.mp4")
        cmd = [FFMPEG, "-i", rect_video, "-c:v", "libx264",
               "-crf", str(crf), "-c:a", "copy", out, "-y"]
        run_ffmpeg(cmd, f"CRF={crf}")
        size = get_file_size(out)
        results.append({"crf": crf, "size_kb": size, "path": out})
        print(f"    -> Size: {size:.1f} KB")
    return results


def step3_rotate_compressed(compressed_path):
    """Rotate the compressed video to show artifact propagation."""
    out = os.path.join(OUTPUT_DIR, "rotated_compressed.mp4")
    cmd = [FFMPEG, "-i", compressed_path, "-vf",
           "rotate=0.1:fillcolor=black",
           "-c:v", "libx264", "-crf", "23", out, "-y"]
    run_ffmpeg(cmd, "Rotating compressed video")
    return out


def step4_shift_compressed(compressed_path):
    """Shift/move the compressed video to show artifacts."""
    out = os.path.join(OUTPUT_DIR, "shifted_compressed.mp4")
    # Crop and pad to simulate shift
    cmd = [FFMPEG, "-i", compressed_path, "-vf",
           "crop=600:440:20:20,pad=640:480:20:20:black",
           "-c:v", "libx264", "-crf", "23", out, "-y"]
    run_ffmpeg(cmd, "Shifting compressed video")
    return out


def step5_double_compress(compressed_path):
    """Re-compress already compressed video (generation loss)."""
    out = os.path.join(OUTPUT_DIR, "double_compressed.mp4")
    cmd = [FFMPEG, "-i", compressed_path, "-c:v", "libx264",
           "-crf", "35", out, "-y"]
    run_ffmpeg(cmd, "Re-compressing (generation loss)")
    return out


def step6_extract_comparison_frames(paths_dict):
    """Extract a frame from each version for visual comparison."""
    frames_dir = os.path.join(OUTPUT_DIR, "comparison_frames")
    os.makedirs(frames_dir, exist_ok=True)
    for name, path in paths_dict.items():
        if os.path.exists(path):
            out = os.path.join(frames_dir, f"{name}.png")
            cmd = [FFMPEG, "-i", path, "-vf", "select=eq(n\\,60)",
                   "-frames:v", "1", "-update", "1", out, "-y"]
            run_ffmpeg(cmd, f"Frame from {name}")


def main(video_path):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("=" * 55)
    print("COMPRESSION EXPERIMENT")
    print("=" * 55)

    print("\n[1/6] Adding rectangle overlay...")
    rect = step1_add_rectangle(video_path)

    print("\n[2/6] Compressing at different CRF levels...")
    comp_results = step2_compress_levels(rect)

    # Use CRF=40 (heavily compressed) for transform experiments
    heavy = os.path.join(OUTPUT_DIR, "compressed_crf40.mp4")

    print("\n[3/6] Rotating compressed video...")
    rotated = step3_rotate_compressed(heavy)

    print("\n[4/6] Shifting compressed video...")
    shifted = step4_shift_compressed(heavy)

    print("\n[5/6] Double-compressing video...")
    double = step5_double_compress(heavy)

    print("\n[6/6] Extracting comparison frames...")
    step6_extract_comparison_frames({
        "original": video_path,
        "with_rectangle": rect,
        "crf1_best": os.path.join(OUTPUT_DIR, "compressed_crf1.mp4"),
        "crf28_medium": os.path.join(OUTPUT_DIR, "compressed_crf28.mp4"),
        "crf51_worst": os.path.join(OUTPUT_DIR, "compressed_crf51.mp4"),
        "rotated": rotated,
        "shifted": shifted,
        "double_compressed": double,
    })

    # Print summary
    print("\n" + "=" * 55)
    print("COMPRESSION RESULTS SUMMARY")
    print("-" * 55)
    print(f"{'CRF':>5} {'Size (KB)':>12} {'Quality':>15}")
    print("-" * 55)
    for r in comp_results:
        q = {1: "Near lossless", 18: "High", 28: "Medium", 40: "Low", 51: "Worst"}
        print(f"{r['crf']:>5} {r['size_kb']:>12.1f} {q.get(r['crf'], ''):>15}")
    print("=" * 55)
    print("Check output/comparison_frames/ for visual comparison!")


if __name__ == "__main__":
    video = sys.argv[1] if len(sys.argv) > 1 else "sample_video.mp4"
    main(video)
