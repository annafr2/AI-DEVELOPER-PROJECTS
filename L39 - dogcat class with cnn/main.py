"""
main.py
=========================================================
  Dogs vs Cats Classifier — PyTorch Implementation
  Course: AI DEV EXPERT — Homework Assignment

  Entry point: runs the full pipeline:
    1. Load data
    2. Train CNN model
    3. Train FC model
    4. Create visualizations
    5. Print final results
    6. Save model weights

  Run with:
      python main.py

  Files in this project:
    config.py         — settings, transforms, device
    models.py         — CNNModel, FCModel definitions
    training.py       — load_datasets, train_model
    visualizations.py — all plotting functions
    main.py           — this file (entry point)
=========================================================
"""

import os
import torch

from config import OUT_DIR, device
from models import CNNModel, FCModel
from training import load_datasets, train_model
from visualizations import make_visualizations


def main():
    print("""
╔══════════════════════════════════════════════╗
║   Dogs vs Cats Classifier — AI DEV EXPERT   ║
║            CNN vs Fully Connected            ║
╚══════════════════════════════════════════════╝
""")

    # 1. Load data
    train_loader, test_loader = load_datasets()

    # 2. Create models
    model_cnn = CNNModel()
    model_fc  = FCModel()

    print(f"  CNN  parameters: {sum(p.numel() for p in model_cnn.parameters()):>10,}")
    print(f"  FC   parameters: {sum(p.numel() for p in model_fc.parameters()):>10,}")

    # 3. Train CNN
    cnn_history = train_model(model_cnn, "CNN", train_loader, test_loader, device)

    # 4. Train FC
    fc_history  = train_model(model_fc,  "Fully Connected", train_loader, test_loader, device)

    # 5. Create visualizations
    print("\n📊 Creating visualizations...")
    make_visualizations(cnn_history, fc_history,
                        train_loader, model_cnn, model_fc, device)

    # 6. Final summary
    print("""
╔══════════════════════════════════════════════╗
║                FINAL RESULTS                ║
╠══════════════════════════════════════════════╣""")
    print(f"║  CNN  best test accuracy:  "
          f"{max(cnn_history['test_acc'])*100:>6.2f}%           ║")
    print(f"║  FC   best test accuracy:  "
          f"{max(fc_history['test_acc'])*100:>6.2f}%           ║")
    print(f"║  CNN  total time: {cnn_history['total_time']:>6.1f}s                   ║")
    print(f"║  FC   total time:  {fc_history['total_time']:>6.1f}s                   ║")
    print("╚══════════════════════════════════════════════╝")

    # 7. Save models
    torch.save(model_cnn.state_dict(), os.path.join(OUT_DIR, "model_cnn.pth"))
    torch.save(model_fc.state_dict(),  os.path.join(OUT_DIR, "model_fc.pth"))
    print("\n💾 Models saved!")


if __name__ == "__main__":
    main()
