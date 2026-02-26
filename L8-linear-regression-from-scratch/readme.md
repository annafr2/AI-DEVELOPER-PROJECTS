# 📈 Linear Regression from Scratch

A comprehensive implementation of linear regression using pure mathematical formulas and NumPy vectorized operations, without relying on built-in regression functions.

## 🎯 Overview

This project demonstrates the mathematical foundations of linear regression by:
1. **Simulating data** with known parameters
2. **Implementing OLS formulas** using vectorized operations
3. **Recovering parameters** with high accuracy
4. **Visualizing results** comprehensively

## 🚀 Quick Start

### Prerequisites
```bash
pip install numpy matplotlib
```

### Running the Analysis
Execute the three main steps in sequence:

1. **Step 1: Data Simulation**
   ```python
   python step1_simulation.py
   ```

2. **Step 2: Regression Calculation**
   ```python
   python step2_regression.py
   ```

3. **Step 3: Visualization**
   ```python
   python step3_visualization.py
   ```

## 📊 What This Project Does

### Step 1: Data Simulation
- Defines true parameters B₀ = 5.0, B₁ = 2.5
- Generates 10,000 X values from normal distribution
- Adds controlled noise (ε ~ N(0, 0.5))
- Creates Y values: **Y = B₀ + B₁X + ε**

### Step 2: Mathematical Implementation
Implements the exact OLS formulas:

**Slope Coefficient:**
```
β₁ = Σ(xᵢ - x̄)(yᵢ - ȳ) / Σ(xᵢ - x̄)²
```

**Intercept:**
```
β₀ = ȳ - β₁x̄
```

### Step 3: Analysis & Visualization
Creates comprehensive plots:
- Scatter plot with regression lines (true vs estimated)
- Predicted vs actual values
- Residuals analysis
- Distribution of residuals

## 📈 Expected Results

With the default parameters, you should see:
- **B₀ estimation error**: < 0.01 (< 0.2%)
- **B₁ estimation error**: < 0.01 (< 0.4%)
- **R-squared**: > 0.99
- **RMSE**: ≈ 0.5 (noise level)

## 🔧 Technical Implementation

### Key Features
- ✅ **No built-in regression functions** - Pure mathematical implementation
- ✅ **Vectorized operations** - No loops, efficient NumPy operations
- ✅ **Large sample handling** - Efficiently processes 10,000+ data points
- ✅ **Comprehensive validation** - Multiple accuracy metrics and visualizations

### Code Structure
```
📁 linear_regression_exercise/
├── 📄 step1_simulation.py      # Data generation
├── 📄 step2_regression.py      # OLS implementation
├── 📄 step3_visualization.py   # Results analysis
├── 📄 README.md               # This file
└── 📄 PRD.md                  # Product Requirements Document
```

## 🧮 Mathematical Foundation

The implementation follows the standard Ordinary Least Squares (OLS) method:

1. **Calculate means**: x̄ = (1/n)Σxᵢ, ȳ = (1/n)Σyᵢ
2. **Compute deviations**: (xᵢ - x̄), (yᵢ - ȳ)
3. **Apply formulas**: Use vectorized operations for efficient computation
4. **Validate results**: Compare estimated vs true parameters

## 📊 Sample Output

```
RESULTS COMPARISON:
==================================================
Parameter    True Value   Estimated    Error
--------------------------------------------------
B0 (Intercept) 5.000000     5.006758     0.006758
B1 (Slope)     2.500000     2.495734     0.004266

Percentage Errors:
  B0 error: 0.1351%
  B1 error: 0.1706%

Model Performance:
  R-squared: 0.996824
  Root Mean Square Error: 0.499891
```

## 🎨 Visualizations Generated

1. **Data Points with Regression Lines**
   - Original data scatter plot
   - True regression line (red)
   - Estimated regression line (green dashed)

2. **Predicted vs Actual Values**
   - Scatter plot of predictions vs reality
   - Perfect prediction line for reference
   - R² value displayed

3. **Residuals Analysis**
   - Residuals vs predicted values
   - Should show random scatter around zero

4. **Residuals Distribution**
   - Histogram of residuals
   - Should approximate normal distribution

## 🔬 Educational Value

This project teaches:
- **Mathematical foundations** of linear regression
- **Vectorized programming** techniques
- **Statistical validation** methods
- **Data visualization** best practices
- **Parameter estimation** concepts

## 🛠️ Customization Options

You can modify these parameters in the code:

```python
# Simulation parameters
true_b0 = 5.0          # True intercept
true_b1 = 2.5          # True slope
n_samples = 10000      # Sample size
noise_std = 0.5        # Noise level
```

## 📚 Dependencies

- **NumPy**: Mathematical operations and array handling
- **Matplotlib**: Data visualization and plotting

## 🤝 Contributing

This is an educational exercise. Feel free to:
- Experiment with different parameters
- Add new visualizations
- Implement additional metrics
- Test with real-world datasets

## 📄 Documentation

- **README.md** - This file (user guide and overview)
- **PRD.md** - Product Requirements Document (detailed specifications)

## ⚡ Performance Notes

- **Efficient**: Uses vectorized NumPy operations
- **Scalable**: Handles large datasets (tested with 10,000+ points)
- **Fast**: Complete analysis typically runs in < 5 seconds

## 🎓 Learning Outcomes

After running this project, you will understand:
1. How linear regression works mathematically
2. The relationship between theory and implementation
3. How to validate statistical models
4. Effective data visualization techniques
5. Vectorized computation benefits

---

