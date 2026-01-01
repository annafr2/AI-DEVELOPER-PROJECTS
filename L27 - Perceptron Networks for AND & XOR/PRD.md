# Product Requirements Document (PRD)
## Perceptron Network for Logic Gates with Noise Analysis

### 1. Project Overview
**Project Name:** Logic Gate Neural Network Trainer  
**Version:** 1.0  
**Date:** January 2026  
**Author:** AI Developer Expert Course Assignment

### 2. Objective
Build a neural network system that learns to solve AND and XOR logic problems using perceptrons, with the ability to add controlled noise to test network robustness.

### 3. Functional Requirements

#### 3.1 Core Features
- **FR-1:** Network must solve AND logic gate (linearly separable)
- **FR-2:** Network must solve XOR logic gate (non-linearly separable)
- **FR-3:** User can configure number of perceptrons (neurons) in hidden layer
- **FR-4:** Generate dataset with minimum 100 samples per feature
- **FR-5:** Use Mean Squared Error (MSE) as loss function
- **FR-6:** Implement training with backpropagation (learning algorithm)
- **FR-7:** Add controllable noise to dataset using percentage parameter
- **FR-8:** Visualize results graphically (decision boundaries, training progress)
- **FR-9:** Maximum 150 lines of code per script

#### 3.2 Technical Specifications
- **TS-1:** Framework: Pure NumPy implementation (no Keras/TensorFlow)
- **TS-2:** Activation Function: ReLU for hidden layers, Sigmoid for output
- **TS-3:** Optimizer: Gradient Descent with fixed learning rate (0.5)
- **TS-4:** Dataset Generation: Balanced samples across all input combinations
- **TS-5:** Noise Model: Gaussian noise with configurable percentage
- **TS-6:** Visualization: matplotlib for plots
- **TS-7:** Implementation: Custom forward/backward propagation from scratch

#### 3.3 Data Requirements
- **DR-1:** AND dataset: 100+ samples with inputs (0,0), (0,1), (1,0), (1,1)
- **DR-2:** XOR dataset: 100+ samples with inputs (0,0), (0,1), (1,0), (1,1)
- **DR-3:** Noise range: 0-50% of feature space
- **DR-4:** Output labels: Binary (0 or 1)

### 4. Non-Functional Requirements
- **NFR-1:** Code must be readable and well-commented
- **NFR-2:** Training time should not exceed 2 minutes per problem
- **NFR-3:** Accuracy on clean data should exceed 95%
- **NFR-4:** Documentation must be in simple English

### 5. User Interface Requirements
- **UI-1:** Command-line interface for parameter configuration
- **UI-2:** Visual plots showing:
  - Decision boundaries
  - Training loss curves
  - Data points with noise visualization
  - Network architecture diagram (optional)

### 6. Acceptance Criteria
- ✓ Network correctly learns AND logic (accuracy > 95%)
- ✓ Network correctly learns XOR logic (accuracy > 95%)
- ✓ Noise addition creates visible cloud around data points
- ✓ Visualization clearly shows decision boundaries
- ✓ Code stays under 150 lines
- ✓ Documentation explains network layers, activation functions, and results

### 7. Deliverables
1. `perceptron_numpy_only.py` - Main implementation (pure NumPy)
2. `README.md` - Comprehensive documentation
3. `PRD.md` - This document
4. Output visualizations (8 PNG files saved locally)
5. Installation guides for troubleshooting

### 8. Implementation Approach

#### Why NumPy Instead of Keras?

The final implementation uses pure NumPy rather than Keras/TensorFlow for several important reasons:

**Educational Value:**
- Students see every computation explicitly
- Understand forward and backward propagation mechanics
- Learn gradient descent implementation from scratch
- No "magic" hidden inside framework abstractions

**Practical Benefits:**
- Faster installation (2 packages vs 10+ packages)
- No compatibility issues with TensorFlow versions
- Easier to run on any system (Windows, Linux, Mac)
- Smaller codebase (easier to understand and debug)

**Technical Implementation:**
- Custom `SimpleNeuralNetwork` class
- Manual forward propagation (matrix multiplications)
- Manual backward propagation (gradient calculations)
- Fixed learning rate gradient descent (not Adam)
- All math operations visible and modifiable

**Learning Outcomes:**
Students understand that neural networks are fundamentally:
1. Matrix operations (numpy.dot)
2. Activation functions (simple math)
3. Error calculation (mean squared error)
4. Weight updates (gradient descent)

This foundation transfers to any deep learning framework (TensorFlow, PyTorch, JAX) because the underlying math is identical.

### 9. Future Enhancements
- Support for additional logic gates (NAND, NOR, XNOR)
- Real-time training visualization
- Hyperparameter tuning interface
- Export trained models (save/load weights)
- Comparative analysis: NumPy vs Keras implementation
- Mini-batch gradient descent
- Momentum and adaptive learning rates
- Different weight initialization strategies