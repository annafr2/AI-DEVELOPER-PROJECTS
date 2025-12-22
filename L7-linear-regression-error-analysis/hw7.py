import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

print("=== AI EXP DEVELOPER Course - Machine Learning Exercise ===")
print("Linear Regression with Random Points and Error Analysis\n")

# ================================================================================
# STEP 1: Generate 1000 random 2D points (vectors)
# ================================================================================
print("STEP 1: Generating 1000 random 2D points")
print("-" * 50)

N_POINTS = 1000
# Generate random points between 0-1 (normalized)
# X is independent, Y is dependent
X_points = np.random.uniform(0, 1, N_POINTS)  # X coordinates (independent)
Y_points = np.random.uniform(0, 1, N_POINTS)  # Y coordinates (dependent)

# Create the data matrix (1000 x 2)
data_points = np.column_stack((X_points, Y_points))

print(f"Generated {N_POINTS} points")
print(f"X range: [{X_points.min():.3f}, {X_points.max():.3f}]")
print(f"Y range: [{Y_points.min():.3f}, {Y_points.max():.3f}]")
print(f"First 5 points:\n{data_points[:5]}\n")

# ================================================================================
# STEP 2: Plot the random points on coordinate system
# ================================================================================
print("STEP 2: Plotting the random points")
print("-" * 50)

plt.figure(figsize=(15, 12))

# Plot 1: Original random points
plt.subplot(2, 3, 1)
plt.scatter(X_points, Y_points, alpha=0.6, s=20, color='blue')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('1000 Random Points (0-1 normalized)')
plt.grid(True, alpha=0.3)
plt.axis('equal')

# ================================================================================
# STEP 3: Generate/Guess random A,B parameters for line equation
# ================================================================================
print("STEP 3: Testing multiple line parameters (A,B)")
print("-" * 50)

K_EXPERIMENTS = 100  # Number of experiments/trials
N_SAMPLES = 1000     # Number of data points

# Parameter ranges:
# B (intercept): 0-1 (intersection with Y-axis in first quadrant)
# A (slope): can be any value for first quadrant angles

best_error = float('inf')
best_A = None
best_B = None
all_errors = []

print(f"Running {K_EXPERIMENTS} experiments to find optimal line parameters...")

for experiment in range(K_EXPERIMENTS):
    # Generate random A and B
    A = random.uniform(-2, 4)  # Slope - wider range for better coverage
    B = random.uniform(0, 1)   # Intercept between 0-1
    
    # ============================================================================
    # STEP 4: Build line equation and calculate errors
    # ============================================================================
    # Line equation: Y = AX + B
    # Error for each point: ERR = (Y - AX - B)²
    
    predicted_Y = A * X_points + B
    errors = (Y_points - predicted_Y) ** 2  # Squared errors (always positive)
    
    # ============================================================================
    # STEP 5: Calculate average error (variance) for this experiment
    # ============================================================================
    mean_squared_error = np.mean(errors)  # Average of all errors = variance
    all_errors.append(mean_squared_error)
    
    # Keep track of best parameters
    if mean_squared_error < best_error:
        best_error = mean_squared_error
        best_A = A
        best_B = B
    
    if experiment % 20 == 0:  # Progress indicator
        print(f"Experiment {experiment}: A={A:.3f}, B={B:.3f}, MSE={mean_squared_error:.6f}")

print(f"\nCompleted {K_EXPERIMENTS} experiments")
print(f"Best parameters found:")
print(f"A (slope) = {best_A:.6f}")
print(f"B (intercept) = {best_B:.6f}")
print(f"Minimum average error = {best_error:.6f}")

# ================================================================================
# STEP 6: Choose and plot the line with minimum average error
# ================================================================================
print(f"\nSTEP 6: Drawing the optimal line")
print("-" * 50)

