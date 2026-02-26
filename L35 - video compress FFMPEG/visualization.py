"""
Visualization - Create beautiful charts from video analysis data.
Reads frame_data.json and creates graphs showing frame types, GOP, sizes.
"""
import json
import os
import sys

OUTPUT_DIR = "output"

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("WARNING: matplotlib not found. Install with: pip install matplotlib")


def load_data():
    """Load frame analysis data."""
    path = os.path.join(OUTPUT_DIR, "frame_data.json")
    with open(path, "r") as f:
        return json.load(f)


def plot_frame_type_distribution(data):
    """Pie chart showing I/P/B frame distribution."""
    counts = data["type_counts"]
    labels = []
    sizes = []
    colors_map = {"I": "#e74c3c", "P": "#3498db", "B": "#2ecc71"}
    colors = []
    for t in ["I", "P", "B"]:
        if counts.get(t, 0) > 0:
            labels.append(f"{t}-frames ({counts[t]})")
            sizes.append(counts[t])
            colors.append(colors_map[t])

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%",
           startangle=90, textprops={"fontsize": 14})
    ax.set_title("Frame Type Distribution", fontsize=16, fontweight="bold")
    out = os.path.join(OUTPUT_DIR, "chart_frame_types.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


def plot_frame_sizes(data):
    """Bar chart showing average frame sizes by type."""
    frame_sizes = data["frame_sizes"]
    types = ["I", "P", "B"]
    avgs = []
    colors = ["#e74c3c", "#3498db", "#2ecc71"]
    for t in types:
        s = frame_sizes.get(t, [])
        avgs.append(sum(s) / len(s) if s else 0)

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(types, avgs, color=colors, width=0.5, edgecolor="black")
    for bar, val in zip(bars, avgs):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                f"{val:.0f}B", ha="center", fontsize=12, fontweight="bold")
    ax.set_xlabel("Frame Type", fontsize=13)
    ax.set_ylabel("Average Size (bytes)", fontsize=13)
    ax.set_title("Average Frame Size by Type", fontsize=16, fontweight="bold")
    ax.grid(axis="y", alpha=0.3)
    out = os.path.join(OUTPUT_DIR, "chart_frame_sizes.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


def plot_gop_structure(data):
    """Visualize GOP sizes as a bar chart."""
    gops = data["gop_sizes"]
    if not gops:
        return
    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(gops))
    ax.bar(x, gops, color="#9b59b6", edgecolor="black", alpha=0.8)
    avg = sum(gops) / len(gops)
    ax.axhline(y=avg, color="red", linestyle="--", label=f"Average: {avg:.1f}")
    ax.set_xlabel("GOP Number", fontsize=13)
    ax.set_ylabel("Frames in GOP", fontsize=13)
    ax.set_title("GOP (Group of Pictures) Sizes", fontsize=16, fontweight="bold")
    ax.legend(fontsize=12)
    ax.grid(axis="y", alpha=0.3)
    out = os.path.join(OUTPUT_DIR, "chart_gop_sizes.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


def plot_frame_timeline(data):
    """Show frame types over time as a color-coded timeline."""
    frames = data["frames"]
    if not frames:
        return
    colors_map = {"I": "#e74c3c", "P": "#3498db", "B": "#2ecc71"}
    frame_colors = [colors_map.get(f.get("pict_type", "?"), "gray") for f in frames]
    sizes = [int(f.get("pkt_size", 0)) for f in frames]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7), sharex=True)

    # Timeline bar
    for i, c in enumerate(frame_colors):
        ax1.axvspan(i, i + 1, color=c, alpha=0.8)
    patches = [mpatches.Patch(color=c, label=f"{t}-frame")
               for t, c in colors_map.items()]
    ax1.legend(handles=patches, loc="upper right", fontsize=11)
    ax1.set_ylabel("Frame Type", fontsize=12)
    ax1.set_title("Frame Type Timeline", fontsize=15, fontweight="bold")
    ax1.set_yticks([])

    # Size plot
    ax2.fill_between(range(len(sizes)), sizes, color="#3498db", alpha=0.4)
    ax2.plot(sizes, color="#2c3e50", linewidth=0.5)
    # Mark I-frames
    for i, f in enumerate(frames):
        if f.get("pict_type") == "I":
            ax2.axvline(x=i, color="red", alpha=0.5, linewidth=0.8)
    ax2.set_xlabel("Frame Number", fontsize=12)
    ax2.set_ylabel("Frame Size (bytes)", fontsize=12)
    ax2.set_title("Frame Sizes (red lines = I-frames)", fontsize=15, fontweight="bold")
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "chart_timeline.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


def plot_compression_comparison():
    """Show file sizes at different CRF levels."""
    crf_values = [1, 18, 28, 40, 51]
    sizes = []
    for crf in crf_values:
        path = os.path.join(OUTPUT_DIR, f"compressed_crf{crf}.mp4")
        sizes.append(os.path.getsize(path) / 1024 if os.path.exists(path) else 0)

    if not any(sizes):
        print("No compression files found. Run compression_experiment.py first.")
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["#27ae60", "#2ecc71", "#f39c12", "#e67e22", "#e74c3c"]
    bars = ax.bar([str(c) for c in crf_values], sizes, color=colors, edgecolor="black")
    for bar, val in zip(bars, sizes):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f"{val:.0f}KB", ha="center", fontsize=11, fontweight="bold")
    ax.set_xlabel("CRF Value (lower = better quality)", fontsize=13)
    ax.set_ylabel("File Size (KB)", fontsize=13)
    ax.set_title("File Size vs Compression Level (CRF)", fontsize=16, fontweight="bold")
    ax.grid(axis="y", alpha=0.3)
    out = os.path.join(OUTPUT_DIR, "chart_crf_comparison.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


def main():
    if not HAS_MPL:
        print("Cannot create charts without matplotlib. Install it first.")
        return
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("=" * 50)
    print("CREATING VISUALIZATIONS")
    print("=" * 50)

    data = load_data()
    plot_frame_type_distribution(data)
    plot_frame_sizes(data)
    plot_gop_structure(data)
    plot_frame_timeline(data)
    plot_compression_comparison()

    print("\n" + "=" * 50)
    print("ALL CHARTS SAVED! Check the 'output' folder.")
    print("=" * 50)


if __name__ == "__main__":
    main()
