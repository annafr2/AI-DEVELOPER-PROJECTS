import numpy as np
import matplotlib.pyplot as plt

# Set basic parameters
np.random.seed(42)  # For reproducibility
n_samples = 1000    # Number of observations
n_features = 50     # Number of independent variables
n_epsilon_values = 20  # Number of different variance values to test

# Step 1: Create simulated data
print("=== Step 1: Creating Simulated Data ===")

# Create X matrix (independent variables)
# Each column is a variable, each row is an observation
X = np.random.randn(n_samples, n_features)
print(f"X matrix shape: {X.shape}")

# Add intercept column (column of ones)
X_with_intercept = np.column_stack([np.ones(n_samples), X])
print(f"X matrix with intercept shape: {X_with_intercept.shape}")

# Set fixed beta vector (true coefficients)
# beta_0 is intercept, beta_1 to beta_50 are variable coefficients
true_beta = np.random.uniform(-2, 2, n_features + 1)  # +1 for intercept
print(f"Beta values (first 5): {true_beta[:5]}")

# Calculate expected value of y (without error)
y_true = X_with_intercept @ true_beta
print(f"y_true shape: {y_true.shape}")

def calculate_r_squared_manual(y_actual, y_predicted):
    """
    Calculate R² manually using formula R² = 1 - SSE/SST
    
    Args:
        y_actual: actual y values
        y_predicted: predicted y values
    
    Returns:
        r_squared: R² value
    """
    # Calculate SSE (Sum of Squared Errors)
    sse = np.sum((y_actual - y_predicted) ** 2)
    
    # Calculate SST (Total Sum of Squares)
    y_mean = np.mean(y_actual)
    sst = np.sum((y_actual - y_mean) ** 2)
    
    # Calculate R²
    r_squared = 1 - (sse / sst)
    
    return r_squared

def fit_linear_regression_manual(X, y):
    """
    Perform linear regression manually using linear algebra
    Formula: β = (X^T * X)^(-1) * X^T * y
    
    Args:
        X: matrix of independent variables (including intercept)
        y: dependent variable vector
    
    Returns:
        beta_hat: estimated coefficients vector
        y_pred: predictions for dependent variable
    """
    # Calculate X^T * X
    XtX = X.T @ X
    
    # Calculate (X^T * X)^(-1)
    XtX_inv = np.linalg.inv(XtX)
    
    # Calculate X^T * y
    Xty = X.T @ y
    
    # Calculate coefficients: β = (X^T * X)^(-1) * X^T * y
    beta_hat = XtX_inv @ Xty
    
    # Calculate predictions
    y_pred = X @ beta_hat
    
    return beta_hat, y_pred

# Create range of error variances - small to large
sigma_values = np.logspace(-1, 1, n_epsilon_values)  # from 0.1 to 10
r_squared_values = []

print(f"\n=== Testing R² for {n_epsilon_values} different error variance levels ===")

for i, sigma in enumerate(sigma_values):
    # Create error vector with current variance
    epsilon = np.random.normal(0, sigma, n_samples)
    
    # Create y with noise
    y_with_noise = y_true + epsilon
    
    # Perform linear regression
    beta_estimated, y_predicted = fit_linear_regression_manual(X_with_intercept, y_with_noise)
    
    # Calculate R²
    r_squared = calculate_r_squared_manual(y_with_noise, y_predicted)
    r_squared_values.append(r_squared)
    
    if i % 5 == 0:  # Print every 5 iterations
        print(f"σ = {sigma:.3f}, R² = {r_squared:.4f}")

print(f"\nR² range: {min(r_squared_values):.4f} - {max(r_squared_values):.4f}")

