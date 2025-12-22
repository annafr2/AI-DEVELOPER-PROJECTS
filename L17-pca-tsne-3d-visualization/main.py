"""
Assignment 17: 3D Visualization of Sentences using PCA and T-SNE

Demonstrates:
1. PCA implementation from scratch (NumPy only!)
2. T-SNE using sklearn
3. Time measurement for both algorithms
4. 3D visualization of high-dimensional sentence vectors

Author: Anna
Course: AI Developer Course
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import time
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================================================
# DATA - Same sentences from Assignment 16
# ============================================================================

SENTENCES = [
    # Animals
    "The dog runs in the park",
    "Cats love to sleep all day",
    "Birds fly high in the sky",
    # Airplanes
    "The airplane flies above clouds",
    "Jets travel at high speed",
    "Pilots control the aircraft carefully",
    # Cars
    "The car drives on the highway",
    "Vehicles need regular maintenance",
    "Drivers must follow traffic rules"
]

LABELS = ["Animals", "Animals", "Animals", 
          "Airplanes", "Airplanes", "Airplanes",
          "Cars", "Cars", "Cars"]

COLORS = {
    "Animals": "#2ecc71",      # Green
    "Airplanes": "#e74c3c",    # Red
    "Cars": "#3498db"          # Blue
}

# ============================================================================
# PCA IMPLEMENTATION FROM SCRATCH (NumPy only!)
# ============================================================================

class PCA_FromScratch:
    """
    PCA implementation using only NumPy
    
    Steps:
    1. Center the data (subtract mean)
    2. Compute covariance matrix
    3. Find eigenvalues and eigenvectors
    4. Sort by eigenvalues (largest first)
    5. Project data onto top components
    """
    
    def __init__(self, n_components=3):
        self.n_components = n_components
        self.mean = None
        self.components = None
        self.eigenvalues = None
        
    def fit(self, X):
        """
        Fit PCA model
        
        Args:
            X: Data matrix (n_samples, n_features)
        """
        # Step 1: Center the data
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean
        
        # Step 2: Compute covariance matrix
        # Cov = (X^T * X) / (n-1)
        n_samples = X.shape[0]
        cov_matrix = (X_centered.T @ X_centered) / (n_samples - 1)
        
        # Step 3: Compute eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        
        # Step 4: Sort by eigenvalues (descending)
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        # Step 5: Keep top n_components
        self.eigenvalues = eigenvalues[:self.n_components]
        self.components = eigenvectors[:, :self.n_components]
        
        return self
    
    def transform(self, X):
        """
        Project data onto principal components
        
        Args:
            X: Data matrix (n_samples, n_features)
            
        Returns:
            Transformed data (n_samples, n_components)
        """
        X_centered = X - self.mean
        return X_centered @ self.components
    
    def fit_transform(self, X):
        """Fit and transform in one step"""
        self.fit(X)
        return self.transform(X)
    
    def explained_variance_ratio(self):
        """Calculate explained variance ratio"""
        total_variance = np.sum(self.eigenvalues)
        return self.eigenvalues / total_variance

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def train_word2vec(sentences, vector_size=50):
    """Train Word2Vec model"""
    tokenized = [s.lower().split() for s in sentences]
    model = Word2Vec(
        sentences=tokenized,
        vector_size=vector_size,
        window=5,
        min_count=1,
        workers=4,
        epochs=100
    )
    return model

def sentences_to_vectors(sentences, model):
    """Convert sentences to vectors by averaging word vectors"""
    vectors = []
    for sent in sentences:
        words = sent.lower().split()
        word_vecs = [model.wv[w] for w in words if w in model.wv]
        if word_vecs:
            vectors.append(np.mean(word_vecs, axis=0))
        else:
            vectors.append(np.zeros(model.wv.vector_size))
    return np.array(vectors)

def plot_3d(data, labels, title, filename, time_taken=None):
    """
    Create 3D scatter plot
    
    Args:
        data: 3D coordinates (n_samples, 3)
        labels: Category labels
        title: Plot title
        filename: Output filename
        time_taken: Time in seconds (optional)
    """
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot each category
    for label in set(labels):
        mask = [l == label for l in labels]
        points = data[mask]
        ax.scatter(
            points[:, 0], points[:, 1], points[:, 2],
            c=COLORS[label], label=label, s=200, alpha=0.7,
            edgecolors='black', linewidth=2
        )
        
        # Add sentence numbers
        for i, (x, y, z) in enumerate(points):
            idx = [j for j, l in enumerate(labels) if l == label][i]
            ax.text(x, y, z, f'  S{idx+1}', fontsize=9, fontweight='bold')
    
    ax.set_xlabel('Component 1', fontsize=12, fontweight='bold')
    ax.set_ylabel('Component 2', fontsize=12, fontweight='bold')
    ax.set_zlabel('Component 3', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    # Add legend
    ax.legend(loc='upper right', fontsize=11)
    
    # Add time info if provided
    if time_taken is not None:
        time_text = f'⏱️ Computation Time: {time_taken:.4f} seconds'
        fig.text(0.5, 0.02, time_text, ha='center', fontsize=12, 
                fontweight='bold', color='red')
    
    # Adjust view angle for better perspective
    ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {filename}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("="*70)
    print("ASSIGNMENT 17: 3D VISUALIZATION WITH PCA AND T-SNE")
    print("="*70)
    
    # Show data
    print("\n📝 Sentences:")
    for i, (sent, label) in enumerate(zip(SENTENCES, LABELS)):
        print(f"{i+1}. [{label:>10}] {sent}")
    
    # ====================
    # STEP 1: Word2Vec
    # ====================
    print("\n" + "="*70)
    print("STEP 1: WORD2VEC EMBEDDING")
    print("="*70)
    
    print("Training Word2Vec model...")
    model = train_word2vec(SENTENCES, vector_size=50)
    print(f"✅ Model trained!")
    print(f"   Vocabulary: {len(model.wv)} words")
    print(f"   Vector dimensions: {model.wv.vector_size}")
    
    # Convert sentences to vectors
    vectors = sentences_to_vectors(SENTENCES, model)
    print(f"\n📊 Sentence vectors shape: {vectors.shape}")
    print(f"   (9 sentences × 50 dimensions)")
    
    # ====================
    # STEP 2: PCA FROM SCRATCH
    # ====================
    print("\n" + "="*70)
    print("STEP 2: PCA (NumPy Implementation)")
    print("="*70)
    
    print("Applying PCA from scratch...")
    print("Steps:")
    print("  1. Center data (subtract mean)")
    print("  2. Compute covariance matrix")
    print("  3. Find eigenvalues & eigenvectors")
    print("  4. Sort by importance")
    print("  5. Project to 3D")
    
    # Time PCA
    start_time = time.time()
    pca = PCA_FromScratch(n_components=3)
    pca_result = pca.fit_transform(vectors)
    pca_time = time.time() - start_time
    
    print(f"\n⏱️  PCA Time: {pca_time:.4f} seconds")
    print(f"📊 Output shape: {pca_result.shape} (9 sentences × 3 dimensions)")
    
    # Explained variance
    var_ratio = pca.explained_variance_ratio()
    print(f"\n📈 Explained Variance:")
    for i, ratio in enumerate(var_ratio):
        print(f"   Component {i+1}: {ratio*100:.2f}%")
    print(f"   Total: {np.sum(var_ratio)*100:.2f}%")
    
    # Visualize PCA
    print("\n🎨 Creating PCA visualization...")
    plot_3d(
        pca_result, LABELS,
        "PCA: 3D Projection of Sentences (50D → 3D)\nImplemented from Scratch using NumPy",
        "pca_visualization.png",
        pca_time
    )
    
    # ====================
    # STEP 3: T-SNE
    # ====================
    print("\n" + "="*70)
    print("STEP 3: T-SNE (sklearn Implementation)")
    print("="*70)
    
    print("Applying T-SNE...")
    print("Note: T-SNE is computationally intensive!")
    print("Expected: Longer computation time than PCA")
    
    # Time T-SNE
    start_time = time.time()
    # Note: perplexity must be less than n_samples (9)
    # Using perplexity=2 for this small dataset
    tsne = TSNE(n_components=3, random_state=42, perplexity=2, max_iter=1000)
    tsne_result = tsne.fit_transform(vectors)
    tsne_time = time.time() - start_time
    
    print(f"\n⏱️  T-SNE Time: {tsne_time:.4f} seconds")
    print(f"📊 Output shape: {tsne_result.shape} (9 sentences × 3 dimensions)")
    
    # Visualize T-SNE
    print("\n🎨 Creating T-SNE visualization...")
    plot_3d(
        tsne_result, LABELS,
        "T-SNE: 3D Projection of Sentences (50D → 3D)\nUsing sklearn Implementation",
        "tsne_visualization.png",
        tsne_time
    )
    
    # ====================
    # STEP 4: COMPARISON
    # ====================
    print("\n" + "="*70)
    print("STEP 4: TIME COMPARISON")
    print("="*70)
    
    print(f"\n⏱️  PCA Time:   {pca_time:.4f} seconds")
    print(f"⏱️  T-SNE Time: {tsne_time:.4f} seconds")
    print(f"\n📊 Speed Difference: T-SNE is {tsne_time/pca_time:.1f}x SLOWER than PCA")
    
    # Create comparison plot
    print("\n🎨 Creating comparison visualization...")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    methods = ['PCA\n(NumPy)', 'T-SNE\n(sklearn)']
    times = [pca_time, tsne_time]
    colors_bar = ['#2ecc71', '#e74c3c']
    
    bars = ax.bar(methods, times, color=colors_bar, alpha=0.7, 
                  edgecolor='black', linewidth=2)
    
    ax.set_ylabel('Time (seconds)', fontsize=14, fontweight='bold')
    ax.set_title('PCA vs T-SNE: Computation Time Comparison', 
                 fontsize=16, fontweight='bold')
    ax.set_ylim(0, max(times) * 1.2)
    
    # Add value labels
    for bar, time_val in zip(bars, times):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{time_val:.4f}s',
               ha='center', va='bottom', fontsize=14, fontweight='bold')
    
    # Add speed difference annotation
    ax.text(0.5, max(times) * 1.05, 
           f'T-SNE is {tsne_time/pca_time:.1f}x slower',
           ha='center', fontsize=12, color='red', fontweight='bold',
           transform=ax.get_xaxis_transform())
    
    plt.tight_layout()
    plt.savefig('time_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✅ Saved: time_comparison.png")
    
    # ====================
    # FINAL SUMMARY
    # ====================
    print("\n" + "="*70)
    print("✨ ANALYSIS COMPLETE!")
    print("="*70)
    
    print("\n📊 Generated Files:")
    print("   1. pca_visualization.png - PCA 3D projection")
    print("   2. tsne_visualization.png - T-SNE 3D projection")
    print("   3. time_comparison.png - Speed comparison")
    
    print("\n💡 Key Findings:")
    print(f"   • PCA: Fast ({pca_time:.4f}s), linear transformation")
    print(f"   • T-SNE: Slower ({tsne_time:.4f}s), non-linear transformation")
    print(f"   • Both reduce 50D → 3D successfully")
    print(f"   • PCA preserves global structure")
    print(f"   • T-SNE preserves local neighborhoods")
    
    print("\n📄 See README.md for detailed explanations!")

if __name__ == "__main__":
    main()