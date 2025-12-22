# Product Requirements Document (PRD)
## Logistic Regression Binary Classifier

---

## 📋 Document Information

**Product Name:** Binary Classification Logistic Regression Model  
**Version:** 1.0  
**Date:** November 2025  
**Author:** Anna  
**Status:** Complete  

---

## 1. Executive Summary

### 1.1 Product Overview
A machine learning system that classifies individuals into two groups (healthy/sick) using logistic regression with gradient ascent optimization.

### 1.2 Purpose
Educational implementation of logistic regression demonstrating:
- Binary classification
- Gradient ascent optimization
- Log-likelihood maximization
- Sigmoid activation function

### 1.3 Target Users
- Students learning machine learning
- Educators teaching classification algorithms
- Developers understanding ML fundamentals

---

## 2. Product Goals & Objectives

### 2.1 Primary Goals
1. **Accuracy**: Achieve >95% classification accuracy
2. **Interpretability**: Provide clear visualizations of model behavior
3. **Educational Value**: Demonstrate ML concepts with simple examples
4. **Reproducibility**: Generate consistent results with fixed random seed

### 2.2 Success Metrics
- **Accuracy**: 97.5% ✓ (Target: >95%)
- **Log-Likelihood**: -26.32 ✓ (converged)
- **Training Time**: <10 seconds ✓
- **Code Quality**: All files <200 lines ✓

---

## 3. Functional Requirements

### 3.1 Data Generation
**FR-1.1:** Generate synthetic dataset
- 400 samples (200 per class)
- 2 features (X1, X2) normalized to [0,1]
- Fully separable classes
- 1 bias term (X0 = 1)

**FR-1.2:** Data characteristics
- Random seed: 42 (reproducibility)
- Group 0 centered at (0.3, 0.3)
- Group 1 centered at (0.7, 0.7)
- Standard deviation: 0.15 per feature

### 3.2 Model Training
**FR-2.1:** Algorithm
- Method: Gradient Ascent
- Objective: Maximize Log-Likelihood
- Activation: Sigmoid function

**FR-2.2:** Hyperparameters
- Learning rate: 0.1
- Iterations: 1000
- Batch: Full dataset (batch gradient ascent)

**FR-2.3:** Outputs per iteration
- Log-Likelihood value
- Mean Squared Error
- Beta parameters
- Console progress (every 100 iterations)

### 3.3 Predictions
**FR-3.1:** Probability calculation
- Use sigmoid function: σ(z) = 1 / (1 + e^(-z))
- Output range: [0, 1]

**FR-3.2:** Binary classification
- Threshold: 0.5
- If P(sick) ≥ 0.5 → Class 1 (sick)
- If P(sick) < 0.5 → Class 0 (healthy)

### 3.4 Visualizations
**FR-4.1:** Training Progress Graph
- Top: Log-Likelihood over iterations
- Bottom: Mean Squared Error over iterations
- Annotations for max/min values

**FR-4.2:** Beta Evolution Graph
- 3 lines (β0, β1, β2)
- Show convergence behavior

**FR-4.3:** Decision Boundary Graph
- Scatter plot of data points
- Color by true class
- Probability heatmap background
- Decision boundary line (P=0.5)

**FR-4.4:** Predictions Comparison Graph
- Left: True labels vs predictions scatter
- Right: Histogram by class

### 3.5 Data Export
**FR-5.1:** Results Table (CSV/Excel)
- Columns: X0, X1, X2, True Label, Prediction, Binary Prediction, Error
- 400 rows (one per sample)
- UTF-8 encoding with BOM

**FR-5.2:** Visualizations
- Format: PNG
- Resolution: 300 DPI
- Size: 12x10 to 16x6 inches

---

## 4. Non-Functional Requirements

### 4.1 Performance
**NFR-1.1:** Training time <10 seconds
**NFR-1.2:** Memory usage <500 MB
**NFR-1.3:** File generation <5 seconds

### 4.2 Code Quality
**NFR-2.1:** Each Python file ≤200 lines
**NFR-2.2:** All functions documented with docstrings
**NFR-2.3:** Type hints for function parameters
**NFR-2.4:** Consistent naming conventions

