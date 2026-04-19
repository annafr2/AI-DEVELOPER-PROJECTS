import torch
import argparse
import time
import os
from config import OUTPUTS_DIR, EXP_SHORT_LEN


def print_banner():
    print("\n" + "=" * 60)
    print("  How Much Does an RNN Remember?")
    print("  A Memory Experiment on Language Modeling")
    print("  3 Experiments | Parameter Sweep | Text Generation")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="RNN Memory Experiments")
    parser.add_argument("--no-sweep", action="store_true",
                        help="Skip parameter sweep (saves ~30-40 min)")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"],
                        help="Compute device")
    args = parser.parse_args()

    if args.device == "auto":
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(args.device)

    print_banner()
    print(f"\n  Device  : {device}")
    print(f"  Outputs : {OUTPUTS_DIR}")

    from experiments import run_all_experiments, run_generation, run_final_test, run_sweep

    start = time.time()

    # Experiments 1 (short) + 2 (long)
    results, models, word_maps = run_all_experiments(device)

    # Experiment 3: text generation (uses the short-sequence model)
    short_model = models["short"]
    w2i, i2w = word_maps["short"]
    run_generation(short_model, w2i, i2w, device)

    # Final test: the 20% held-out set we never touched
    run_final_test(short_model, EXP_SHORT_LEN, device)

    # Optional: 27-model parameter sweep
    if not args.no_sweep:
        run_sweep(device)
    else:
        print("\n  [Skipping parameter sweep — remove --no-sweep to enable]")

    elapsed = time.time() - start
    print(f"\n{'=' * 60}")
    print(f"  Done in {elapsed / 60:.1f} minutes")
    pngs = [f for f in os.listdir(OUTPUTS_DIR) if f.endswith(".png")]
    print(f"  {len(pngs)} visualizations saved to outputs/:")
    for f in sorted(pngs):
        print(f"    - {f}")
    print("=" * 60)


if __name__ == "__main__":
    main()
