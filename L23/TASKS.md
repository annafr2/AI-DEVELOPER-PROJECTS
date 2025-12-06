# Tasks Breakdown
## SVM Classification Project

### Phase 1: Setup & Data Preparation
- [x] Create project structure
- [x] Create PRD.md
- [x] Create TASKS.md
- [ ] Implement utils.py (data loading, preprocessing)

### Phase 2: Scikit-learn Implementation
- [ ] Implement SVM with sklearn
- [ ] Create hierarchical classifier (Level 1 + Level 2)
- [ ] Generate decision boundary plots
- [ ] Calculate and display accuracy

### Phase 3: QP Solver Implementation
- [ ] Implement dual SVM formulation
- [ ] Solve using cvxopt QP solver
- [ ] Extract support vectors and weights
- [ ] Generate decision boundary plots
- [ ] Calculate and display accuracy

### Phase 4: Visualization & Comparison
- [ ] Create comparison graphs
- [ ] Plot support vectors
- [ ] Generate accuracy comparison chart

### Phase 5: Documentation
- [ ] Write README.md with simple explanations
- [ ] Add graphs to README
- [ ] Final code review

---

## Detailed Task Descriptions

### Task 1: utils.py
**File**: `utils.py`
**Lines**: ~40
**Functions**:
- `load_iris_data()` - Load and return Iris dataset
- `prepare_binary_data(X, y, class1, class2)` - Prepare data for binary classification
- `plot_decision_boundary()` - Visualize decision boundary

### Task 2: svm_sklearn.py
**File**: `svm_sklearn.py`
**Lines**: ~50
**Functions**:
- `train_sklearn_svm()` - Train SVM using sklearn
- `hierarchical_predict()` - Two-level prediction
- `visualize_sklearn()` - Generate plots

### Task 3: svm_qp.py
**File**: `svm_qp.py`
**Lines**: ~60
**Functions**:
- `solve_svm_qp()` - Solve SVM using quadratic programming
- `predict_qp()` - Make predictions with QP solution
- `visualize_qp()` - Generate plots

### Task 4: main.py
**File**: `main.py`
**Lines**: ~40
**Functions**:
- `main()` - Run both methods and compare

---

## Progress Tracking

| Task | Status | Assigned | Notes |
|------|--------|----------|-------|
| Project Setup | ✅ Done | - | Structure created |
| utils.py | 🔄 In Progress | - | - |
| svm_sklearn.py | ⏳ Pending | - | - |
| svm_qp.py | ⏳ Pending | - | - |
| main.py | ⏳ Pending | - | - |
| README.md | ⏳ Pending | - | - |
| Testing | ⏳ Pending | - | - |