### 4.3 Usability
**NFR-3.1:** Single command execution: `python main.py`
**NFR-3.2:** Clear console output with progress indicators
**NFR-3.3:** All outputs saved to `/mnt/user-data/outputs/`
**NFR-3.4:** English language for all code/comments/outputs

### 4.4 Maintainability
**NFR-4.1:** Modular architecture (3 files)
**NFR-4.2:** Separation of concerns:
  - Model logic (logistic_regression.py)
  - Visualization (visualizations.py)
  - Orchestration (main.py)

### 4.5 Compatibility
**NFR-5.1:** Python 3.7+
**NFR-5.2:** Dependencies: numpy, pandas, matplotlib, seaborn, openpyxl
**NFR-5.3:** Works in WSL/Linux environment
**NFR-5.4:** Compatible with global virtual environment

---

## 5. Technical Specifications

### 5.1 Mathematical Formulation

#### Model Equation:
```
z = β0·X0 + β1·X1 + β2·X2
P(y=1|X) = σ(z) = 1 / (1 + e^(-z))
```

#### Log-Likelihood:
```
ℓ(β) = Σ [yi·zi - log(1 + e^(zi))]
where zi = X·β
```

#### Gradient:
```
∇ℓ(β) = X^T · (y - σ(Xβ))
```

#### Update Rule:
```
β_new = β_old + α·∇ℓ(β)
where α = learning rate
```

### 5.2 Class Structure

#### LogisticRegression Class
**Attributes:**
- `learning_rate`: float
- `n_iterations`: int
- `beta`: np.ndarray
- `likelihood_history`: list
- `error_history`: list
- `beta_history`: list

**Methods:**
- `sigmoid(z)`: Activation function
- `log_likelihood(X, y, beta)`: Calculate objective
- `gradient(X, y, beta)`: Calculate gradient
- `mean_squared_error(y_true, y_pred)`: Calculate MSE
- `fit(X, y, verbose)`: Train model
- `predict_proba(X)`: Get probabilities
- `predict(X, threshold)`: Get binary predictions

### 5.3 File Outputs

| File | Type | Size | Description |
|------|------|------|-------------|
| results_table.csv | CSV | ~37 KB | All predictions |
| results_table.xlsx | Excel | ~32 KB | All predictions |
| decision_boundary.png | PNG | ~975 KB | Visualization |
| predictions_comparison.png | PNG | ~436 KB | Visualization |
| training_progress.png | PNG | ~270 KB | Visualization |
| beta_evolution.png | PNG | ~184 KB | Visualization |

---

## 6. User Stories

### US-1: Run Complete Analysis
**As a** student  
**I want to** run a single command  
**So that** I can generate all results and visualizations

**Acceptance Criteria:**
- Execute `python main.py`
- See progress in console
- Get 6 output files
- Complete in <15 seconds

### US-2: Understand Model Behavior
**As a** learner  
**I want to** see how the model trains  
**So that** I can understand gradient ascent

**Acceptance Criteria:**
- Training progress graph shows convergence
- Beta evolution shows parameter adjustment
- Console shows intermediate results

### US-3: Evaluate Model Performance
**As an** educator  
**I want to** see model accuracy and mistakes  
**So that** I can explain classification performance

**Acceptance Criteria:**
- Accuracy reported in console
- Decision boundary shows correct/incorrect predictions
- Results table lists all 400 predictions
- Mistakes are identifiable

### US-4: Analyze Individual Predictions
**As a** data analyst  
**I want to** examine each person's prediction  
**So that** I can understand model confidence

**Acceptance Criteria:**
- Excel file with all features
- Probabilities and binary predictions
- Absolute error for each sample
- Sortable/filterable in Excel

---

## 7. System Architecture

