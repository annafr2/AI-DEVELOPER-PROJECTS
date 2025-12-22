"""
Visualization module for clustering and classification results
Creates comprehensive plots and charts
"""

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from collections import Counter


def setup_plot_style(config):
    """Setup matplotlib style for visualizations"""
    plt.style.use(config['style'])
    sns.set_palette("husl")


def create_kmeans_visualization(sentences, true_labels, kmeans_labels, 
                                 accuracy, mistakes, conf_matrix_data,
                                 label_names, label_mapping, output_path):
    """
    Create comprehensive K-Means clustering visualization
    
    Args:
        sentences: List of sentences
        true_labels: Original labels
        kmeans_labels: K-Means cluster assignments
        accuracy: Accuracy score
        mistakes: Number of mistakes
        conf_matrix_data: Confusion matrix
        label_names: List of label names
        label_mapping: Label to number mapping
        output_path: Where to save the plot
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('K-Means Clustering Analysis', fontsize=18, fontweight='bold')
    
    # Plot 1: Our Original Classification
    ax1 = axes[0, 0]
    colors_true = [plt.cm.Set2(label_mapping[label]) for label in true_labels]
    for i, (label, color) in enumerate(zip(true_labels, colors_true)):
        ax1.scatter(i, 0, s=500, c=[color], alpha=0.7, edgecolors='black', linewidth=2)
        ax1.text(i, -0.15, f"S{i+1}", ha='center', fontsize=10, fontweight='bold')
        ax1.text(i, 0.15, label, ha='center', fontsize=8)
    
    ax1.set_xlim(-0.5, 8.5)
    ax1.set_ylim(-0.5, 0.5)
    ax1.set_title('Our Original Classification', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Sentence Number', fontsize=12)
    ax1.set_yticks([])
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: K-Means Classification
    ax2 = axes[0, 1]
    colors_kmeans = [plt.cm.Set2(label) for label in kmeans_labels]
    for i, (km_label, color) in enumerate(zip(kmeans_labels, colors_kmeans)):
        ax2.scatter(i, 0, s=500, c=[color], alpha=0.7, edgecolors='black', linewidth=2)
        ax2.text(i, -0.15, f"S{i+1}", ha='center', fontsize=10, fontweight='bold')
        ax2.text(i, 0.15, f"Cluster {km_label}", ha='center', fontsize=8)
    
    ax2.set_xlim(-0.5, 8.5)
    ax2.set_ylim(-0.5, 0.5)
    ax2.set_title('K-Means Classification', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Sentence Number', fontsize=12)
    ax2.set_yticks([])
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Accuracy Bar Chart
    ax3 = axes[1, 0]
    categories = ['Correct', 'Incorrect']
    values = [9-mistakes, mistakes]
    colors_bar = ['#2ecc71', '#e74c3c']
    bars = ax3.bar(categories, values, color=colors_bar, alpha=0.7, 
                   edgecolor='black', linewidth=2)
    ax3.set_ylabel('Number of Sentences', fontsize=12)
    ax3.set_title(f'Classification Accuracy: {accuracy*100:.1f}%', 
                  fontsize=14, fontweight='bold')
    ax3.set_ylim(0, 10)
    
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}/9', ha='center', va='bottom', 
                fontsize=14, fontweight='bold')
    
    # Plot 4: Confusion Matrix
    ax4 = axes[1, 1]
    sns.heatmap(conf_matrix_data, annot=True, fmt='d', cmap='YlOrRd', 
                xticklabels=label_names, yticklabels=label_names,
                cbar_kws={'label': 'Count'}, ax=ax4, 
                linewidths=2, linecolor='black')
    ax4.set_title('Confusion Matrix', fontsize=14, fontweight='bold')
    ax4.set_xlabel('K-Means Predicted Label', fontsize=12)
    ax4.set_ylabel('True Label', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


def create_knn_visualization(test_sentences, test_true_labels, knn_predictions,
                              knn_accuracy, knn_mistakes, label_mapping,
                              cluster_to_label_map, output_path):
    """
    Create comprehensive KNN classification visualization
    
    Args:
        test_sentences: List of test sentences
        test_true_labels: Expected labels
        knn_predictions: KNN predictions
        knn_accuracy: KNN accuracy score
        knn_mistakes: Number of mistakes
        label_mapping: Label to number mapping
        cluster_to_label_map: Cluster to label mapping
        output_path: Where to save the plot
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('KNN Classification Results', fontsize=18, fontweight='bold')
    
    # Plot 1: Expected Classification
    ax1 = axes[0, 0]
    colors_expected = [plt.cm.Set2(label_mapping[label]) for label in test_true_labels]
    for i, (label, color) in enumerate(zip(test_true_labels, colors_expected)):
        ax1.scatter(i, 0, s=600, c=[color], alpha=0.7, edgecolors='black', linewidth=2)
        ax1.text(i, -0.15, f"Test {i+1}", ha='center', fontsize=10, fontweight='bold')
        ax1.text(i, 0.15, label, ha='center', fontsize=9)
    
    ax1.set_xlim(-0.5, 2.5)
    ax1.set_ylim(-0.5, 0.5)
    ax1.set_title('Expected Classification', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Test Sentence Number', fontsize=12)
    ax1.set_yticks([])
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: KNN Predictions
    ax2 = axes[0, 1]
    colors_knn = [plt.cm.Set2(cluster) for cluster in knn_predictions]
    for i, (cluster, color) in enumerate(zip(knn_predictions, colors_knn)):
        ax2.scatter(i, 0, s=600, c=[color], alpha=0.7, edgecolors='black', linewidth=2)
        ax2.text(i, -0.15, f"Test {i+1}", ha='center', fontsize=10, fontweight='bold')
        ax2.text(i, 0.15, f"Cluster {cluster}", ha='center', fontsize=9)
    
    ax2.set_xlim(-0.5, 2.5)
    ax2.set_ylim(-0.5, 0.5)
    ax2.set_title('KNN Predictions', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Test Sentence Number', fontsize=12)
    ax2.set_yticks([])
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: KNN Accuracy
    ax3 = axes[1, 0]
    categories = ['Correct', 'Incorrect']
    values = [3-knn_mistakes, knn_mistakes]
    colors_bar = ['#3498db', '#e67e22']
    bars = ax3.bar(categories, values, color=colors_bar, alpha=0.7, 
                   edgecolor='black', linewidth=2)
    ax3.set_ylabel('Number of Sentences', fontsize=12)
    ax3.set_title(f'KNN Accuracy: {knn_accuracy*100:.1f}%', 
                  fontsize=14, fontweight='bold')
    ax3.set_ylim(0, 4)
    
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}/3', ha='center', va='bottom', 
                fontsize=14, fontweight='bold')
    
    # Plot 4: Comparison Summary
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    kmeans_acc = 22.2  # From actual results
    summary_text = f"""
KNN FOLLOWS K-MEANS CLUSTERING!

Key Insight:
• KNN was trained on K-Means labels
• KNN learns the pattern K-Means found
• NOT our original categorization

Results:
• K-Means Accuracy: {kmeans_acc:.1f}%
• KNN Accuracy: {knn_accuracy*100:.1f}%

What does this mean?
{"✅ KNN successfully learned K-Means pattern" if knn_accuracy >= 0.66 else "⚠️ KNN struggled with K-Means pattern"}

The classification follows:
{"✅ Our original logic" if kmeans_acc >= 80 else "❌ A different semantic pattern"}
"""
    
    ax4.text(0.5, 0.5, summary_text, ha='center', va='center', 
             fontsize=12, family='monospace',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()