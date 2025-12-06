"""Main script to run and compare both SVM implementations."""
import numpy as np
import matplotlib.pyplot as plt
from svm_sklearn import run_sklearn_svm
from svm_qp import run_qp_svm
from utils import load_iris_data

def create_comparison_plot(acc_sklearn, acc_qp):
    """Create accuracy comparison bar chart."""
    fig, ax = plt.subplots(figsize=(8, 5))
    methods = ['Scikit-learn\nSVM', 'QP Solver\nSVM']
    accuracies = [acc_sklearn * 100, acc_qp * 100]
    colors = ['#3498db', '#e74c3c']
    
    bars = ax.bar(methods, accuracies, color=colors, edgecolor='black', linewidth=2)
    ax.set_ylabel('Accuracy (%)', fontsize=12)
    ax.set_title('SVM Methods Comparison on Iris Dataset', fontsize=14)
    ax.set_ylim(0, 105)
    
    for bar, acc in zip(bars, accuracies):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{acc:.1f}%', ha='center', va='bottom', fontsize=14, fontweight='bold')
    
    ax.axhline(y=90, color='green', linestyle='--', alpha=0.7, label='90% threshold')
    ax.legend()
    plt.tight_layout()
    plt.savefig('comparison.png', dpi=150, bbox_inches='tight')
    plt.close()

def create_data_visualization():
    """Visualize the Iris dataset."""
    X, y, names, features = load_iris_data()
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Iris Dataset Visualization', fontsize=14)
    
    # Plot using petal features (best separation)
    colors = ['blue', 'orange', 'green']
    for i, (name, color) in enumerate(zip(names, colors)):
        mask = y == i
        axes[0].scatter(X[mask, 2], X[mask, 3], c=color, label=name, edgecolors='k', s=60)
    axes[0].set_xlabel('Petal Length (cm)')
    axes[0].set_ylabel('Petal Width (cm)')
    axes[0].set_title('Petal Features - Clear Separation')
    axes[0].legend()
    
    # Plot using sepal features (harder separation)
    for i, (name, color) in enumerate(zip(names, colors)):
        mask = y == i
        axes[1].scatter(X[mask, 0], X[mask, 1], c=color, label=name, edgecolors='k', s=60)
    axes[1].set_xlabel('Sepal Length (cm)')
    axes[1].set_ylabel('Sepal Width (cm)')
    axes[1].set_title('Sepal Features - More Overlap')
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig('iris_data.png', dpi=150, bbox_inches='tight')
    plt.close()

def main():
    """Run both SVM methods and compare results."""
    print("=" * 50)
    print("SVM Classification on Iris Dataset")
    print("=" * 50)
    
    # Visualize data
    print("\n1. Creating data visualization...")
    create_data_visualization()
    print("   Saved: iris_data.png")
    
    # Run sklearn SVM
    print("\n2. Running Scikit-learn SVM...")
    acc_sklearn, _ = run_sklearn_svm()
    print("   Saved: sklearn_svm_results.png")
    
    # Run QP SVM
    print("\n3. Running QP Solver SVM...")
    acc_qp, _ = run_qp_svm()
    print("   Saved: qp_svm_results.png")
    
    # Create comparison
    print("\n4. Creating comparison plot...")
    create_comparison_plot(acc_sklearn, acc_qp)
    print("   Saved: comparison.png")
    
    print("\n" + "=" * 50)
    print("RESULTS SUMMARY")
    print("=" * 50)
    print(f"Scikit-learn SVM Accuracy: {acc_sklearn:.2%}")
    print(f"QP Solver SVM Accuracy:    {acc_qp:.2%}")
    print("=" * 50)

if __name__ == "__main__":
    main()