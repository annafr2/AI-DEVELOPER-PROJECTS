"""Utility functions for SVM Iris classification project."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_iris_data():
    """Load Iris dataset and return features, labels, and names."""
    iris = load_iris()
    return iris.data, iris.target, iris.target_names, iris.feature_names

def prepare_binary_data(X, y, positive_classes, negative_classes):
    """Prepare data for binary classification.
    Args:
        X: Features array
        y: Labels array  
        positive_classes: List of class indices for positive class (label=1)
        negative_classes: List of class indices for negative class (label=-1)
    Returns: X_binary, y_binary (with labels -1 and 1)
    """
    pos_mask = np.isin(y, positive_classes)
    neg_mask = np.isin(y, negative_classes)
    mask = pos_mask | neg_mask
    X_bin = X[mask]
    y_bin = np.where(pos_mask[mask], 1, -1)
    return X_bin, y_bin

def plot_decision_boundary(X, y, clf, title, ax, feature_idx=(0, 1)):
    """Plot decision boundary for 2D features."""
    f1, f2 = feature_idx
    x_min, x_max = X[:, f1].min() - 0.5, X[:, f1].max() + 0.5
    y_min, y_max = X[:, f2].min() - 0.5, X[:, f2].max() + 0.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                         np.linspace(y_min, y_max, 200))
    # Create full feature array with zeros for unused features
    grid_points = np.zeros((xx.ravel().shape[0], X.shape[1]))
    grid_points[:, f1] = xx.ravel()
    grid_points[:, f2] = yy.ravel()
    Z = clf.predict(grid_points).reshape(xx.shape)
    
    ax.contourf(xx, yy, Z, alpha=0.3, cmap='RdYlBu')
    ax.contour(xx, yy, Z, colors='k', linewidths=0.5)
    scatter = ax.scatter(X[:, f1], X[:, f2], c=y, cmap='RdYlBu', edgecolors='black', s=50)
    ax.set_xlabel(f'Feature {f1}')
    ax.set_ylabel(f'Feature {f2}')
    ax.set_title(title)
    return scatter

def scale_data(X_train, X_test):
    """Scale features using StandardScaler."""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler