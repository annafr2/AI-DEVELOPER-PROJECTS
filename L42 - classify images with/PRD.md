# PRD — Bridge Card HCP Classifier
## Product Requirements Document

| Field | Value |
|-------|-------|
| **Project** | Bridge Card HCP Image Classifier |
| **Course** | AI Developer Expert — Lesson 42 (Image Classification) |
| **Author** | Anna F. |
| **Date** | February 2026 |
| **Status** | Homework Submission |
| **Model** | ResNet-50 (Transfer Learning) |

---

## 1. Overview

### 1.1 Problem Statement

Bridge is a card game where players evaluate the strength of their hand using **High Card Points (HCP)**: Ace=4, King=3, Queen=2, Jack=1.
Automatically classifying card images by HCP value is a clean, measurable computer-vision task that demonstrates transfer learning on a real-world labelled dataset.

### 1.2 Research Question

> **"Can ResNet-50 accurately classify bridge playing cards by High Card Points (HCP) from card images?"**

**Success criterion:** Test-set accuracy ≥ 80% on the 5-class HCP classification task.

### 1.3 Hypothesis

ResNet-50 pre-trained on ImageNet will be able to learn the mapping from card rank (visible in the image) to HCP value, because:
- Card faces have distinct, structured visual features (suit symbols, rank indices)
- Transfer learning reduces the need for large datasets
- 5 well-separated HCP classes should be easier than 52 original classes

---

## 2. Dataset

### 2.1 Source

| Property | Value |
|----------|-------|
| Name | Cards Image Dataset — Classification |
| Platform | Kaggle |
| Dataset ID | `gpiosenka/cards-image-datasetclassification` |
| License | CC0 — Public Domain |
| Original classes | 53 (52 standard cards + joker) |
| Download method | `kagglehub.dataset_download(...)` |

### 2.2 Dataset Splits

| Split | Images (approx.) | Purpose |
|-------|-------------------|---------|
| train | ~3,640 | Model training + augmentation |
| valid | ~265   | Hyperparameter tuning, early stopping |
| test  | ~265   | Final evaluation (held out) |

### 2.3 Label Re-mapping (52 → 5 HCP Classes)

The original 53 folder names are mapped to 5 HCP classes by detecting the rank keyword in the folder name:

| HCP Class | Label | Card Ranks |
|-----------|-------|------------|
| 0 | 0 pts  (2–10) | Two, Three, Four, Five, Six, Seven, Eight, Nine, Ten, Joker |
| 1 | J = 1 pt      | Jack of any suit |
| 2 | Q = 2 pts     | Queen of any suit |
| 3 | K = 3 pts     | King of any suit |
| 4 | A = 4 pts     | Ace of any suit |

> Note: Class 0 (~40 of 53 original classes) will be over-represented.
> The model must learn to distinguish the 4 high-card ranks from the large "zero-point" majority.

### 2.4 Data Augmentation (applied to train split only)

| Augmentation | Value | Reason |
|-------------|-------|--------|
| Rotation | ±15° | Cards may be slightly tilted |
| Width / height shift | 10% | Cards not always perfectly centred |
| Horizontal flip | True | Left–right mirror is a valid card view |
| Zoom | 10% | Variable distance from camera |
| Brightness | 85–115% | Lighting variation |

---

## 3. Model Architecture

### 3.1 Backbone

**ResNet-50** (He et al., 2016) pre-trained on **ImageNet-1K**.
- Input: 224 × 224 × 3 (RGB, normalized 0–1)
- Output of backbone: 7 × 7 × 2048 feature map
- Weights: `imagenet` (downloaded automatically by Keras)

### 3.2 Custom Classification Head

```
GlobalAveragePooling2D  →  (2048,)
Dense(512, relu)
Dropout(0.40)
Dense(256, relu)
Dropout(0.30)
Dense(5, softmax)        →  HCP class probabilities
```

### 3.3 Training Strategy

| Phase | Backbone | Epochs | LR | Optimizer |
|-------|----------|--------|----|-----------|
| 1 — Head training | Frozen (all layers) | 20 (+ early stop) | 1e-4 | Adam |
| 2 — Fine-tuning   | Top 30 layers unfrozen | 10 (+ early stop) | 1e-5 | Adam |

