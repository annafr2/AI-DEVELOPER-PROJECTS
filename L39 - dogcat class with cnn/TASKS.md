# TASKS — Dogs vs Cats Classifier
**Course: AI DEV EXPERT | Assignment: L39**

---

## Task Breakdown

### Task 1 — Set Up the Project
- [x] Install Python libraries: `torch`, `torchvision`, `matplotlib`, `numpy`
- [x] Create output folder for visualization images
- [x] Set random seed = 42 (for reproducible results)

### Task 2 — Prepare the Dataset
- [x] Load Oxford-IIIT Pet Dataset using `torchvision.datasets.OxfordIIITPet`
- [x] Select binary labels: `target_types="binary_category"` (0=cat, 1=dog)
- [x] Use only 3,000 images (not the full dataset)
- [x] Split: 80% training (2,400 images), 20% testing (600 images)
- [x] Resize every image to 64×64 pixels
- [x] Normalize with ImageNet mean/std values
- [x] Add data augmentation: random flip, brightness/contrast jitter

### Task 3 — Build the CNN Model
- [x] 3 convolutional blocks (Conv → BatchNorm → ReLU → MaxPool)
- [x] Block 1: 32 filters, 3×3 kernel → output [batch, 32, 32, 32]
- [x] Block 2: 64 filters, 3×3 kernel → output [batch, 64, 16, 16]
- [x] Block 3: 128 filters, 3×3 kernel → output [batch, 128, 8, 8]
- [x] Flatten layer → [batch, 8192]
- [x] Fully Connected: 8192 → 512 → 128 → 2
- [x] Dropout layers (0.1, 0.2, 0.3, 0.5) to prevent overfitting
- [x] BatchNorm after each conv for stable training
- [x] Output: 2 logits (cat, dog)

### Task 4 — Build the FC (Fully Connected) Model
- [x] Flatten input: [batch, 3, 64, 64] → [batch, 12,288]
- [x] FC layer 1: 12,288 → 512 neurons (ReLU + BatchNorm + Dropout)
- [x] FC layer 2: 512 → 256 neurons (ReLU + BatchNorm + Dropout)
- [x] FC layer 3: 256 → 128 neurons (ReLU + Dropout)
- [x] Output: 128 → 2 logits (cat, dog)
- [x] Note: NO convolutions — just flat connections

### Task 5 — Write the Training Loop
- [x] Use CrossEntropyLoss (standard for classification)
- [x] Use Adam optimizer (learning rate = 0.001, weight decay = 0.0001)
- [x] Use CosineAnnealingLR scheduler (learning rate decreases over time)
- [x] Print loss and accuracy after each epoch
- [x] Track: train loss, train accuracy, test loss, test accuracy, time per epoch

### Task 6 — Train Both Models
- [x] Train CNN for 15 epochs
- [x] Train FC for 15 epochs
- [x] Record all metrics
- [x] Save trained model weights (.pth files)

### Task 7 — Create Visualizations
- [x] `01_training_curves.png` — Loss and accuracy per epoch (both models)
- [x] `02_timing.png` — Time per epoch + total training time comparison
- [x] `03_accuracy_comparison.png` — Final accuracy bar chart
- [x] `04_sample_predictions.png` — 16 sample predictions (correct=green, wrong=red)
- [x] `05_architecture.png` — Architecture diagram (CNN vs FC side by side)
- [x] `06_tensor_flow.png` — How data tensor flows through CNN layer by layer
- [x] `07_filter_visualization.png` — What CNN filters detect in cat/dog images

### Task 8 — Write Documentation
- [x] `PRD.md` — What we're building and why
- [x] `TASKS.md` — This file (task tracking)
- [x] `README.md` — Full documentation with images + simple explanations

---

## Status Summary

| Task | Status     | Notes                          |
|------|------------|--------------------------------|
| 1    | Done       | Environment ready              |
| 2    | Done       | Dataset auto-downloads         |
| 3    | Done       | CNN model written and tested   |
| 4    | Done       | FC model written and tested    |
| 5    | Done       | Training loop working          |
| 6    | Done       | Both models trained            |
| 7    | Done       | 7 visualizations created       |
| 8    | Done       | All 3 docs written             |

**All tasks complete!**

---

## How to Run

```bash
# Step 1: Install requirements
pip install torch torchvision matplotlib numpy

# Step 2: Train (downloads dataset automatically)
python dogcat_pytorch.py

# Step 3: Generate visualizations only (demo mode)
python run_demo.py
```

---

## Notes for Next Steps

- Try a bigger image size (128×128) for better accuracy
- Try more epochs (30+) to see if accuracy keeps improving
- Try transfer learning (use pretrained ResNet) to get 95%+ accuracy
- Try data augmentation (rotation, zoom) to improve generalization

---

*Task tracking for AI DEV EXPERT — L39 homework*
