"""
Run all analysis scripts in the correct order.
"""
import subprocess
import sys
import os

SCRIPTS = [
    ("video_analyzer.py", "Analyzing video structure..."),
    ("macroblock_visualizer.py", "Creating motion vector visualizations..."),
    ("compression_experiment.py", "Running compression experiments..."),
    ("visualization.py", "Creating charts and graphs..."),
]


def main():
    video = sys.argv[1] if len(sys.argv) > 1 else "sample_video.mp4"
    base_dir = os.path.dirname(os.path.abspath(__file__))

    print("=" * 60)
    print("VIDEO COMPRESSION ANALYSIS - RUNNING ALL SCRIPTS")
    print("=" * 60)

    for script, msg in SCRIPTS:
        print(f"\n{'=' * 60}")
        print(f">> {msg}")
        print(f"{'=' * 60}")
        path = os.path.join(base_dir, script)
        args = [sys.executable, path]
        if script != "visualization.py":
            args.append(video)
        result = subprocess.run(args, cwd=base_dir)
        if result.returncode != 0:
            print(f"WARNING: {script} exited with code {result.returncode}")

    print("\n" + "=" * 60)
    print("ALL DONE! Check the 'output' folder for results.")
    print("=" * 60)


if __name__ == "__main__":
    main()