**Callbacks (both phases):**
- `EarlyStopping` — patience 5, monitors `val_accuracy`, restores best weights
- `ModelCheckpoint` — saves best model to `outputs/resnet50_hcp_model.keras`
- `ReduceLROnPlateau` — factor 0.5, patience 3

### 3.4 Loss & Metrics

| Property | Value |
|----------|-------|
| Loss | Categorical cross-entropy |
| Metric | Accuracy |
| Final report | Per-class precision, recall, F1 (scikit-learn) |

---

## 4. Outputs

### 4.1 Files Produced

| File | Description |
|------|-------------|
| `outputs/resnet50_hcp_model.keras` | Trained model (best checkpoint) |
| `outputs/training_history.png` | Accuracy & loss curves for both phases |
| `outputs/confusion_matrix.png` | 5×5 prediction heatmap |
| `outputs/sample_predictions.png` | 10 random test images with true/predicted labels |

### 4.2 Visualization Specifications

**Training History**
- 2-panel figure (Accuracy | Loss)
- Train = blue line, Validation = orange line
- Dashed vertical line marks Phase 1 → Phase 2 transition
- Grid, legend, no top/right spines (clean style)

**Confusion Matrix**
- 5×5 seaborn heatmap, Blues colormap
- Annotations: integer counts per cell
- Axis labels: HCP class names

**Sample Predictions**
- 2 × 5 grid, 10 random test images
- Green border = correct, Red border = wrong
- Title shows both true and predicted label

---

## 5. Code Architecture

Each Python module has a single responsibility and stays under **150 lines**.

| File | Lines | Responsibility |
|------|-------|----------------|
| `config.py` | ~50 | Constants: paths, HCP mapping, hyper-parameters, colours |
| `dataset.py` | ~90 | Download, load images, remap labels, build generators |
| `model.py` | ~80 | Build ResNet-50, fine-tune helper, callbacks, summary |
| `train.py` | ~75 | Phase-1 training, Phase-2 training, evaluation, verdict |
| `visualize.py` | ~95 | Three plots + classification report |
| `main.py` | ~60 | Orchestrates all steps, single entry point |

---

## 6. Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| tensorflow | ≥ 2.13 | Model building and training |
| kagglehub | ≥ 0.2 | Automated dataset download |
| numpy | ≥ 1.24 | Array operations |
| matplotlib | ≥ 3.7 | Plotting |
| seaborn | ≥ 0.12 | Confusion matrix heatmap |
| scikit-learn | ≥ 1.3 | Metrics: confusion matrix, classification report |
| Pillow | ≥ 10.0 | Image I/O |

Install: `pip install -r requirements.txt`

---

## 7. Acceptance Criteria

| Criterion | Pass Condition |
|-----------|----------------|
| Training completes | No crashes on standard Python + TF environment |
| Test accuracy | ≥ 80% on the 5-class HCP test split |
| All plots saved | `outputs/` contains 3 `.png` files after training |
| Model saved | `outputs/resnet50_hcp_model.keras` exists and is loadable |
| Research answer printed | Console shows clear verdict for research question |
| Code quality | Each `.py` file ≤ 150 lines, English comments throughout |

---

## 8. Limitations & Future Work

| Limitation | Notes |
|------------|-------|
| Class imbalance | Class 0 (2–10) has ~40× more original classes than each high-card class. Could use class weights or oversampling. |
| Single card images | The dataset shows single cards, not full hands. Real HCP calculation needs 13 cards. |
| Dataset size | ~3,600 training images is small. Fine-tuning on more data could improve results further. |
| Joker class | The joker (0 HCP) is included and may confuse the model with unusual artwork. |

**Possible extensions:**
- Composite hand images (combine 13 cards into one image, predict total HCP bin)
- Try EfficientNet or MobileNet as alternative backbones
- Deploy as a mobile app using TensorFlow Lite

---

*Document version 1.0 — AI Developer Expert Course, February 2026*
