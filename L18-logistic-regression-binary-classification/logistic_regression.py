"""
Logistic Regression with Gradient Descent
Binary classification using sigmoid and log-likelihood optimization
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import Tuple, List

np.random.seed(42)
plt.style.use('seaborn-v0_8-darkgrid')


class LogisticRegression:
    """Logistic Regression classifier using gradient ascent"""
    
    def __init__(self, learning_rate: float = 0.01, n_iterations: int = 1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.beta = None
        self.likelihood_history = []
        self.error_history = []
        self.beta_history = []
        
    def sigmoid(self, z: np.ndarray) -> np.ndarray:
        """Sigmoid activation function"""
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))
    
    def log_likelihood(self, X: np.ndarray, y: np.ndarray, beta: np.ndarray) -> float:
        """Calculate log-likelihood"""
        z = np.clip(X @ beta, -500, 500)
        ll = np.sum(y * z - np.log(1 + np.exp(z)))
        return ll
    
    def gradient(self, X: np.ndarray, y: np.ndarray, beta: np.ndarray) -> np.ndarray:
        """Calculate gradient of log-likelihood"""
        z = X @ beta
        predictions = self.sigmoid(z)
        grad = X.T @ (y - predictions)
        return grad
    
    def mean_squared_error(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Calculate mean squared error"""
        return np.mean((y_true - y_pred) ** 2)
    
    def fit(self, X: np.ndarray, y: np.ndarray, verbose: bool = True) -> None:
        """Train model using gradient ascent"""
        n_samples, n_features = X.shape
        
        # Initialize beta randomly
        self.beta = np.random.randn(n_features) * 0.01
        
        if verbose:
            print(f"{'='*70}")
            print(f"{'Starting Logistic Regression Training':^70}")
            print(f"{'='*70}\n")
        
        for iteration in range(self.n_iterations):
            # Predictions
            z = X @ self.beta
            predictions = self.sigmoid(z)
            
            # Metrics
            ll = self.log_likelihood(X, y, self.beta)
            mse = self.mean_squared_error(y, predictions)
            
            # Store history
            self.likelihood_history.append(ll)
            self.error_history.append(mse)
            self.beta_history.append(self.beta.copy())
            
            # Update beta
            grad = self.gradient(X, y, self.beta)
            self.beta += self.learning_rate * grad
            
            # Print progress
            if verbose and (iteration % 100 == 0 or iteration == self.n_iterations - 1):
                print(f"Iteration {iteration:4d} | Log-Likelihood: {ll:10.4f} | MSE: {mse:.6f}")
                print(f"  Beta: [{', '.join([f'{b:.4f}' for b in self.beta])}]")
                print(f"  {'-'*68}")
        
        if verbose:
            print(f"\n{'='*70}")
            print(f"{'Training Completed Successfully!':^70}")
            print(f"{'='*70}\n")
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict probabilities"""
        z = X @ self.beta
        return self.sigmoid(z)
    
    def predict(self, X: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        """Predict binary labels"""
        probabilities = self.predict_proba(X)
        return (probabilities >= threshold).astype(int)


def generate_synthetic_data(n_samples: int = 200, 
                           separation: float = 2.0) -> Tuple[np.ndarray, np.ndarray]:
    """Generate synthetic binary classification dataset"""
    
    # Group 0: Healthy (centered around [0.3, 0.3])
    X0 = np.random.randn(n_samples, 2) * 0.15 + np.array([0.3, 0.3])
    y0 = np.zeros(n_samples)
    
    # Group 1: Sick (centered around [0.7, 0.7])
    X1 = np.random.randn(n_samples, 2) * 0.15 + np.array([0.7, 0.7])
    y1 = np.ones(n_samples)
    
    # Combine
    X = np.vstack([X0, X1])
    y = np.hstack([y0, y1])
    
    # Normalize to [0, 1]
    X = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0) + 1e-10)
    
    # Add bias term
    X_with_bias = np.column_stack([np.ones(len(X)), X])
    
    # Shuffle
    indices = np.random.permutation(len(X))
    X_with_bias = X_with_bias[indices]
    y = y[indices]
    
    return X_with_bias, y


def create_results_table(X: np.ndarray, y_true: np.ndarray, 
                        y_pred_proba: np.ndarray) -> pd.DataFrame:
    """Create detailed results table"""
    df = pd.DataFrame({
        'X0 (Bias)': X[:, 0],
        'X1': X[:, 1],
        'X2': X[:, 2],
        'True Label (y)': y_true.astype(int),
        'Prediction (Sigmoid)': y_pred_proba,
        'Binary Prediction': (y_pred_proba >= 0.5).astype(int),
        'Absolute Error': np.abs(y_true - y_pred_proba)
    })
    return df


def print_summary_statistics(df: pd.DataFrame):
    """Print summary statistics"""
    print(f"\n{'='*70}")
    print(f"{'Summary Statistics':^70}")
    print(f"{'='*70}\n")
    
    accuracy = np.mean(df['True Label (y)'] == df['Binary Prediction'])
    mean_error = df['Absolute Error'].mean()
    
    print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Mean Absolute Error: {mean_error:.6f}")
    print(f"\nSample from table (first 20 rows):")
    print(df.head(20).to_string(index=True))