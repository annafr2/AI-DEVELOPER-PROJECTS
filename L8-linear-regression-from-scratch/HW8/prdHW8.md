# Product Requirements Document (PRD)
## Linear Regression Analysis with R² Simulation

---

## 1. Executive Summary

### Project Overview
A comprehensive linear regression analysis tool that simulates the relationship between error variance and R² performance using pure mathematical implementations. The project demonstrates how adding variables affects model performance and introduces adjusted R² as a correction mechanism.

### Key Objectives
- **Educational**: Demonstrate linear regression concepts without black-box libraries
- **Analytical**: Show the impact of noise and variable count on model performance  
- **Comparative**: Illustrate the difference between regular R² and adjusted R²

---

## 2. Project Scope & Goals

### Primary Goals
1. **Simulate realistic datasets** with controlled noise levels
2. **Implement linear regression** using pure linear algebra (NumPy only)
3. **Analyze R² performance** across different error variance levels
4. **Compare models** with different numbers of variables
5. **Calculate adjusted R²** to account for model complexity

### Success Metrics
- ✅ Generate 20 different noise levels from σ=0.1 to σ=10
- ✅ Create base model with 50 independent variables
- ✅ Extend model with 20 additional engineered features
- ✅ Produce 4+ visualizations showing key relationships
- ✅ Calculate both regular and adjusted R² metrics

---

## 3. Technical Requirements

### Core Functionality

#### 3.1 Data Generation
- **Sample Size**: 1,000 observations
- **Base Variables**: 50 independent variables (normal distribution)
- **Target Variable**: Linear combination of predictors + noise
- **Coefficient Vector**: Fixed beta values for reproducibility

#### 3.2 Feature Engineering
- **Polynomial Features**: X² terms for first 5 variables
- **Root Features**: √|X| terms for variables 6-10
- **Interaction Terms**: 10 pairwise interactions (Xi × Xj)
- **Total Extended**: 20 additional engineered features

#### 3.3 Regression Implementation
```
Mathematical Formula: β = (X^T × X)^(-1) × X^T × y
R² Formula: R² = 1 - SSE/SST
Adjusted R²: R²_adj = 1 - (1-R²) × (n-1)/(n-p-1)
```

#### 3.4 Variance Testing
- **Range**: 20 logarithmically spaced values from 0.1 to 10
- **Error Distribution**: Normal(0, σ) for each variance level
- **Reproducibility**: Fixed random seed for consistent results

---

## 4. User Stories & Use Cases

### Primary Users
1. **Data Science Students**: Learning regression fundamentals
2. **Educators**: Teaching statistical concepts with visual examples
3. **Researchers**: Understanding model complexity trade-offs
4. **Analysts**: Benchmarking custom vs library implementations

### Key Use Cases

#### UC1: Educational Demonstration
- **As a** data science instructor
- **I want to** show students how noise affects model performance
- **So that** they understand the relationship between data quality and accuracy

#### UC2: Model Comparison
- **As a** data analyst
- **I want to** compare models with different numbers of variables
- **So that** I can decide whether adding features improves performance

#### UC3: Overfitting Analysis
- **As a** machine learning practitioner
- **I want to** see the difference between R² and adjusted R²
- **So that** I can avoid overfitting in my models

---

## 5. Functional Requirements

### 5.1 Core Functions
| Function | Input | Output | Purpose |
|----------|--------|--------|---------|
| `create_simulated_data()` | n_samples, n_features | X matrix, y vector | Generate base dataset |
| `fit_linear_regression_manual()` | X, y | β coefficients, predictions | Pure linear algebra regression |
| `calculate_r_squared_manual()` | y_actual, y_pred | R² value | Performance metric |
| `create_extended_features()` | X_original | X_extended | Feature engineering |
| `calculate_adjusted_r_squared()` | R², n, p | R²_adj | Complexity-adjusted metric |

### 5.2 Visualization Requirements
1. **Primary Plot**: R² vs Error Variance (log scale)
2. **Comparison Plot**: 50 vs 70 variables performance
3. **Improvement Plot**: Delta R² from adding variables
4. **Adjustment Analysis**: Regular vs Adjusted R² comparison

