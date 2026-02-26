# Product Requirements Document (PRD)
## Temperature Conversion Neural Network

---

## 1. Project Overview

**Project Name:** Temperature Conversion Neural Network  
**Course:** AI Developer Expert  
**Platform:** Google Colab (with GPU support)  
**Framework:** TensorFlow/Keras  
**Language:** Python 3.x  

### 1.1 Objective
Build a neural network that learns to convert temperatures from Celsius to Fahrenheit **without being explicitly programmed with the formula** (f = 1.8 × c + 32). The model should discover this relationship through training on example data.

### 1.2 Educational Goals
- Demonstrate supervised learning with regression
- Show how neural networks can learn mathematical relationships
- Visualize the learning process
- Analyze learned weights and parameters
- Compare model predictions with the true formula

---

## 2. Technical Requirements

### 2.1 Environment Setup
- **Platform:** Google Colab notebook (Jupyter notebook environment)
- **GPU:** Enabled in Colab settings
- **Python Version:** 3.7+
- **Required Libraries:**
  - TensorFlow 2.x
  - NumPy
  - Matplotlib

### 2.2 Data Specifications

**Training Dataset:**
```python
Celsius:    [-40, -10,  0,  8, 15, 22, 38]
Fahrenheit: [-40,  14, 32, 46.4, 59, 71.6, 100]
```
- 7 temperature pairs
- dtype: float
- Covers range from freezing to hot temperatures

**Test Dataset:**
- Values NOT in training data
- Examples: 100°C, 50°C, -20°C, 25°C

### 2.3 Model Architecture

**Network Structure:**
```
Input Layer  → Dense Layer (4 units) → l0
              ↓
Hidden Layer → Dense Layer (4 units) → l1
              ↓
Output Layer → Dense Layer (1 unit)  → l2
```

**Architecture Details:**
- **Layer 0 (l0):** 
  - Units: 4
  - Input shape: [1] (single Celsius value)
  - Activation: Default (linear)
  
- **Layer 1 (l1):**
  - Units: 4
  - Activation: Default (linear)
  
- **Layer 2 (l2):**
  - Units: 1 (output Fahrenheit value)
  - Activation: Default (linear)

### 2.4 Training Configuration

**Compilation Parameters:**
- **Loss Function:** Mean Squared Error (MSE)
  - Measures: `(prediction - actual)²`
  - Suitable for regression problems
  
- **Optimizer:** Adam
  - Learning rate: 0.1
  - Adaptive learning rate algorithm
  - Efficient and fast convergence

**Training Parameters:**
- **Epochs:** 500
  - Full pass through training data
  - Model learns and corrects 500 times
  
- **Batch Size:** 7
  - Uses all training samples in each update
  - Full batch gradient descent

### 2.5 Code Constraints
- Maximum 150 lines of code
- Well-commented and structured
- Clear section separations
- Professional coding standards

---

## 3. Functional Requirements

### 3.1 Core Functionality

1. **Data Preparation**
   - Load and format training data
   - Display input/output pairs
   - Verify data types and shapes

2. **Model Building**
   - Define three-layer architecture
   - Create Sequential model
   - Display model summary

3. **Model Compilation**
   - Set loss function (MSE)
   - Configure optimizer (Adam with lr=0.1)
   - Prepare for training

4. **Training Process**
   - Train for 500 epochs
   - Track loss history
   - Silent training (verbose=False) for clean output

5. **Predictions**
   - Test on unseen data
   - Compare with true formula
   - Calculate prediction errors

6. **Weight Extraction**
   - Extract all layer weights
   - Extract all layer biases
   - Display learned parameters

### 3.2 Visualization Requirements

**Required Visualizations:**

1. **Loss Curve Graph**
   - X-axis: Epoch number (0-500)
   - Y-axis: Loss magnitude
   - Title: "Learning Curve: Loss Over Training"
   - Shows how error decreases over time
   - Saved as: `loss_curve.png`

2. **Prediction Comparison Graph**
   - X-axis: Celsius temperature
   - Y-axis: Fahrenheit temperature
   - Lines:
     - Model predictions (red solid line)
     - True formula (blue dashed line)
     - Training data points (green dots)
     - Test predictions (orange X markers)
   - Saved as: `prediction_comparison.png`

### 3.3 Output Requirements

**Console Output Must Include:**
1. TensorFlow version
2. Training data display
3. Model architecture summary
4. Compilation details
5. Training completion message
6. Final loss value
7. Test predictions table
8. Learned weights for all layers
9. Analysis of whether formula was discovered

**File Outputs:**
1. `loss_curve.png` - High resolution (300 DPI)
2. `prediction_comparison.png` - High resolution (300 DPI)

---

## 4. Analysis Requirements

### 4.1 Formula Discovery Analysis

**Question to Answer:**
"Did the model discover the formula f = 1.8 × c + 32?"

**Analysis Points:**
1. The model approximates the formula through learned weights
2. With 3 layers, it's more complex than a simple linear equation
3. The network represents a composition of transformations
4. While functionally equivalent, it's not explicitly using the formula
5. This demonstrates implicit vs. explicit learning

### 4.2 Weight Interpretation

**Display for Each Layer:**
- Weight matrix shape
- Weight values
- Bias values

**Layer 0 Example:**
```
Weights shape: (1, 4)
Weights: [value1, value2, value3, value4]
Biases: [bias1, bias2, bias3, bias4]
```

---

## 5. Success Criteria

### 5.1 Model Performance
- ✓ Final loss < 10
- ✓ Predictions within ±5°F of true formula
- ✓ Successful training completion (500 epochs)
- ✓ Decreasing loss curve

### 5.2 Prediction Accuracy
- ✓ 100°C → ~212°F (within acceptable error)
- ✓ Consistent predictions across test range
- ✓ Model generalizes to unseen data

### 5.3 Visualization Quality
- ✓ Clear, readable graphs
- ✓ Proper labels and titles
- ✓ High resolution images
- ✓ Professional appearance

### 5.4 Code Quality
- ✓ Under 150 lines
- ✓ Well-commented
- ✓ Structured sections
- ✓ Error-free execution
- ✓ Reproducible results

---

## 6. Understanding Jupyter Notebooks

### 6.1 What is Jupyter Notebook?

**Definition:**
Jupyter Notebook is an interactive computing environment that allows you to:
- Write and execute code in cells
- Mix code with documentation (markdown)
- Display outputs (text, graphs, tables) inline
- Create a narrative workflow

### 6.2 Google Colab = Jupyter Notebook

**Google Colab is:**
- A cloud-based Jupyter notebook environment
- Provided free by Google
- Includes free GPU access
- No installation required
- Saves notebooks to Google Drive

### 6.3 How to Use This Code in Colab

**Steps:**
1. Open Google Colab: https://colab.research.google.com
2. Create new notebook
3. Copy code into cells
4. Enable GPU: Runtime → Change runtime type → GPU
5. Run cells sequentially
6. View outputs inline
7. Download generated images from `/content` folder

---

## 7. Deliverables

1. **temp_conversion_nn.py** - Main Python script
2. **PRD.md** - This document
3. **README.md** - User guide with image links
4. **loss_curve.png** - Generated visualization
5. **prediction_comparison.png** - Generated visualization

---

**Document Version:** 1.0  
**Last Updated:** January 2026  
**Status:** Final