# Plot 2: Best line with random points
plt.subplot(2, 3, 2)
plt.scatter(X_points, Y_points, alpha=0.6, s=20, color='blue', label='Data points')

# Draw the best line
x_line = np.linspace(0, 1, 100)
y_line = best_A * x_line + best_B
plt.plot(x_line, y_line, 'red', linewidth=2, 
         label=f'Best Line: Y = {best_A:.3f}X + {best_B:.3f}')

plt.xlabel('X')
plt.ylabel('Y')
plt.title(f'Best Line (MSE = {best_error:.6f})')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(0, 1)
plt.ylim(0, 1.5)

# Plot 3: Error distribution
plt.subplot(2, 3, 3)
plt.hist(all_errors, bins=20, alpha=0.7, color='green')
plt.axvline(best_error, color='red', linestyle='--', 
            label=f'Best MSE = {best_error:.6f}')
plt.xlabel('Mean Squared Error')
plt.ylabel('Frequency')
plt.title('Distribution of Errors Across Experiments')
plt.legend()
plt.grid(True, alpha=0.3)

# ================================================================================
# STEP 7: SIMULATION PHASE - Generate data with known A,B + noise
# ================================================================================
print(f"\nSTEP 7: SIMULATION PHASE - Generating synthetic data")
print("-" * 50)

# Set true parameters for simulation
TRUE_A = 1.5  # True slope
TRUE_B = 0.2  # True intercept

print(f"True parameters: A = {TRUE_A}, B = {TRUE_B}")

# Generate X values
X_sim = np.random.uniform(0, 1, N_POINTS)

# Generate noise (epsilon) - small random noise
noise_std = 0.1  # Standard deviation of noise
epsilon = np.random.normal(0, noise_std, N_POINTS)

# Generate Y with equation: Y = AX + B + EPSILON
Y_sim = TRUE_A * X_sim + TRUE_B + epsilon

print(f"Generated synthetic data with noise (std = {noise_std})")

# Plot 4: Synthetic data with true line
plt.subplot(2, 3, 4)
plt.scatter(X_sim, Y_sim, alpha=0.6, s=20, color='orange', label='Noisy data')

# Draw true line
x_true = np.linspace(0, 1, 100)
y_true = TRUE_A * x_true + TRUE_B
plt.plot(x_true, y_true, 'green', linewidth=2, 
         label=f'True Line: Y = {TRUE_A}X + {TRUE_B}')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Synthetic Data with True Relationship')
plt.legend()
plt.grid(True, alpha=0.3)

# ================================================================================
# STEP 8: Data orientation analysis (variance in different directions)
# ================================================================================
print(f"\nSTEP 8: Data orientation and variance analysis")
print("-" * 50)

# Calculate covariance matrix
data_matrix = np.column_stack((X_sim, Y_sim))
cov_matrix = np.cov(data_matrix.T)

print("Covariance Matrix:")
print(cov_matrix)
print(f"Variance in X direction: {cov_matrix[0,0]:.6f}")
print(f"Variance in Y direction: {cov_matrix[1,1]:.6f}")
print(f"Covariance X-Y: {cov_matrix[0,1]:.6f}")

# Find principal components (eigenvectors and eigenvalues)
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
print(f"Eigenvalues (variances along principal axes): {eigenvalues}")

# Sort by eigenvalue
idx = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[idx]
eigenvectors = eigenvectors[:, idx]

print(f"Principal component 1 (max variance): {eigenvectors[:, 0]}")
print(f"Principal component 2 (min variance): {eigenvectors[:, 1]}")

# Plot 5: Data with principal components
plt.subplot(2, 3, 5)
plt.scatter(X_sim, Y_sim, alpha=0.6, s=20, color='orange', label='Data')

# Draw principal component vectors
center_x, center_y = np.mean(X_sim), np.mean(Y_sim)
scale = 0.3

