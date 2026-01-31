"""
Video Analyzer - Extract video info like VLC does.
Uses ffprobe/ffmpeg to get GOP structure, I-frames, resolution, codec info.
"""
import subprocess
import json
import sys
import os

FFPROBE = r"C:\ffmpeg\bin\ffprobe.exe"
FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"
OUTPUT_DIR = "output"


def run_cmd(cmd):
    """Run a command and return stdout."""
    result = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    return result.stdout, result.stderr


def get_basic_info(video_path):
    """Get basic video info (resolution, codec, fps, bitrate, duration)."""
    cmd = [FFPROBE, "-v", "quiet", "-print_format", "json",
           "-show_format", "-show_streams", video_path]
    stdout, _ = run_cmd(cmd)
    return json.loads(stdout)


def get_frame_types(video_path):
    """Get frame types (I, P, B) for every frame in the video."""
    cmd = [FFPROBE, "-v", "quiet", "-select_streams", "v:0",
           "-show_entries", "frame=pict_type,key_frame,pkt_size,coded_picture_number",
           "-print_format", "json", video_path]
    stdout, _ = run_cmd(cmd)
    data = json.loads(stdout)
    return data.get("frames", [])


def analyze_gop(frames):
    """Analyze GOP (Group of Pictures) structure."""
    gop_sizes = []
    current_gop = 0
    for f in frames:
        if f.get("key_frame") == 1:
            if current_gop > 0:
                gop_sizes.append(current_gop)
            current_gop = 1
        else:
            current_gop += 1
    if current_gop > 0:
        gop_sizes.append(current_gop)
    return gop_sizes


def print_report(video_path):
    """Print a full video analysis report and save to file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    info = get_basic_info(video_path)
    frames = get_frame_types(video_path)

    # Find video stream
    vid = None
    for s in info.get("streams", []):
        if s.get("codec_type") == "video":
            vid = s
            break

    if not vid:
        print("ERROR: No video stream found!")
        return

    fmt = info.get("format", {})
    gop_sizes = analyze_gop(frames)

    # Count frame types
    type_counts = {"I": 0, "P": 0, "B": 0}
    frame_sizes = {"I": [], "P": [], "B": []}
    for f in frames:
        t = f.get("pict_type", "?")
        type_counts[t] = type_counts.get(t, 0) + 1
        size = int(f.get("pkt_size", 0))
        if t in frame_sizes:
            frame_sizes[t].append(size)

    # Build report
    lines = []
    lines.append("=" * 60)
    lines.append("VIDEO ANALYSIS REPORT")
    lines.append("=" * 60)
    lines.append(f"File: {os.path.basename(video_path)}")
    lines.append(f"Format: {fmt.get('format_long_name', 'N/A')}")
    lines.append(f"Duration: {float(fmt.get('duration', 0)):.2f} seconds")
    lines.append(f"Total Bitrate: {int(fmt.get('bit_rate', 0)) // 1000} kbps")
    lines.append(f"File Size: {int(fmt.get('size', 0)) / 1024:.1f} KB")
    lines.append("")
    lines.append("--- VIDEO STREAM ---")
    lines.append(f"Codec: {vid.get('codec_name')} ({vid.get('codec_long_name')})")
    lines.append(f"Resolution: {vid.get('width')}x{vid.get('height')}")
    lines.append(f"FPS: {vid.get('r_frame_rate')}")
    lines.append(f"Pixel Format: {vid.get('pix_fmt')}")
    lines.append(f"Profile: {vid.get('profile')}")
    lines.append(f"Level: {vid.get('level')}")
    lines.append("")
    lines.append("--- FRAME ANALYSIS ---")
    lines.append(f"Total Frames: {len(frames)}")
    for t in ["I", "P", "B"]:
        count = type_counts.get(t, 0)
        pct = (count / len(frames) * 100) if frames else 0
        avg_size = sum(frame_sizes[t]) / len(frame_sizes[t]) if frame_sizes[t] else 0
        lines.append(f"  {t}-frames: {count} ({pct:.1f}%) avg size: {avg_size:.0f} bytes")
    lines.append("")
    lines.append("--- GOP STRUCTURE ---")
    lines.append(f"Number of GOPs: {len(gop_sizes)}")
    if gop_sizes:
        lines.append(f"Average GOP size: {sum(gop_sizes)/len(gop_sizes):.1f} frames")
        lines.append(f"Min GOP: {min(gop_sizes)}, Max GOP: {max(gop_sizes)}")
        lines.append(f"First 10 GOP sizes: {gop_sizes[:10]}")
    lines.append("=" * 60)

    report = "\n".join(lines)
    print(report)

    # Save report + raw data
    with open(os.path.join(OUTPUT_DIR, "video_analysis.txt"), "w") as f:
        f.write(report)

    # Save frame data as JSON for visualization
    frame_data = {"frames": frames, "gop_sizes": gop_sizes,
                  "type_counts": type_counts, "frame_sizes": frame_sizes}
    with open(os.path.join(OUTPUT_DIR, "frame_data.json"), "w") as f:
        json.dump(frame_data, f, indent=2)

    print(f"\nSaved: {OUTPUT_DIR}/video_analysis.txt")
    print(f"Saved: {OUTPUT_DIR}/frame_data.json")


if __name__ == "__main__":
    video = sys.argv[1] if len(sys.argv) > 1 else "sample_video.mp4"
    print_report(video)
