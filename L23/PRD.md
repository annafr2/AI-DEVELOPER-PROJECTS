# Product Requirements Document (PRD)
## SVM Classification on Iris Dataset

### Project Overview
Implementation of Support Vector Machine (SVM) classification on the Iris flower dataset using two different approaches: scikit-learn library and QP (Quadratic Programming) solver.

### Problem Statement
The Iris dataset contains 3 flower species (Setosa, Versicolor, Virginica). Since SVM is inherently a binary classifier, we need a hierarchical approach:
1. **Level 1**: Classify Setosa vs (Versicolor + Virginica)
2. **Level 2**: If not Setosa, classify Versicolor vs Virginica

### Technical Requirements

#### Functional Requirements
| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Load and preprocess Iris dataset | High |
| FR2 | Implement SVM using scikit-learn | High |
| FR3 | Implement SVM using QP solver (cvxopt) | High |
| FR4 | Create hierarchical binary classification | High |
| FR5 | Generate visualization graphs | High |
| FR6 | Compare accuracy of both methods | Medium |

#### Non-Functional Requirements
| ID | Requirement | Priority |
|----|-------------|----------|
| NFR1 | Code should not exceed 150 lines per file | High |
| NFR2 | Code should be well-documented | Medium |
| NFR3 | Graphs should be clear and labeled | High |

### Implementation Approach

#### Method 1: Scikit-learn
- Use `sklearn.svm.SVC` with linear kernel
- Built-in optimization
- Easy to use API

#### Method 2: QP Solver (cvxopt)
- Solve the dual SVM optimization problem manually
- Use `cvxopt.solvers.qp` for quadratic programming
- Educational purpose: understand SVM internals

### Deliverables
1. `svm_sklearn.py` - Scikit-learn implementation
2. `svm_qp.py` - QP solver implementation  
3. `utils.py` - Shared utilities and data loading
4. `main.py` - Main execution script
5. `README.md` - Simple explanation for beginners
6. `PRD.md` - This document
7. `TASKS.md` - Task breakdown

### Success Criteria
- Both methods achieve >90% accuracy
- Visualizations clearly show decision boundaries
- Code is clean and under line limit