# First principal component (max variance)
pc1_x = eigenvectors[0, 0] * scale
pc1_y = eigenvectors[1, 0] * scale
plt.arrow(center_x, center_y, pc1_x, pc1_y, 
          color='red', width=0.005, head_width=0.02, 
          label=f'PC1 (var={eigenvalues[0]:.3f})')

# Second principal component (min variance)
pc2_x = eigenvectors[0, 1] * scale
pc2_y = eigenvectors[1, 1] * scale
plt.arrow(center_x, center_y, pc2_x, pc2_y, 
          color='blue', width=0.005, head_width=0.02,
          label=f'PC2 (var={eigenvalues[1]:.3f})')

# Draw data ellipse
angle = np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]) * 180 / np.pi
ellipse = Ellipse((center_x, center_y), 
                  width=np.sqrt(eigenvalues[0])*2, 
                  height=np.sqrt(eigenvalues[1])*2,
                  angle=angle, alpha=0.2, color='gray')
plt.gca().add_patch(ellipse)

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Principal Component Analysis')
plt.legend()
plt.grid(True, alpha=0.3)
plt.axis('equal')

# Plot 6: Regression line vs Principal Component
plt.subplot(2, 3, 6)
plt.scatter(X_sim, Y_sim, alpha=0.6, s=20, color='orange', label='Data')

# True regression line
plt.plot(x_true, y_true, 'green', linewidth=2, label='True regression')

# Principal component direction as a line
pc1_slope = eigenvectors[1, 0] / eigenvectors[0, 0]
pc1_intercept = center_y - pc1_slope * center_x
x_pc = np.linspace(0, 1, 100)
y_pc = pc1_slope * x_pc + pc1_intercept
plt.plot(x_pc, y_pc, 'red', linewidth=2, linestyle='--', 
         label=f'PC1 direction (slope={pc1_slope:.3f})')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Regression vs Principal Component')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ================================================================================
# SUMMARY AND EXPLANATION
# ================================================================================
print(f"\n" + "="*70)
print("SUMMARY AND EXPLANATION")
print("="*70)

print(f"""
WHAT WE DID AND WHY:

1. RANDOM POINT GENERATION:
   - Generated {N_POINTS} random points to simulate real data
   - X and Y coordinates between 0-1 (normalized)

2. LINE FITTING EXPERIMENT:
   - Tested {K_EXPERIMENTS} different line parameters (A, B)
   - For each line, calculated Mean Squared Error (MSE)
   - MSE = average of (Y - AX - B)² across all points

3. WHY CALCULATE PREDICTION ERROR?
   - To find the best line that fits our data
   - Lower error = better prediction accuracy
   - This is the foundation of machine learning!

4. OPTIMAL PARAMETERS FOUND:
   - Best A (slope): {best_A:.6f}
   - Best B (intercept): {best_B:.6f} 
   - Minimum error: {best_error:.6f}

5. SIMULATION WITH KNOWN TRUTH:
   - Generated data with TRUE_A = {TRUE_A}, TRUE_B = {TRUE_B}
   - Added noise to make it realistic
   - This shows how regression works with real noisy data

6. DATA ORIENTATION ANALYSIS:
   - Calculated how data spreads in different directions
   - Principal Component 1: direction of maximum variance
   - This is where the most "information" lies
   - PC1 often aligns with the regression line!

7. REGRESSION = RELATIONSHIP DISCOVERY:
   - Regression finds the best linear relationship between X and Y
   - It's like finding the "average" direction of the data cloud
   - The goal is optimal prediction of Y given X

REAL-WORLD APPLICATIONS:
- Predicting house prices from size (X=size, Y=price)
- Stock price prediction from market indicators  
- Medical diagnosis from symptoms
- And much more!
""")

print("\nThis exercise demonstrates the core concepts of:")
print("• Linear regression")
print("• Error minimization") 
print("• Principal component analysis")
print("• The relationship between regression and data orientation")
print("\nThese are fundamental building blocks of machine learning!")