# Create the plot
plt.figure(figsize=(10, 6))
plt.semilogx(sigma_values, r_squared_values, 'b-o', linewidth=2, markersize=6)
plt.xlabel('Error Variance (σ)', fontsize=12)
plt.ylabel('R²', fontsize=12)
plt.title('Relationship between Error Variance and R²\n(50 independent variables)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.ylim(0, 1.1)

# Add explanations to plot
plt.text(0.5, 0.8, 'Low Variance\n↓\nHigh R²', 
         horizontalalignment='center', fontsize=10, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))

plt.text(5, 0.2, 'High Variance\n↓\nLow R²', 
         horizontalalignment='center', fontsize=10,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral"))

plt.tight_layout()
plt.show()

print("\n=== Step 1 Summary ===")
print(f"• Created data with {n_samples} observations and {n_features} variables")
print(f"• Tested {n_epsilon_values} different error variance levels")
print(f"• Highest R²: {max(r_squared_values):.4f} (low variance)")
print(f"• Lowest R²: {min(r_squared_values):.4f} (high variance)")
print("The plot shows how increasing error variance hurts model prediction ability")

# =================================================================
# Step 2: Adding additional variables (X², interactions, etc.)
# =================================================================

print("\n\n=== Step 2: Adding 20 Additional Variables ===")

def create_extended_features(X_original):
    """
    Create 20 additional variables from original variables
    Including: squares, square roots, interactions, and complex variables
    
    Args:
        X_original: original variables matrix (without intercept)
    
    Returns:
        X_extended: extended matrix with additional variables
    """
    n_samples, n_features = X_original.shape
    extended_features = []
    
    # Squares of first variables (5 variables)
    for i in range(min(5, n_features)):
        extended_features.append(X_original[:, i] ** 2)
    
    # Square roots of absolute values (5 variables)
    for i in range(5, min(10, n_features)):
        extended_features.append(np.sqrt(np.abs(X_original[:, i])))
    
    # Interactions between pairs of variables (10 variables)
    interaction_count = 0
    for i in range(n_features):
        for j in range(i+1, n_features):
            if interaction_count < 10:
                extended_features.append(X_original[:, i] * X_original[:, j])
                interaction_count += 1
            else:
                break
        if interaction_count >= 10:
            break
    
    # Convert to matrix
    X_extended = np.column_stack(extended_features)
    return X_extended

# Create extended variables
X_extended = create_extended_features(X)
print(f"Extended matrix shape: {X_extended.shape}")

# Combine original and extended variables
X_combined = np.column_stack([X, X_extended])
X_combined_with_intercept = np.column_stack([np.ones(n_samples), X_combined])
print(f"Combined matrix shape (with intercept): {X_combined_with_intercept.shape}")

# Create new beta vector for extended variables
true_beta_extended = np.random.uniform(-1, 1, X_extended.shape[1])
true_beta_combined = np.concatenate([true_beta, true_beta_extended])
print(f"Combined beta vector length: {len(true_beta_combined)}")

# Calculate true y with extended variables
y_true_extended = X_combined_with_intercept @ true_beta_combined

# Test R² with extended variables
r_squared_extended_values = []

print(f"\n=== Testing R² with extended variables ({X_combined.shape[1]} variables) ===")

for i, sigma in enumerate(sigma_values):
    # Create error vector
    epsilon = np.random.normal(0, sigma, n_samples)
    
    # Create y with noise
    y_with_noise_extended = y_true_extended + epsilon
    
    # Perform linear regression
    beta_estimated_ext, y_predicted_ext = fit_linear_regression_manual(
        X_combined_with_intercept, y_with_noise_extended
    )
    
    # Calculate R²
    r_squared_ext = calculate_r_squared_manual(y_with_noise_extended, y_predicted_ext)
    r_squared_extended_values.append(r_squared_ext)
    
    if i % 5 == 0:  # Print every 5 iterations
        print(f"σ = {sigma:.3f}, R² = {r_squared_ext:.4f}")

# Create comparison plot
plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
plt.semilogx(sigma_values, r_squared_values, 'b-o', linewidth=2, markersize=6, label='50 variables only')
plt.semilogx(sigma_values, r_squared_extended_values, 'r-s', linewidth=2, markersize=6, label='70 variables (50+20)')
plt.xlabel('Error Variance (σ)', fontsize=12)
plt.ylabel('R²', fontsize=12)
plt.title('Comparison: R² with and without additional variables', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.ylim(0, 1.1)

plt.subplot(2, 1, 2)
r_squared_improvement = np.array(r_squared_extended_values) - np.array(r_squared_values)
plt.semilogx(sigma_values, r_squared_improvement, 'g-^', linewidth=2, markersize=6)
plt.xlabel('Error Variance (σ)', fontsize=12)
plt.ylabel('R² Improvement (70 variables - 50 variables)', fontsize=12)
plt.title('Performance Improvement from Adding Variables', fontsize=14)
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()

print("\n=== Step 2 Summary ===")
print(f"• Added 20 additional variables (squares, square roots, interactions)")
print(f"• Total variables: {X_combined.shape[1]}")
print(f"• Average R² improvement: {np.mean(r_squared_improvement):.4f}")
print(f"• Maximum R² improvement: {max(r_squared_improvement):.4f}")
print("• Additional variables improve performance, especially when variance is low")

# =================================================================
# Step 3: Calculate Adjusted R² (R_adj)
# =================================================================

print("\n\n=== Step 3 Bonus: Calculate Adjusted R² (R_adj) ===")

def calculate_adjusted_r_squared(r_squared, n_samples, n_features):
    """
    Calculate Adjusted R² - corrects for artificial increase in R² due to adding variables
    
    Formula: R²_adj = 1 - (1-R²) * (n-1) / (n-p-1)
    where n = number of observations, p = number of independent variables
    
    Args:
        r_squared: regular R²
        n_samples: number of observations
        n_features: number of independent variables (without intercept)
    
    Returns:
        adjusted_r_squared: adjusted R²
    """
    adj_r_squared = 1 - (1 - r_squared) * (n_samples - 1) / (n_samples - n_features - 1)
    return adj_r_squared

# Calculate adjusted R² for both models
r_squared_adj_basic = []  # Adjusted R² for 50 variables
r_squared_adj_extended = []  # Adjusted R² for 70 variables

print("Calculating adjusted R² for both models:")

for i, (r_sq_basic, r_sq_ext) in enumerate(zip(r_squared_values, r_squared_extended_values)):
    # Adjusted R² for basic model (50 variables)
    adj_basic = calculate_adjusted_r_squared(r_sq_basic, n_samples, n_features)
    r_squared_adj_basic.append(adj_basic)
    
    # Adjusted R² for extended model (70 variables)
    adj_extended = calculate_adjusted_r_squared(r_sq_ext, n_samples, X_combined.shape[1])
    r_squared_adj_extended.append(adj_extended)
    
    if i % 5 == 0:
        print(f"σ = {sigma_values[i]:.3f}:")
        print(f"  Regular R²: {r_sq_basic:.4f} → Adjusted R²: {adj_basic:.4f}")
        print(f"  Extended R²: {r_sq_ext:.4f} → Adjusted R²: {adj_extended:.4f}")

# Create comprehensive plot with all metrics
plt.figure(figsize=(15, 10))

# Plot 1: Compare regular R²
plt.subplot(2, 2, 1)
plt.semilogx(sigma_values, r_squared_values, 'b-o', linewidth=2, markersize=5, label='50 variables')
plt.semilogx(sigma_values, r_squared_extended_values, 'r-s', linewidth=2, markersize=5, label='70 variables')
plt.xlabel('Error Variance (σ)')
plt.ylabel('Regular R²')
plt.title('Regular R²: 50 vs 70 variables')
plt.legend()
plt.grid(True, alpha=0.3)
plt.ylim(0, 1.1)

# Plot 2: Compare adjusted R²
plt.subplot(2, 2, 2)
plt.semilogx(sigma_values, r_squared_adj_basic, 'b-o', linewidth=2, markersize=5, label='50 variables')
plt.semilogx(sigma_values, r_squared_adj_extended, 'r-s', linewidth=2, markersize=5, label='70 variables')
plt.xlabel('Error Variance (σ)')
plt.ylabel('Adjusted R²')
plt.title('Adjusted R²: 50 vs 70 variables')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 3: Adjustment effect on basic model
plt.subplot(2, 2, 3)
penalty_basic = np.array(r_squared_values) - np.array(r_squared_adj_basic)
plt.semilogx(sigma_values, penalty_basic, 'g-^', linewidth=2, markersize=5)
plt.xlabel('Error Variance (σ)')
plt.ylabel('Penalty (Regular R² - Adjusted R²)')
plt.title('Adjustment Penalty - Basic Model (50 variables)')
plt.grid(True, alpha=0.3)

# Plot 4: Adjustment effect on extended model
plt.subplot(2, 2, 4)
penalty_extended = np.array(r_squared_extended_values) - np.array(r_squared_adj_extended)
plt.semilogx(sigma_values, penalty_extended, 'm-^', linewidth=2, markersize=5)
plt.xlabel('Error Variance (σ)')
plt.ylabel('Penalty (Regular R² - Adjusted R²)')
plt.title('Adjustment Penalty - Extended Model (70 variables)')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Final summary plot - comprehensive comparison
plt.figure(figsize=(14, 8))

plt.subplot(1, 2, 1)
plt.semilogx(sigma_values, r_squared_values, 'b-o', linewidth=2, markersize=6, label='Regular R² (50)')
plt.semilogx(sigma_values, r_squared_adj_basic, 'b--o', linewidth=2, markersize=6, label='Adjusted R² (50)')
plt.semilogx(sigma_values, r_squared_extended_values, 'r-s', linewidth=2, markersize=6, label='Regular R² (70)')
plt.semilogx(sigma_values, r_squared_adj_extended, 'r--s', linewidth=2, markersize=6, label='Adjusted R² (70)')
plt.xlabel('Error Variance (σ)', fontsize=12)
plt.ylabel('R²', fontsize=12)
plt.title('Comprehensive Comparison: Regular vs Adjusted R²', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.ylim(0, 1.1)

plt.subplot(1, 2, 2)
advantage_basic = np.array(r_squared_adj_basic) - np.array(r_squared_values)
advantage_extended = np.array(r_squared_adj_extended) - np.array(r_squared_extended_values)
plt.semilogx(sigma_values, advantage_basic, 'b-o', linewidth=2, markersize=6, label='Adjusted R² advantage (50)')
plt.semilogx(sigma_values, advantage_extended, 'r-s', linewidth=2, markersize=6, label='Adjusted R² advantage (70)')
plt.xlabel('Error Variance (σ)', fontsize=12)
plt.ylabel('Adjusted R² Advantage (negative = penalty)', fontsize=12)
plt.title('Adjusted R² Penalty as Function of Number of Variables', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='black', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()

print("\n=== Step 3 Summary (Bonus) ===")
print(f"• Adjusted R² handles the overfitting problem created by adding variables")
print(f"• Average penalty for basic model: {np.mean(penalty_basic):.4f}")
print(f"• Average penalty for extended model: {np.mean(penalty_extended):.4f}")
print(f"• Extended model receives higher penalty due to 20 additional variables")
print("• Adjusted R² helps decide if adding variables truly improves the model")

print("\n" + "="*70)
print("COMPLETE PROJECT SUMMARY")
print("="*70)
print("1. Created simulated data with 50 variables and tested how error variance affects R²")
print("2. Added 20 additional variables (squares, interactions) and saw performance improvement")
print("3. Used adjusted R² to examine if improvement is real or artificial")
print("4. All calculations performed using linear algebra only (no built-in functions)")
print("\nResults show the importance of balancing model accuracy with complexity!")