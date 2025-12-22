import numpy as np
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(42)

# Step 1: Generate simulation data
# Choose true parameters B0 and B1
true_b0 = 5.0   # Intercept (true value)
true_b1 = 2.5   # Slope (true value)

# Generate X values - 10,000 points from normal distribution
n_samples = 10000
X = np.random.normal(loc=0, scale=1, size=n_samples)

# Generate noise (epsilon) - small random error
noise_std = 0.5  # Standard deviation of noise
epsilon = np.random.normal(loc=0, scale=noise_std, size=n_samples)

# Generate Y using the linear relationship: y = b0 + b1*x + epsilon
Y = true_b0 + true_b1 * X + epsilon

# Display the generated data
print(f"Generated {n_samples} data points")
print(f"True B0 (intercept): {true_b0}")
print(f"True B1 (slope): {true_b1}")
print(f"Noise standard deviation: {noise_std}")
print(f"\nX statistics:")
print(f"  Mean: {np.mean(X):.4f}")
print(f"  Std: {np.std(X):.4f}")
print(f"  Min: {np.min(X):.4f}")
print(f"  Max: {np.max(X):.4f}")
print(f"\nY statistics:")
print(f"  Mean: {np.mean(Y):.4f}")
print(f"  Std: {np.std(Y):.4f}")
print(f"  Min: {np.min(Y):.4f}")
print(f"  Max: {np.max(Y):.4f}")

# Create a scatter plot to visualize the data (sample of 1000 points)
sample_size = 1000
sample_indices = np.random.choice(n_samples, sample_size, replace=False)
X_sample = X[sample_indices]
Y_sample = Y[sample_indices]

plt.figure(figsize=(10, 6))
plt.scatter(X_sample, Y_sample, alpha=0.6, s=10)
plt.xlabel('X')
plt.ylabel('Y')
plt.title(f'Generated Data Sample ({sample_size} points)\nTrue relationship: Y = {true_b0} + {true_b1}*X + ε')
plt.grid(True, alpha=0.3)
plt.show()

# Save the generated data for next steps
print(f"\nData generated successfully!")
print(f"Shape of X: {X.shape}")
print(f"Shape of Y: {Y.shape}")

# Step 2: Calculate regression coefficients using the formulas
# We use the data X and Y generated in Step 1

# Calculate sample means
X_mean = np.mean(X)  # x̄ (x-bar)
Y_mean = np.mean(Y)  # ȳ (y-bar)

print("Step 2: Calculating Linear Regression Coefficients")
print("=" * 50)
print(f"Sample means:")
print(f"  X̄ (X-bar): {X_mean:.6f}")
print(f"  Ȳ (Y-bar): {Y_mean:.6f}")

# Calculate deviations from means using vectorized operations
X_deviations = X - X_mean  # (xi - x̄)
Y_deviations = Y - Y_mean  # (yi - ȳ)

print(f"\nDeviations calculated:")
print(f"  X deviations shape: {X_deviations.shape}")
print(f"  Y deviations shape: {Y_deviations.shape}")

# Calculate B1 (slope coefficient) using the formula from the image:
# β₁ = Σ(xi - x̄)(yi - ȳ) / Σ(xi - x̄)²

# Numerator: sum of products of deviations
numerator = np.sum(X_deviations * Y_deviations) #change to dot operand

# Denominator: sum of squared X deviations  
denominator = np.sum(X_deviations ** 2)

# Calculate B1 (slope)
estimated_b1 = numerator / denominator

print(f"\nB1 (Slope) calculation:")
print(f"  Numerator (Σ(xi-x̄)(yi-ȳ)): {numerator:.6f}")
print(f"  Denominator (Σ(xi-x̄)²): {denominator:.6f}")
print(f"  B1 = {estimated_b1:.6f}")

# Calculate B0 (intercept) using the formula:
# β₀ = ȳ - β₁x̄
estimated_b0 = Y_mean - estimated_b1 * X_mean

print(f"\nB0 (Intercept) calculation:")
print(f"  B0 = Ȳ - B1*X̄")
print(f"  B0 = {Y_mean:.6f} - {estimated_b1:.6f} * {X_mean:.6f}")
print(f"  B0 = {estimated_b0:.6f}")

# Compare with true values
print(f"\n" + "=" * 50)
print("RESULTS COMPARISON:")
print("=" * 50)
print(f"{'Parameter':<12} {'True Value':<12} {'Estimated':<12} {'Error':<12}")
print("-" * 50)
print(f"{'B0 (Intercept)':<12} {true_b0:<12.6f} {estimated_b0:<12.6f} {abs(true_b0 - estimated_b0):<12.6f}")
print(f"{'B1 (Slope)':<12} {true_b1:<12.6f} {estimated_b1:<12.6f} {abs(true_b1 - estimated_b1):<12.6f}")

# Calculate percentage errors
b0_error_percent = abs(true_b0 - estimated_b0) / abs(true_b0) * 100
b1_error_percent = abs(true_b1 - estimated_b1) / abs(true_b1) * 100

print(f"\nPercentage Errors:")
print(f"  B0 error: {b0_error_percent:.4f}%")
print(f"  B1 error: {b1_error_percent:.4f}%")

# Create predicted values using estimated coefficients
Y_predicted = estimated_b0 + estimated_b1 * X

