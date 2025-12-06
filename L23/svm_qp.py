"""SVM implementation using Quadratic Programming (cvxopt)."""
import numpy as np
import matplotlib.pyplot as plt
from cvxopt import matrix, solvers
from sklearn.metrics import accuracy_score
from utils import load_iris_data, prepare_binary_data

solvers.options['show_progress'] = False

class SVM_QP:
    """SVM using Quadratic Programming solver."""
    def __init__(self, C=1.0):
        self.C, self.w, self.b, self.support_vectors = C, None, None, None
    
    def fit(self, X, y):
        """Solve SVM dual problem: max sum(α) - 0.5*Σαi*αj*yi*yj*xi.xj"""
        n, y = X.shape[0], y.astype(float)
        K = np.outer(y, y) * (X @ X.T)
        P, q = matrix(K), matrix(-np.ones(n))
        G = matrix(np.vstack([-np.eye(n), np.eye(n)]))
        h = matrix(np.hstack([np.zeros(n), np.ones(n) * self.C]))
        A, b = matrix(y.reshape(1, -1)), matrix(np.zeros(1))
        
        alphas = np.array(solvers.qp(P, q, G, h, A, b)['x']).flatten()
        sv_mask = alphas > 1e-5
        self.support_vectors = X[sv_mask]
        self.w = np.sum((alphas[sv_mask] * y[sv_mask])[:, np.newaxis] * X[sv_mask], axis=0)
        margin = (alphas > 1e-5) & (alphas < self.C - 1e-5)
        self.b = np.mean(y[margin] - X[margin] @ self.w) if margin.any() else np.mean(y[sv_mask] - X[sv_mask] @ self.w)
    
    def predict(self, X):
        return np.sign(X @ self.w + self.b)

class HierarchicalSVM_QP:
    """Hierarchical SVM classifier using QP solver."""
    def __init__(self, C=1.0):
        self.svm1, self.svm2 = SVM_QP(C), SVM_QP(C)
        self.mean1, self.std1, self.mean2, self.std2 = None, None, None, None
    
    def fit(self, X, y):
        X1, y1 = prepare_binary_data(X, y, [0], [1, 2])
        self.mean1, self.std1 = X1.mean(0), X1.std(0) + 1e-8
        self.svm1.fit((X1 - self.mean1) / self.std1, y1)
        X2, y2 = prepare_binary_data(X, y, [1], [2])
        self.mean2, self.std2 = X2.mean(0), X2.std(0) + 1e-8
        self.svm2.fit((X2 - self.mean2) / self.std2, y2)
    
    def predict(self, X):
        preds = np.zeros(len(X), dtype=int)
        l1 = self.svm1.predict((X - self.mean1) / self.std1)
        preds[l1 == 1] = 0
        mask = l1 == -1
        if mask.any():
            l2 = self.svm2.predict((X[mask] - self.mean2) / self.std2)
            preds[mask] = np.where(l2 == 1, 1, 2)
        return preds

def run_qp_svm():
    """Run QP SVM and generate visualizations."""
    X, y, names, _ = load_iris_data()
    clf = HierarchicalSVM_QP(C=1.0)
    clf.fit(X, y)
    accuracy = accuracy_score(y, clf.predict(X))
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f'QP Solver SVM - Hierarchical Classification\nAccuracy: {accuracy:.2%}', fontsize=14)
    
    X1, y1 = prepare_binary_data(X, y, [0], [1, 2])
    plot_qp_svm((X1 - clf.mean1) / clf.std1, y1, clf.svm1, axes[0], 'Level 1: Setosa vs Others', [2, 3])
    X2, y2 = prepare_binary_data(X, y, [1], [2])
    plot_qp_svm((X2 - clf.mean2) / clf.std2, y2, clf.svm2, axes[1], 'Level 2: Versicolor vs Virginica', [2, 3])
    
    plt.tight_layout()
    plt.savefig('qp_svm_results.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"QP Solver SVM Accuracy: {accuracy:.2%}")
    return accuracy, clf

def plot_qp_svm(X, y, svm, ax, title, feat_idx):
    """Plot decision boundary for QP SVM."""
    f1, f2 = feat_idx
    xx, yy = np.meshgrid(np.linspace(X[:, f1].min()-0.5, X[:, f1].max()+0.5, 200),
                         np.linspace(X[:, f2].min()-0.5, X[:, f2].max()+0.5, 200))
    grid = np.zeros((xx.size, X.shape[1]))
    grid[:, f1], grid[:, f2] = xx.ravel(), yy.ravel()
    Z = (grid @ svm.w + svm.b).reshape(xx.shape)
    ax.contourf(xx, yy, Z, levels=20, alpha=0.4, cmap='RdYlBu')
    ax.contour(xx, yy, Z, levels=[0], colors='black', linewidths=2)
    ax.contour(xx, yy, Z, levels=[-1, 1], colors='gray', linestyles='--')
    ax.scatter(X[:, f1], X[:, f2], c=y, cmap='RdYlBu', edgecolors='k', s=60)
    ax.scatter(svm.support_vectors[:, f1], svm.support_vectors[:, f2], s=150, 
               facecolors='none', edgecolors='green', linewidths=2, label='Support Vectors')
    ax.set_xlabel(f'Feature {f1}'); ax.set_ylabel(f'Feature {f2}')
    ax.set_title(title); ax.legend()

if __name__ == "__main__":
    run_qp_svm()