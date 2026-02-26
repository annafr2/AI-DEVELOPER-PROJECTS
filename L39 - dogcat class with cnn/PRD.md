# PRD — Dogs vs Cats Classifier
**Product Requirements Document**
Course: AI DEV EXPERT | Assignment: L39

---

## What Are We Building?

A program that looks at a photo and says: **"Is this a cat or a dog?"**

We build TWO different versions and compare them:
1. **CNN** — a smart network that looks at patterns in the image
2. **FC** — a simpler network that just reads all the pixels

---

## The Problem

Given any photo of a pet, automatically decide:
- Output **0** = Cat
- Output **1** = Dog

---

## What the Program Must Do

**Must do:**
- Load 3,000 pet images (cats and dogs)
- Resize every image to 64×64 pixels
- Train a CNN model for 15 rounds (epochs)
- Train a Fully Connected model for 15 rounds
- Show training loss and accuracy after every round
- Compare the two models at the end
- Save 7 visualization images
- Run on CPU (no GPU needed)

**Nice to have:**
- Show sample predictions with correct/wrong labels
- Show how data flows through the CNN (tensor shapes)
- Show what CNN filters actually detect

---

## Technical Choices

| What          | Choice                    | Why                              |
|---------------|---------------------------|----------------------------------|
| Language      | Python 3.10               | Most popular for AI              |
| Framework     | PyTorch                   | Industry standard for deep learning |
| Dataset       | Oxford-IIIT Pet (auto-download) | Free, well-known, has cat/dog labels |
| Image size    | 64×64 pixels              | Small enough to train fast on CPU |
| Batch size    | 32 images at a time       | Balance between speed and memory |
| Epochs        | 15                        | Enough to see learning happen    |
| Loss function | CrossEntropyLoss          | Standard for classification      |
| Optimizer     | Adam                      | Fast and reliable                |

---

## Success Criteria

| Metric          | CNN Target | FC Target  |
|-----------------|------------|------------|
| Test accuracy   | ≥ 80%      | ≥ 65%      |
| Training time   | < 10 min   | < 15 min   |
| Code runs cleanly | Yes      | Yes        |
| Visualizations saved | Yes   | Yes        |

---

## Files to Deliver

```
dogcat_pytorch.py    ← main PyTorch code (CNN + FC models)
run_demo.py          ← demo runner (generates visualizations)
README.md            ← full documentation with images
PRD.md               ← this file
TASKS.md             ← task breakdown and status
output_images/
  01_training_curves.png
  02_timing.png
  03_accuracy_comparison.png
  04_sample_predictions.png
  05_architecture.png
  06_tensor_flow.png
  07_filter_visualization.png
```

---

## Timeline

| Step | What                        | Time   |
|------|-----------------------------|--------|
| 1    | Set up PyTorch environment  | 10 min |
| 2    | Write CNN + FC models       | 30 min |
| 3    | Write training loop         | 20 min |
| 4    | Train on 3,000 images       | ~5 min |
| 5    | Create visualizations       | 20 min |
| 6    | Write documentation         | 15 min |

---

*Written for AI DEV EXPERT course — simple, clear, to the point.*
