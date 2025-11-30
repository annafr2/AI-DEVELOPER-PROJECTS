# Product Requirements Document (PRD)

## Project: Iris Flower Classification with Naive Bayes

### Overview
Implement a Naive Bayes classifier for the famous Iris flower dataset. Compare implementations using NumPy (from scratch) and scikit-learn library.

### Dataset
- **Name**: Iris Dataset
- **Source**: UCI Machine Learning Repository
- **Download**: https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data
- **Features**: 4 features (sepal length, sepal width, petal length, petal width)
- **Classes**: 3 classes (Setosa, Versicolor, Virginica)
- **Samples**: 150 total samples

### Requirements

#### 1. Data Processing
- Download Iris dataset from UCI repository
- Split data: 75% training, 25% testing
- No feature scaling required (Naive Bayes works with raw features)

#### 2. Model Training
- Train Naive Bayes classifier using probability distributions
- Calculate histograms for each feature per class
- Estimate probability distributions (Gaussian assumption)

#### 3. Classification
Implement two versions:
- **Version 1**: NumPy implementation (from scratch)
- **Version 2**: scikit-learn implementation

#### 4. Evaluation
- Compare predictions from both implementations
- Calculate accuracy for each
- Analyze differences and explain reasons

#### 5. Visualization
- Feature distributions per class (histograms)
- Confusion matrices for both implementations
- Comparison charts

### Technical Constraints
- Maximum 200 lines per Python file
- Use global virtual environment
- Clear, simple visualizations
- Child-friendly explanations in README

### Deliverables
1. `main.py` - Main classification script
2. `TASKS.md` - Task breakdown
3. `PRD.md` - This document
4. `README.md` - Usage guide with examples and outputs
5. `requirements.txt` - Dependencies

### Success Criteria
- Both implementations produce results
- Clear comparison and analysis
- Visual outputs saved and documented
- Simple explanations for understanding differences