# Calculate R-squared (coefficient of determination)
SS_total = np.sum((Y - Y_mean) ** 2)  # Total sum of squares
SS_residual = np.sum((Y - Y_predicted) ** 2)  # Residual sum of squares
r_squared = 1 - (SS_residual / SS_total)

print(f"\nModel Performance:")
print(f"  R-squared: {r_squared:.6f}")
print(f"  Root Mean Square Error: {np.sqrt(np.mean((Y - Y_predicted) ** 2)):.6f}")

# Step 3: Visualization of Linear Regression Results

# Create comprehensive plots to visualize the results
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Linear Regression Analysis Results', fontsize=16, fontweight='bold')

# Sample data for plotting (use subset for better visualization)
plot_sample_size = 2000
sample_indices = np.random.choice(n_samples, plot_sample_size, replace=False)
X_plot = X[sample_indices]
Y_plot = Y[sample_indices]
Y_pred_plot = Y_predicted[sample_indices]

# Plot 1: Scatter plot with regression lines
axes[0, 0].scatter(X_plot, Y_plot, alpha=0.5, s=8, color='lightblue', label='Data points')

# True regression line
X_line = np.linspace(X_plot.min(), X_plot.max(), 100)
Y_true_line = true_b0 + true_b1 * X_line
axes[0, 0].plot(X_line, Y_true_line, 'r-', linewidth=3, 
                label=f'True: Y = {true_b0} + {true_b1}X')

# Estimated regression line
Y_est_line = estimated_b0 + estimated_b1 * X_line
axes[0, 0].plot(X_line, Y_est_line, 'g--', linewidth=3, 
                label=f'Estimated: Y = {estimated_b0:.3f} + {estimated_b1:.3f}X')

axes[0, 0].set_xlabel('X')
axes[0, 0].set_ylabel('Y')
axes[0, 0].set_title('Data Points with Regression Lines')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Plot 2: Predicted vs Actual values
axes[0, 1].scatter(Y_plot, Y_pred_plot, alpha=0.5, s=8, color='orange')
# Perfect prediction line (45-degree line)
min_val = min(Y_plot.min(), Y_pred_plot.min())
max_val = max(Y_plot.max(), Y_pred_plot.max())
axes[0, 1].plot([min_val, max_val], [min_val, max_val], 'r--', 
                linewidth=2, label='Perfect Prediction')
axes[0, 1].set_xlabel('Actual Y')
axes[0, 1].set_ylabel('Predicted Y')
axes[0, 1].set_title(f'Predicted vs Actual Values\nR² = {r_squared:.6f}')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Plot 3: Residuals plot
residuals = Y_plot - Y_pred_plot
axes[1, 0].scatter(Y_pred_plot, residuals, alpha=0.5, s=8, color='purple')
axes[1, 0].axhline(y=0, color='r', linestyle='-', linewidth=2)
axes[1, 0].set_xlabel('Predicted Y')
axes[1, 0].set_ylabel('Residuals (Actual - Predicted)')
axes[1, 0].set_title('Residuals Plot')
axes[1, 0].grid(True, alpha=0.3)

# Plot 4: Histogram of residuals
axes[1, 1].hist(residuals, bins=50, alpha=0.7, color='green', edgecolor='black')
axes[1, 1].axvline(x=0, color='r', linestyle='--', linewidth=2)
axes[1, 1].set_xlabel('Residuals')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].set_title(f'Distribution of Residuals\nMean: {np.mean(residuals):.6f}')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Create summary statistics table
print("\n" + "=" * 60)
print("DETAILED ANALYSIS SUMMARY")
print("=" * 60)

# Coefficient comparison table
print("\nCoefficient Estimation Results:")
print("-" * 45)
coeffs_data = [
    ["Parameter", "True Value", "Estimated", "Absolute Error", "% Error"],
    ["-" * 9, "-" * 10, "-" * 9, "-" * 14, "-" * 8],
    ["B0", f"{true_b0:.6f}", f"{estimated_b0:.6f}", 
     f"{abs(true_b0 - estimated_b0):.6f}", f"{b0_error_percent:.4f}%"],
    ["B1", f"{true_b1:.6f}", f"{estimated_b1:.6f}", 
     f"{abs(true_b1 - estimated_b1):.6f}", f"{b1_error_percent:.4f}%"]
]

for row in coeffs_data:
    print(f"{row[0]:>12} {row[1]:>12} {row[2]:>12} {row[3]:>14} {row[4]:>10}")

# Model performance metrics
print(f"\nModel Performance Metrics:")
print("-" * 30)
rmse = np.sqrt(np.mean((Y - Y_predicted) ** 2))
mae = np.mean(np.abs(Y - Y_predicted))
print(f"R-squared (R²):           {r_squared:.6f}")
print(f"Root Mean Square Error:   {rmse:.6f}")
print(f"Mean Absolute Error:      {mae:.6f}")
print(f"Residuals Mean:           {np.mean(Y - Y_predicted):.8f}")
print(f"Residuals Std:            {np.std(Y - Y_predicted):.6f}")

# Data characteristics
print(f"\nData Characteristics:")
print("-" * 25)
print(f"Sample size:              {n_samples:,}")
print(f"Noise std deviation:      {noise_std}")
print(f"X range:                  [{X.min():.3f}, {X.max():.3f}]")
print(f"Y range:                  [{Y.min():.3f}, {Y.max():.3f}]")

print(f"\n" + "=" * 60)
print("SUCCESS! Linear regression coefficients estimated successfully!")
print("The estimated values are very close to the true parameters.")
print("=" * 60)