### 7.1 Component Diagram
```
┌─────────────────────────────────────────┐
│            main.py                      │
│  (Orchestration & User Interface)       │
└────────────┬───────────────┬────────────┘
             │               │
             ▼               ▼
┌─────────────────────┐  ┌──────────────────────┐
│ logistic_regression │  │   visualizations.py  │
│      .py            │  │  (Plotting Functions)│
│  (Model Logic)      │  └──────────────────────┘
└─────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│          Output Files                   │
│  CSV, Excel, PNG files                  │
└─────────────────────────────────────────┘
```

### 7.2 Data Flow
```
1. Generate synthetic data
   ↓
2. Initialize model (random β)
   ↓
3. For each iteration:
   - Calculate predictions
   - Calculate log-likelihood & MSE
   - Calculate gradient
   - Update β
   - Store history
   ↓
4. Generate visualizations
   ↓
5. Export results table
   ↓
6. Display summary
```

---

## 8. Constraints & Assumptions

### 8.1 Constraints
- Python 3.7+ required
- Must run in environment with numpy/pandas/matplotlib
- Output directory must be writable
- Single-threaded execution

### 8.2 Assumptions
- Data is linearly separable (or nearly so)
- Features are normalized to [0,1]
- Binary classification only
- Fixed random seed for reproducibility
- Full dataset fits in memory

---

## 9. Testing & Validation

### 9.1 Functional Tests
- ✓ Data generation creates 400 samples
- ✓ Model trains without errors
- ✓ All 6 output files are created
- ✓ Accuracy is calculated correctly
- ✓ Visualizations render properly

### 9.2 Performance Tests
- ✓ Training completes in <10 seconds
- ✓ Memory usage stays under 500 MB
- ✓ All files generate successfully

### 9.3 Quality Tests
- ✓ All Python files <200 lines
- ✓ No syntax errors
- ✓ Functions have docstrings
- ✓ Consistent code style

---

## 10. Future Enhancements

### 10.1 Potential Improvements
- [ ] Multi-class classification (>2 classes)
- [ ] Regularization (L1/L2)
- [ ] Cross-validation
- [ ] Feature engineering
- [ ] Additional metrics (precision, recall, F1)
- [ ] ROC curve visualization
- [ ] Confusion matrix
- [ ] Comparison with sklearn

### 10.2 Not in Scope
- Real-world datasets
- Data preprocessing pipeline
- Model deployment
- Web interface
- API endpoints
- Database integration

---

## 11. Acceptance Criteria

### 11.1 Must Have (Completed ✓)
- [x] Logistic regression implementation
- [x] Gradient ascent optimization
- [x] 4 visualizations
- [x] Results table (CSV + Excel)
- [x] 97.5% accuracy achieved
- [x] All code in English
- [x] Files <200 lines each

### 11.2 Should Have (Completed ✓)
- [x] Clear console output
- [x] Progress indicators
- [x] Summary statistics
- [x] Comprehensive README

### 11.3 Could Have (Not Implemented)
- [ ] Command-line arguments
- [ ] Configurable hyperparameters
- [ ] Additional metrics
- [ ] Interactive plots

---

## 12. Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Poor convergence | Low | High | Use appropriate learning rate (0.1) |
| Memory issues | Low | Medium | Use efficient numpy operations |
| File write errors | Medium | Low | Check directory permissions |
| Dependency conflicts | Medium | Medium | Document exact versions |

---

## 13. Glossary

**Binary Classification:** Categorizing items into one of two groups  
**Logistic Regression:** Statistical model for binary classification  
**Gradient Ascent:** Optimization algorithm to maximize objective  
**Log-Likelihood:** Measure of model fit to data  
**Sigmoid:** S-shaped activation function outputting 0-1  
**Beta (β):** Model parameters/weights  
**Epoch/Iteration:** One complete pass through the training process  
**Convergence:** When model parameters stabilize  

---

## 14. Appendix

### 14.1 Mathematical Derivations
See README.md for detailed explanations

### 14.2 Example Outputs
See generated PNG files and Excel table

### 14.3 Code Structure
- 3 Python files
- Total: 472 lines of code
- Modular and maintainable

---

**Document Version:** 1.0  
**Last Updated:** November 2025  
**Status:** ✓ Complete & Delivered