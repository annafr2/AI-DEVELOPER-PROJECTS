# Tasks Breakdown

## Homework 21: Naive Bayes Classification on Iris Dataset

### Task 1: Setup Environment
- [x] Create L21 folder
- [ ] Set up virtual environment (use global venv)
- [ ] Install required packages

### Task 2: Data Acquisition
- [ ] Download Iris dataset from UCI repository
- [ ] Load data into appropriate format
- [ ] Verify data integrity (150 samples, 4 features, 3 classes)

### Task 3: Data Preparation
- [ ] Split dataset: 75% training, 25% testing
- [ ] Separate features (X) and labels (y)
- [ ] Ensure random but reproducible split

### Task 4: Naive Bayes Implementation (NumPy)
- [ ] Calculate class priors (P(class))
- [ ] For each feature and class:
  - Calculate mean (μ)
  - Calculate standard deviation (σ)
- [ ] Implement Gaussian probability density function
- [ ] Implement prediction function using Bayes' theorem
- [ ] Make predictions on test set

### Task 5: Naive Bayes Implementation (scikit-learn)
- [ ] Import GaussianNB from sklearn
- [ ] Train model on training data
- [ ] Make predictions on test set

### Task 6: Visualization
- [ ] Create histograms showing feature distributions per class
- [ ] Generate confusion matrices for both implementations
- [ ] Create comparison charts

### Task 7: Analysis & Comparison
- [ ] Calculate accuracy for both implementations
- [ ] Compare predictions
- [ ] Identify differences
- [ ] Explain reasons for any discrepancies

### Task 8: Documentation
- [ ] Write clear README with:
  - Simple explanations
  - Usage examples
  - Output screenshots
  - Comparison results
- [ ] Ensure all outputs are saved and documented

## File Structure
```
L21/
├── main.py              # Main classification script
├── iris.data            # Downloaded dataset
├── outputs/             # Visualizations folder
│   ├── feature_distributions.png
│   ├── confusion_matrix_numpy.png
│   ├── confusion_matrix_sklearn.png
│   └── accuracy_comparison.png
├── requirements.txt     # Dependencies
├── TASKS.md            # This file
├── PRD.md              # Requirements
└── README.md           # Documentation
```