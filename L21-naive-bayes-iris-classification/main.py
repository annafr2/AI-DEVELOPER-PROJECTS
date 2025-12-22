"""
Homework 21: Naive Bayes Classification on Iris Dataset
Compare NumPy (from scratch) vs scikit-learn implementations
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.datasets import load_iris
import os
import time

# Create outputs folder
os.makedirs('outputs', exist_ok=True)

# Load Iris dataset from sklearn
print("Loading Iris dataset...")
iris = load_iris()
X = iris.data
y = iris.target_names[iris.target]  # Convert to class names

print("Dataset loaded successfully!")
print(f"\nDataset shape: {X.shape}")
print(f"Number of samples: {len(X)}")
print(f"Classes: {np.unique(y)}")
print(f"Features: {iris.feature_names}")

# Split data: 75% train, 25% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}")


# ============================================
# NUMPY IMPLEMENTATION (From Scratch)
# ============================================

class NaiveBayesNumPy:
    """Naive Bayes classifier implemented from scratch using NumPy"""
    
    def __init__(self):
        self.classes = None
        self.class_priors = {}
        self.means = {}
        self.stds = {}
    
    def fit(self, X, y):
        """Train the model by calculating means and stds for each feature per class"""
        self.classes = np.unique(y)
        
        for cls in self.classes:
            # Get samples for this class
            X_cls = X[y == cls]
            
            # Calculate prior probability: P(class)
            self.class_priors[cls] = len(X_cls) / len(X)
            
            # Calculate mean and std for each feature
            self.means[cls] = np.mean(X_cls, axis=0)
            self.stds[cls] = np.std(X_cls, axis=0) + 1e-6  # Add small value to avoid division by zero
    
    def _gaussian_probability(self, x, mean, std):
        """Calculate Gaussian probability density"""
        exponent = np.exp(-((x - mean) ** 2) / (2 * std ** 2))
        return (1 / (np.sqrt(2 * np.pi) * std)) * exponent
    
    def predict_single(self, x):
        """Predict class for a single sample using Bayes theorem"""
        posteriors = {}
        
        for cls in self.classes:
            # Start with prior probability
            posterior = np.log(self.class_priors[cls])
            
            # Multiply by likelihood for each feature (use log to avoid underflow)
            for i in range(len(x)):
                likelihood = self._gaussian_probability(
                    x[i], self.means[cls][i], self.stds[cls][i]
                )
                posterior += np.log(likelihood + 1e-10)
            
            posteriors[cls] = posterior
        
        # Return class with highest posterior probability
        return max(posteriors, key=posteriors.get)
    
    def predict(self, X):
        """Predict classes for multiple samples"""
        return np.array([self.predict_single(x) for x in X])


# Train NumPy implementation
print("\n" + "="*50)
print("NUMPY IMPLEMENTATION (From Scratch)")
print("="*50)

nb_numpy = NaiveBayesNumPy()

# Measure training time
start_time = time.time()
nb_numpy.fit(X_train, y_train)
train_time_numpy = time.time() - start_time

# Measure prediction time
start_time = time.time()
y_pred_numpy = nb_numpy.predict(X_test)
predict_time_numpy = time.time() - start_time

accuracy_numpy = accuracy_score(y_test, y_pred_numpy)
print(f"Accuracy: {accuracy_numpy:.4f} ({accuracy_numpy*100:.2f}%)")
print(f"Training time: {train_time_numpy*1000:.4f} ms")
print(f"Prediction time: {predict_time_numpy*1000:.4f} ms")
print(f"Total time: {(train_time_numpy + predict_time_numpy)*1000:.4f} ms")


# ============================================
# SCIKIT-LEARN IMPLEMENTATION
# ============================================

print("\n" + "="*50)
print("SCIKIT-LEARN IMPLEMENTATION")
print("="*50)

nb_sklearn = GaussianNB()

# Measure training time
start_time = time.time()
nb_sklearn.fit(X_train, y_train)
train_time_sklearn = time.time() - start_time

# Measure prediction time
start_time = time.time()
y_pred_sklearn = nb_sklearn.predict(X_test)
predict_time_sklearn = time.time() - start_time

accuracy_sklearn = accuracy_score(y_test, y_pred_sklearn)
print(f"Accuracy: {accuracy_sklearn:.4f} ({accuracy_sklearn*100:.2f}%)")
print(f"Training time: {train_time_sklearn*1000:.4f} ms")
print(f"Prediction time: {predict_time_sklearn*1000:.4f} ms")
print(f"Total time: {(train_time_sklearn + predict_time_sklearn)*1000:.4f} ms")


# ============================================
# COMPARISON
# ============================================

print("\n" + "="*50)
print("COMPARISON")
print("="*50)
print(f"NumPy Accuracy:    {accuracy_numpy*100:.2f}%")
print(f"Sklearn Accuracy:  {accuracy_sklearn*100:.2f}%")
print(f"Difference:        {abs(accuracy_numpy - accuracy_sklearn)*100:.2f}%")

# Compare predictions
differences = np.sum(y_pred_numpy != y_pred_sklearn)
print(f"\nPredictions that differ: {differences} out of {len(y_test)}")

# Performance comparison
print("\n" + "-"*50)
print("PERFORMANCE COMPARISON")
print("-"*50)
print(f"NumPy Training Time:    {train_time_numpy*1000:.4f} ms")
print(f"Sklearn Training Time:  {train_time_sklearn*1000:.4f} ms")
speedup_train = train_time_numpy / train_time_sklearn if train_time_sklearn > 0 else 0
print(f"Speedup (training):     {speedup_train:.2f}x {'(sklearn faster)' if speedup_train > 1 else '(numpy faster)'}")

print(f"\nNumPy Prediction Time:  {predict_time_numpy*1000:.4f} ms")
print(f"Sklearn Prediction Time:{predict_time_sklearn*1000:.4f} ms")
speedup_predict = predict_time_numpy / predict_time_sklearn if predict_time_sklearn > 0 else 0
print(f"Speedup (prediction):   {speedup_predict:.2f}x {'(sklearn faster)' if speedup_predict > 1 else '(numpy faster)'}")

total_numpy = train_time_numpy + predict_time_numpy
total_sklearn = train_time_sklearn + predict_time_sklearn
speedup_total = total_numpy / total_sklearn if total_sklearn > 0 else 0
print(f"\nTotal NumPy Time:       {total_numpy*1000:.4f} ms")
print(f"Total Sklearn Time:     {total_sklearn*1000:.4f} ms")
print(f"Overall Speedup:        {speedup_total:.2f}x {'(sklearn faster)' if speedup_total > 1 else '(numpy faster)'}")


# ============================================
# VISUALIZATIONS
# ============================================

# 1. Feature Distributions
print("\nCreating visualizations...")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
feature_names = ['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width']

for idx, (ax, feature_name) in enumerate(zip(axes.flatten(), feature_names)):
    for cls in nb_numpy.classes:
        data = X_train[y_train == cls, idx]
        ax.hist(data, alpha=0.6, label=cls, bins=15)
    
    ax.set_xlabel(feature_name, fontsize=11)
    ax.set_ylabel('Frequency', fontsize=11)
    ax.set_title(f'{feature_name} Distribution by Class', fontsize=12, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/feature_distributions.png', dpi=300, bbox_inches='tight')
print("[OK] Saved: outputs/feature_distributions.png")

# 2. Confusion Matrix - NumPy
plt.figure(figsize=(8, 6))
cm_numpy = confusion_matrix(y_test, y_pred_numpy, labels=nb_numpy.classes)
sns.heatmap(cm_numpy, annot=True, fmt='d', cmap='Blues', 
            xticklabels=nb_numpy.classes, yticklabels=nb_numpy.classes)
plt.title('Confusion Matrix - NumPy Implementation', fontsize=14, fontweight='bold')
plt.ylabel('True Label', fontsize=11)
plt.xlabel('Predicted Label', fontsize=11)
plt.tight_layout()
plt.savefig('outputs/confusion_matrix_numpy.png', dpi=300, bbox_inches='tight')
print("[OK] Saved: outputs/confusion_matrix_numpy.png")

# 3. Confusion Matrix - Sklearn
plt.figure(figsize=(8, 6))
cm_sklearn = confusion_matrix(y_test, y_pred_sklearn, labels=nb_numpy.classes)
sns.heatmap(cm_sklearn, annot=True, fmt='d', cmap='Greens',
            xticklabels=nb_numpy.classes, yticklabels=nb_numpy.classes)
plt.title('Confusion Matrix - Scikit-learn Implementation', fontsize=14, fontweight='bold')
plt.ylabel('True Label', fontsize=11)
plt.xlabel('Predicted Label', fontsize=11)
plt.tight_layout()
plt.savefig('outputs/confusion_matrix_sklearn.png', dpi=300, bbox_inches='tight')
print("[OK] Saved: outputs/confusion_matrix_sklearn.png")

# 4. Accuracy Comparison
plt.figure(figsize=(10, 6))
implementations = ['NumPy\n(From Scratch)', 'Scikit-learn']
accuracies = [accuracy_numpy * 100, accuracy_sklearn * 100]
colors = ['#3498db', '#2ecc71']

bars = plt.bar(implementations, accuracies, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
plt.ylabel('Accuracy (%)', fontsize=12)
plt.title('Naive Bayes Accuracy Comparison', fontsize=14, fontweight='bold')
plt.ylim([0, 105])

# Add value labels on bars
for bar, acc in zip(bars, accuracies):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 1,
             f'{acc:.2f}%', ha='center', va='bottom', fontsize=13, fontweight='bold')

plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('outputs/accuracy_comparison.png', dpi=300, bbox_inches='tight')
print("[OK] Saved: outputs/accuracy_comparison.png")

print("\n" + "="*50)
print("All tasks completed successfully!")
print("="*50)