"""
main.py — L44 MediaPipe TSSCI Image Generator
Pipeline:
  1. Copy video to local path (avoids Unicode path issues on Windows)
  2. Extract MediaPipe Pose skeletons  → skeleton_overlay.gif
  3. Build 49x49x3 TSSCI image        → tssci_image.png / tssci_upscaled.png
  4. Create animated flyer            → animated_flyer.gif
"""
import shutil
from pathlib import Path
from config import VIDEO_PATH, LOCAL_VIDEO, NUM_FRAMES
from skeleton import extract_skeletons, save_skeleton_gif
from tssci import sample_frames, build_tssci, save_tssci, plot_tssci
from animate import create_animated_flyer


def prepare_video() -> str:
    """Copy source video to local folder (removes Unicode path issues)."""
    local = Path(LOCAL_VIDEO)
    if not local.exists():
        print(f"Copying video → {local} ...")
        shutil.copy2(VIDEO_PATH, local)
    else:
        print(f"Using cached local video: {local}")
    return str(local)


def main() -> None:
    print("=" * 55)
    print("  L44 — MediaPipe TSSCI Image Generator")
    print("  Reference: Segal et al., JPM 2023, 13, 874")
    print("=" * 55)

    # Step 1 — Prepare video
    video_path = prepare_video()

    # Step 2 — Extract skeletons with MediaPipe
    print("\n[1/4] Extracting skeletons with MediaPipe Pose...")
    skeleton_data = extract_skeletons(video_path)

    # Step 3 — Save skeleton overlay GIF
    print("\n[2/4] Saving skeleton overlay GIF...")
    save_skeleton_gif(skeleton_data, video_path)

    # Step 4 — Build TSSCI image
    print("\n[3/4] Building TSSCI image (49x49x3)...")
    sampled = sample_frames(skeleton_data, n=NUM_FRAMES)
    print(f"      Sampled {len(sampled)} frames from {len(skeleton_data)} total.")
    tssci = build_tssci(sampled)
    save_tssci(tssci)
    plot_tssci(tssci)
    print(f"      TSSCI shape: {tssci.shape}  "
          f"min={tssci.min():.3f}  max={tssci.max():.3f}")

    # Step 5 — Animated flyer
    print("\n[4/4] Creating animated flyer GIF...")
    create_animated_flyer(skeleton_data, tssci)

    print("\n" + "=" * 55)
    print("  Done!  Outputs:")
    print("    outputs/skeleton_overlay.gif")
    print("    outputs/tssci_image.png        (49x49 px original)")
    print("    outputs/tssci_upscaled.png     (392x392 px display)")
    print("    outputs/tssci_plot.png         (labeled figure)")
    print("    outputs/animated_flyer.gif")
    print("=" * 55)


if __name__ == "__main__":
    main()