---

## 6. Technical Architecture

### Dependencies
- **NumPy**: Matrix operations and random number generation
- **Matplotlib**: All visualizations and plots
- **Python**: 3.7+ (for @ matrix multiplication operator)

### Code Structure
```
linear_regression_analysis.py
├── Data Generation (Step 1)
│   ├── Base dataset creation
│   ├── Beta coefficient definition  
│   └── Target variable calculation
├── Feature Engineering (Step 2)
│   ├── Polynomial features
│   ├── Root transformations
│   └── Interaction terms
├── Model Training & Evaluation
│   ├── Manual regression fitting
│   ├── R² calculation
│   └── Adjusted R² calculation
└── Visualization & Analysis
    ├── Performance plots
    ├── Comparison charts
    └── Summary statistics
```

---

## 7. Performance & Quality Requirements

### Performance Specifications
- **Execution Time**: < 30 seconds for complete analysis
- **Memory Usage**: < 500MB for all data structures
- **Numerical Stability**: Handle condition numbers up to 10^12

### Quality Standards
- **Code Quality**: Clear variable names, comprehensive comments
- **Mathematical Accuracy**: Results match theoretical expectations
- **Reproducibility**: Fixed seeds ensure identical results across runs
- **Error Handling**: Graceful handling of singular matrices

---

## 8. Constraints & Limitations

### Technical Constraints
- **No ML Libraries**: Pure NumPy implementation only
- **Memory Limits**: Single machine, in-memory processing
- **Matrix Inversion**: Assumes non-singular X^T×X matrices

### Scope Limitations
- **Single Target**: Only continuous regression (no classification)
- **Linear Models**: No polynomial or non-linear relationships
- **Static Analysis**: No real-time or streaming data

---

## 9. Deliverables & Timeline

### Phase 1: Core Implementation (Week 1)
- ✅ Basic data generation
- ✅ Manual regression implementation  
- ✅ R² calculation and visualization

### Phase 2: Feature Extension (Week 1)
- ✅ Extended feature engineering
- ✅ Comparative analysis plots
- ✅ Performance improvement metrics

### Phase 3: Advanced Analysis (Week 1)
- ✅ Adjusted R² implementation
- ✅ Comprehensive visualization suite
- ✅ Final documentation and testing

---

## 10. Acceptance Criteria

### Must Have Features
- [x] Generate simulated dataset with 50 base variables
- [x] Implement linear regression using only linear algebra
- [x] Test 20 different error variance levels
- [x] Create extended dataset with 20 additional features
- [x] Calculate both regular and adjusted R²
- [x] Produce 4+ informative visualizations
- [x] All code comments and output in English

### Success Validation
- **Educational Value**: Clear demonstration of key concepts
- **Mathematical Correctness**: Results align with statistical theory
- **Visual Clarity**: Plots effectively communicate findings
- **Code Quality**: Clean, readable, well-documented implementation

---

## 11. Risk Assessment

### Technical Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|---------|------------|
| Matrix singularity | Low | High | Add regularization term |
| Numerical instability | Medium | Medium | Use double precision |
| Memory constraints | Low | Medium | Monitor array sizes |

### Project Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|---------|------------|
| Scope creep | Medium | Low | Stick to core requirements |
| Complexity underestimated | Low | Medium | Iterative development |

---

## 12. Future Enhancements

### Potential Extensions
1. **Cross-Validation**: K-fold validation for robustness testing
2. **Regularization**: Ridge/Lasso regression implementations
3. **Interactive Plots**: Bokeh/Plotly for dynamic visualizations
4. **Statistical Tests**: Significance testing for coefficients
5. **Real Data**: Extension to real-world datasets

### Scalability Considerations
- **Larger Datasets**: Chunked processing for big data
- **Parallel Processing**: Multi-core matrix operations
- **GPU Acceleration**: CuPy integration for large matrices

---

## Document Information
- **Version**: 1.0
- **Last Updated**: September 27, 2025
- **Author**: Linear Regression Analysis Team
- **Status**: Implementation Complete
- **Next Review**: Q1 2026