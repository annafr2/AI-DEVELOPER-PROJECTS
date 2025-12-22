"""
Visualization functions for Logistic Regression
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logistic_regression import LogisticRegression

plt.rcParams['font.family'] = 'DejaVu Sans'


def plot_data_and_boundary(X: np.ndarray, y: np.ndarray,
                           model: 'LogisticRegression',
                           save_path: str = 'outputs/decision_boundary.png'):
    """Plot dataset with decision boundary"""
    plt.figure(figsize=(12, 10))
    
    # Extract features (without bias)
    X_plot = X[:, 1:]
    
    # Plot data points
    plt.scatter(X_plot[y == 0, 0], X_plot[y == 0, 1], 
               c='blue', marker='o', s=100, alpha=0.6, 
               edgecolors='black', linewidth=1.5, label='Group 0 (Healthy)')
    plt.scatter(X_plot[y == 1, 0], X_plot[y == 1, 1], 
               c='red', marker='s', s=100, alpha=0.6, 
               edgecolors='black', linewidth=1.5, label='Group 1 (Sick)')
    
    # Decision boundary mesh
    x1_min, x1_max = X_plot[:, 0].min() - 0.1, X_plot[:, 0].max() + 0.1
    x2_min, x2_max = X_plot[:, 1].min() - 0.1, X_plot[:, 1].max() + 0.1
    
    xx1, xx2 = np.meshgrid(np.linspace(x1_min, x1_max, 200),
                            np.linspace(x2_min, x2_max, 200))
    
    X_mesh = np.c_[np.ones(xx1.ravel().shape), xx1.ravel(), xx2.ravel()]
    Z = model.predict_proba(X_mesh)
    Z = Z.reshape(xx1.shape)
    
    # Plot probability contours
    contour = plt.contourf(xx1, xx2, Z, levels=20, cmap='RdYlBu_r', alpha=0.3)
    plt.colorbar(contour, label='Probability (Sigmoid)')
    plt.contour(xx1, xx2, Z, levels=[0.5], colors='green', linewidths=3, 
                linestyles='--', label='Decision Boundary (p=0.5)')
    
    plt.xlabel('X1 (Feature 1)', fontsize=14, fontweight='bold')
    plt.ylabel('X2 (Feature 2)', fontsize=14, fontweight='bold')
    plt.title('Dataset with Decision Boundary\nLogistic Regression Classification', 
              fontsize=16, fontweight='bold')
    plt.legend(fontsize=11, loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {save_path}")


def plot_predictions_comparison(y_true: np.ndarray, y_pred_proba: np.ndarray,
                                save_path: str = 'outputs/predictions_comparison.png'):
    """Plot true labels vs predictions"""
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot 1: Scatter plot
    ax1 = axes[0]
    indices = np.arange(len(y_true))
    
    ax1.scatter(indices, y_true, c='green', marker='o', s=50, 
               alpha=0.6, label='True Labels', edgecolors='black', linewidth=1)
    ax1.scatter(indices, y_pred_proba, c='orange', marker='x', s=50, 
               alpha=0.7, label='Predicted Probability')
    
    ax1.axhline(y=0.5, color='red', linestyle='--', linewidth=2, 
               alpha=0.7, label='Threshold (0.5)')
    ax1.set_xlabel('Sample Index', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Value', fontsize=12, fontweight='bold')
    ax1.set_title('True Labels vs Predicted Probabilities', 
                  fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Histogram of predictions
    ax2 = axes[1]
    ax2.hist(y_pred_proba[y_true == 0], bins=30, alpha=0.6, 
            color='blue', label='Class 0 (Healthy)', edgecolor='black')
    ax2.hist(y_pred_proba[y_true == 1], bins=30, alpha=0.6, 
            color='red', label='Class 1 (Sick)', edgecolor='black')
    ax2.axvline(x=0.5, color='green', linestyle='--', linewidth=2, 
               alpha=0.7, label='Threshold')
    ax2.set_xlabel('Predicted Probability', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax2.set_title('Distribution of Predictions by Class', 
                  fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {save_path}")


def plot_training_progress(likelihood_history: list, error_history: list,
                           save_path: str = 'outputs/training_progress.png'):
    """Plot log-likelihood and error over iterations"""
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    iterations = np.arange(len(likelihood_history))
    
    # Plot 1: Log-Likelihood
    ax1 = axes[0]
    ax1.plot(iterations, likelihood_history, 'b-', linewidth=2, label='Log-Likelihood')
    ax1.set_xlabel('Iteration', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Log-Likelihood', fontsize=12, fontweight='bold')
    ax1.set_title('Log-Likelihood Progress During Training\n(Maximizing Objective)', 
                  fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # Add annotations
    max_ll = max(likelihood_history)
    max_idx = likelihood_history.index(max_ll)
    ax1.annotate(f'Max: {max_ll:.2f}', 
                xy=(max_idx, max_ll), 
                xytext=(max_idx + len(likelihood_history)*0.1, max_ll),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=10, fontweight='bold', color='red')
    
    # Plot 2: Mean Squared Error
    ax2 = axes[1]
    ax2.plot(iterations, error_history, 'r-', linewidth=2, label='Mean Squared Error')
    ax2.set_xlabel('Iteration', fontsize=12, fontweight='bold')
    ax2.set_ylabel('MSE', fontsize=12, fontweight='bold')
    ax2.set_title('Mean Squared Error Progress During Training\n(Minimizing Error)', 
                  fontsize=14, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    
    # Add annotations
    min_mse = min(error_history)
    min_idx = error_history.index(min_mse)
    ax2.annotate(f'Min: {min_mse:.6f}', 
                xy=(min_idx, min_mse), 
                xytext=(min_idx + len(error_history)*0.1, min_mse + (max(error_history)-min_mse)*0.1),
                arrowprops=dict(arrowstyle='->', color='green', lw=2),
                fontsize=10, fontweight='bold', color='green')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {save_path}")


def plot_beta_evolution(beta_history: list,
                        save_path: str = 'outputs/beta_evolution.png'):
    """Plot evolution of beta parameters"""
    beta_array = np.array(beta_history)
    n_params = beta_array.shape[1]
    iterations = np.arange(len(beta_history))
    
    plt.figure(figsize=(14, 8))
    
    colors = ['blue', 'red', 'green', 'purple', 'orange']
    labels = ['β0 (Bias)', 'β1', 'β2', 'β3', 'β4']
    
    for i in range(n_params):
        plt.plot(iterations, beta_array[:, i], 
                linewidth=2, label=labels[i] if i < len(labels) else f'β{i}',
                color=colors[i] if i < len(colors) else None)
    
    plt.xlabel('Iteration', fontsize=12, fontweight='bold')
    plt.ylabel('Beta Value', fontsize=12, fontweight='bold')
    plt.title('Evolution of Beta Parameters During Training\nGradient Ascent Optimization', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=11, loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Saved: {save_path}")