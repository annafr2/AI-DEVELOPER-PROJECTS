"""
main.py - Entry point for Bridge Card HCP Classification with ResNet-50.
Course: AI Developer Expert | Lesson 42

Research Question:
  "Can ResNet-50 accurately classify bridge playing cards by HCP
   (High Card Points) from individual card images?"

How to run:
  python main.py

Outputs are saved to the outputs/ folder:
  - resnet50_hcp_model.keras
  - training_history.png
  - confusion_matrix.png
  - sample_predictions.png
"""

import os
import tensorflow as tf
from dataset   import download_dataset, get_data_generators
from train     import train_phase1, train_phase2, evaluate_model, answer_research_question
from visualize import (plot_training_history, plot_confusion_matrix,
                       plot_sample_predictions, print_report)
from config    import OUTPUT_DIR

os.makedirs(OUTPUT_DIR, exist_ok=True)


def main():
    print("\n" + "=" * 55)
    print("  BRIDGE CARD HCP CLASSIFIER")
    print("  Model  : ResNet-50 (Transfer Learning)")
    print("  Task   : Classify cards into 5 HCP point classes")
    print("=" * 55 + "\n")

    # ── GPU info ─────────────────────────────────────────────────────────────
    gpus = tf.config.list_physical_devices("GPU")
    print(f"TensorFlow version : {tf.__version__}")
    print(f"GPUs available     : {len(gpus)}\n")

    # ── Step 1: Download dataset from Kaggle ─────────────────────────────────
    dataset_root = download_dataset()

    # ── Step 2: Load & preprocess all three splits ───────────────────────────
    train_gen, val_data, test_data = get_data_generators(dataset_root)

    # ── Step 3: Phase 1 – train head with frozen backbone ────────────────────
    model, history1 = train_phase1(train_gen, val_data)

    # ── Step 4: Phase 2 – fine-tune top ResNet layers ────────────────────────
    history2 = train_phase2(model, train_gen, val_data)

    # ── Step 5: Evaluate on held-out test set ────────────────────────────────
    y_true, y_pred, accuracy = evaluate_model(model, test_data)

    # ── Step 6: Generate & save all visualizations ───────────────────────────
    print("Generating visualizations...")
    plot_training_history(history1, history2)
    plot_confusion_matrix(y_true, y_pred)
    plot_sample_predictions(model, test_data[0], y_true)
    print_report(y_true, y_pred)

    # ── Step 7: Answer the research question ─────────────────────────────────
    answer_research_question(accuracy)

    print("=" * 55)
    print("  All done!")
    print(f"  Model  -> {OUTPUT_DIR}/resnet50_hcp_model.keras")
    print(f"  Plots  -> {OUTPUT_DIR}/")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()
