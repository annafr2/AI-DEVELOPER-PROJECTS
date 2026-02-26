"""SVM implementation using scikit-learn."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from utils import load_iris_data, prepare_binary_data, scale_data

class HierarchicalSVM_Sklearn:
    """Hierarchical SVM classifier using sklearn."""
    
    def __init__(self, kernel='linear', C=1.0):
        self.svm_level1 = SVC(kernel=kernel, C=C)  # Setosa vs Others
        self.svm_level2 = SVC(kernel=kernel, C=C)  # Versicolor vs Virginica
        self.scaler1 = None
        self.scaler2 = None
    
    def fit(self, X, y):
        """Train hierarchical SVM.
        Level 1: Class 0 (Setosa) vs Classes 1,2 (Others)
        Level 2: Class 1 (Versicolor) vs Class 2 (Virginica)
        """
        # Level 1: Setosa (0) vs Others (1, 2)
        X1, y1 = prepare_binary_data(X, y, [0], [1, 2])
        from sklearn.preprocessing import StandardScaler
        self.scaler1 = StandardScaler().fit(X1)
        X1_scaled = self.scaler1.transform(X1)
        self.svm_level1.fit(X1_scaled, y1)
        
        # Level 2: Versicolor (1) vs Virginica (2) - only non-Setosa
        X2, y2 = prepare_binary_data(X, y, [1], [2])
        self.scaler2 = StandardScaler().fit(X2)
        X2_scaled = self.scaler2.transform(X2)
        self.svm_level2.fit(X2_scaled, y2)
        
    def predict(self, X):
        """Hierarchical prediction."""
        predictions = np.zeros(len(X), dtype=int)
        X1_scaled = self.scaler1.transform(X)
        level1_pred = self.svm_level1.predict(X1_scaled)
        
        # Setosa predicted
        predictions[level1_pred == 1] = 0
        
        # For non-Setosa, use level 2
        non_setosa_mask = level1_pred == -1
        if np.any(non_setosa_mask):
            X2_scaled = self.scaler2.transform(X[non_setosa_mask])
            level2_pred = self.svm_level2.predict(X2_scaled)
            predictions[non_setosa_mask] = np.where(level2_pred == 1, 1, 2)
        return predictions

def run_sklearn_svm():
    """Run sklearn SVM and generate visualizations."""
    X, y, target_names, feature_names = load_iris_data()
    
    # Train hierarchical SVM
    clf = HierarchicalSVM_Sklearn(kernel='linear', C=1.0)
    clf.fit(X, y)
    predictions = clf.predict(X)
    accuracy = accuracy_score(y, predictions)
    
    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f'Scikit-learn SVM - Hierarchical Classification\nAccuracy: {accuracy:.2%}', fontsize=14)
    
    # Plot Level 1: Setosa vs Others (features 2,3 - petal length/width)
    X1, y1 = prepare_binary_data(X, y, [0], [1, 2])
    X1_scaled = clf.scaler1.transform(X1)
    ax = axes[0]
    plot_svm_2d(X1_scaled, y1, clf.svm_level1, ax, 
                'Level 1: Setosa (blue) vs Others (red)', [2, 3])
    
    # Plot Level 2: Versicolor vs Virginica
    X2, y2 = prepare_binary_data(X, y, [1], [2])
    X2_scaled = clf.scaler2.transform(X2)
    ax = axes[1]
    plot_svm_2d(X2_scaled, y2, clf.svm_level2, ax,
                'Level 2: Versicolor (blue) vs Virginica (red)', [2, 3])
    
    plt.tight_layout()
    plt.savefig('sklearn_svm_results.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Sklearn SVM Accuracy: {accuracy:.2%}")
    return accuracy, clf

def plot_svm_2d(X, y, svm, ax, title, feat_idx):
    """Plot 2D decision boundary with support vectors."""
    f1, f2 = feat_idx
    x_min, x_max = X[:, f1].min() - 0.5, X[:, f1].max() + 0.5
    y_min, y_max = X[:, f2].min() - 0.5, X[:, f2].max() + 0.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                         np.linspace(y_min, y_max, 200))
    grid = np.zeros((xx.ravel().shape[0], X.shape[1]))
    grid[:, f1], grid[:, f2] = xx.ravel(), yy.ravel()
    Z = svm.decision_function(grid).reshape(xx.shape)
    
    ax.contourf(xx, yy, Z, levels=np.linspace(Z.min(), Z.max(), 20), alpha=0.4, cmap='RdYlBu')
    ax.contour(xx, yy, Z, levels=[0], colors='black', linewidths=2)
    ax.contour(xx, yy, Z, levels=[-1, 1], colors='gray', linestyles='--', linewidths=1)
    ax.scatter(X[:, f1], X[:, f2], c=y, cmap='RdYlBu', edgecolors='k', s=60)
    sv = svm.support_vectors_
    ax.scatter(sv[:, f1], sv[:, f2], s=150, facecolors='none', edgecolors='green', linewidths=2, label='Support Vectors')
    ax.set_xlabel(f'Feature {f1} (scaled)')
    ax.set_ylabel(f'Feature {f2} (scaled)')
    ax.set_title(title)
    ax.legend()

if __name__ == "__main__":
    run_sklearn_svm()