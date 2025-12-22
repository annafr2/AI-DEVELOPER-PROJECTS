"""
Assignment 16: Sentence Clustering Analysis
K-Means and KNN from scratch - Compact version

Author: Anna
Usage: python main.py
Output: kmeans_analysis.png, knn_results.png (in current directory)
"""

import numpy as np
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
import seaborn as sns
from collections import Counter

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Data
SENTENCES = [
    "The dog runs in the park", "Cats love to sleep all day", "Birds fly high in the sky",
    "The airplane flies above clouds", "Jets travel at high speed", "Pilots control the aircraft carefully",
    "The car drives on the highway", "Vehicles need regular maintenance", "Drivers must follow traffic rules"
]
LABELS = ["Animals"]*3 + ["Airplanes"]*3 + ["Cars"]*3
TEST_SENTENCES = ["The elephant walks slowly", "Boeing planes are very large", "Trucks carry heavy loads"]
TEST_LABELS = ["Animals", "Airplanes", "Cars"]
LABEL_MAP = {"Animals": 0, "Airplanes": 1, "Cars": 2}

# Algorithms
def normalize(vectors):
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1
    return vectors / norms

class KMeans:
    def __init__(self, n_clusters=3, random_state=42, n_init=10, max_iter=300):
        self.n_clusters, self.random_state, self.n_init, self.max_iter = n_clusters, random_state, n_init, max_iter
        self.cluster_centers_ = None

    def fit_predict(self, X):
        rng = np.random.RandomState(self.random_state)
        best_inertia, best_centers, best_labels = np.inf, None, None
        for _ in range(self.n_init):
            centers = X[rng.choice(X.shape[0], self.n_clusters, replace=False)].copy()
            for _ in range(self.max_iter):
                distances = np.array([np.linalg.norm(X - centers[i], axis=1) for i in range(self.n_clusters)]).T
                labels = np.argmin(distances, axis=1)
                new_centers = np.array([X[labels == i].mean(axis=0) if np.any(labels == i) else centers[i] 
                                       for i in range(self.n_clusters)])
                if np.allclose(centers, new_centers): break
                centers = new_centers
            inertia = sum(np.sum((X[labels == i] - centers[i]) ** 2) for i in range(self.n_clusters) if np.any(labels == i))
            if inertia < best_inertia:
                best_inertia, best_centers, best_labels = inertia, centers, labels
        self.cluster_centers_ = best_centers
        return best_labels

class KNN:
    def __init__(self, n_neighbors=3):
        self.n_neighbors = n_neighbors
    def fit(self, X, y):
        self.X_train, self.y_train = X, y
        return self
    def predict(self, X):
        return np.array([Counter(self.y_train[np.argsort(np.linalg.norm(self.X_train - x, axis=1))[:self.n_neighbors]]).most_common(1)[0][0] for x in X])

def train_word2vec(sentences):
    return Word2Vec([s.lower().split() for s in sentences], vector_size=50, window=5, min_count=1, workers=4, epochs=100)

def sentences_to_vectors(sentences, model):
    return np.array([np.mean([model.wv[w] for w in s.lower().split() if w in model.wv], axis=0) if any(w in model.wv for w in s.lower().split()) else np.zeros(model.wv.vector_size) for s in sentences])

def confusion_matrix(y_true, y_pred, n=3):
    m = np.zeros((n, n), dtype=int)
    for t, p in zip(y_true, y_pred): m[t][p] += 1
    return m

def find_mapping(conf_mat):
    used, mapping = set(), {}
    for i in range(len(conf_mat)):
        avail = [j for j in range(len(conf_mat)) if j not in used]
        if avail:
            best = max(avail, key=lambda j: conf_mat[i][j])
            mapping[best], used = i, used | {best}
    return mapping

def plot_kmeans(sentences, true_labels, km_labels, acc, mistakes, conf_mat, label_map):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('K-Means Clustering Analysis - Assignment 16', fontsize=18, fontweight='bold')
    for i, (ax, labels, title) in enumerate([(axes[0,0], true_labels, 'Our Original'), (axes[0,1], km_labels, 'K-Means')]):
        for j, label in enumerate(labels):
            color = plt.cm.Set2(label_map[label] if i == 0 else label)
            ax.scatter(j, 0, s=500, c=[color], alpha=0.7, edgecolors='black', linewidth=2)
            ax.text(j, -0.15, f"S{j+1}", ha='center', fontsize=10, fontweight='bold')
            ax.text(j, 0.15, label if i == 0 else f"Cluster {label}", ha='center', fontsize=8)
        ax.set_xlim(-0.5, 8.5); ax.set_ylim(-0.5, 0.5); ax.set_title(f'{title} Classification', fontsize=14, fontweight='bold')
        ax.set_yticks([]); ax.grid(True, alpha=0.3)
    bars = axes[1,0].bar(['Correct', 'Incorrect'], [9-mistakes, mistakes], color=['#2ecc71', '#e74c3c'], alpha=0.7, edgecolor='black', linewidth=2)
    axes[1,0].set_ylabel('Sentences', fontsize=12); axes[1,0].set_title(f'Accuracy: {acc*100:.1f}%', fontsize=14, fontweight='bold'); axes[1,0].set_ylim(0, 10)
    for bar in bars: axes[1,0].text(bar.get_x() + bar.get_width()/2., bar.get_height(), f'{int(bar.get_height())}/9', ha='center', va='bottom', fontsize=14, fontweight='bold')
    sns.heatmap(conf_mat, annot=True, fmt='d', cmap='YlOrRd', xticklabels=['Animals', 'Airplanes', 'Cars'], yticklabels=['Animals', 'Airplanes', 'Cars'], cbar_kws={'label': 'Count'}, ax=axes[1,1], linewidths=2, linecolor='black')
    axes[1,1].set_title('Confusion Matrix', fontsize=14, fontweight='bold'); axes[1,1].set_xlabel('K-Means Predicted', fontsize=12); axes[1,1].set_ylabel('True Label', fontsize=12)
    plt.tight_layout(); plt.savefig('kmeans_analysis.png', dpi=300, bbox_inches='tight'); plt.close()

def plot_knn(test_sents, test_labels, preds, acc, mistakes, label_map, km_acc):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('KNN Classification Results - Assignment 16', fontsize=18, fontweight='bold')
    for i, (ax, labels, title) in enumerate([(axes[0,0], test_labels, 'Expected'), (axes[0,1], preds, 'KNN Predictions')]):
        for j, label in enumerate(labels):
            color = plt.cm.Set2(label_map[label] if i == 0 else label)
            ax.scatter(j, 0, s=600, c=[color], alpha=0.7, edgecolors='black', linewidth=2)
            ax.text(j, -0.15, f"Test {j+1}", ha='center', fontsize=10, fontweight='bold')
            ax.text(j, 0.15, label if i == 0 else f"Cluster {label}", ha='center', fontsize=9)
        ax.set_xlim(-0.5, 2.5); ax.set_ylim(-0.5, 0.5); ax.set_title(f'{title} Classification', fontsize=14, fontweight='bold'); ax.set_yticks([]); ax.grid(True, alpha=0.3)
    bars = axes[1,0].bar(['Correct', 'Incorrect'], [3-mistakes, mistakes], color=['#3498db', '#e67e22'], alpha=0.7, edgecolor='black', linewidth=2)
    axes[1,0].set_ylabel('Sentences', fontsize=12); axes[1,0].set_title(f'KNN Accuracy: {acc*100:.1f}%', fontsize=14, fontweight='bold'); axes[1,0].set_ylim(0, 4)
    for bar in bars: axes[1,0].text(bar.get_x() + bar.get_width()/2., bar.get_height(), f'{int(bar.get_height())}/3', ha='center', va='bottom', fontsize=14, fontweight='bold')
    axes[1,1].axis('off'); axes[1,1].text(0.5, 0.5, f"\nKNN FOLLOWS K-MEANS!\n\nKey Insight:\n• KNN trained on K-Means labels\n• NOT our original categorization\n\nResults:\n• K-Means: {km_acc:.1f}%\n• KNN: {acc*100:.1f}%\n\nClassification follows:\n{'Our logic' if km_acc >= 80 else 'Different pattern'}", ha='center', va='center', fontsize=12, family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    plt.tight_layout(); plt.savefig('knn_results.png', dpi=300, bbox_inches='tight'); plt.close()

def main():
    print("="*70 + "\nASSIGNMENT 16: SENTENCE CLUSTERING\n" + "="*70)
    print("\n📝 Training Sentences:")
    for i, (s, l) in enumerate(zip(SENTENCES, LABELS)): print(f"{i+1}. [{l:>10}] {s}")
    
    print("\n" + "="*70 + "\nSTEP 1: WORD2VEC\n" + "="*70)
    model = train_word2vec(SENTENCES)
    print(f"✅ Trained! Vocab: {len(model.wv)} words")
    vectors = normalize(sentences_to_vectors(SENTENCES, model))
    print("✅ Vectorized and normalized")
    
    print("\n" + "="*70 + "\nSTEP 2: K-MEANS (K=3)\n" + "="*70)
    kmeans = KMeans()
    km_labels = kmeans.fit_predict(vectors)
    print("✅ Completed!\n\n🔍 Assignments:")
    for i, (s, tl, kl) in enumerate(zip(SENTENCES, LABELS, km_labels)): print(f"{i+1}. Cluster {kl} | True: {tl:>10} | {s}")
    
    print("\n📍 Centroids:")
    for i, c in enumerate(kmeans.cluster_centers_):
        print(f"   Cluster {i}: ||c|| = {np.linalg.norm(c):.4f}, First 5: [{', '.join([f'{x:.3f}' for x in c[:5]])}...]")
    
    print("\n" + "="*70 + "\nSTEP 3: EVALUATE\n" + "="*70)
    true_num = np.array([LABEL_MAP[l] for l in LABELS])
    conf_mat = confusion_matrix(true_num, km_labels)
    mapping = find_mapping(conf_mat)
    acc = np.mean(true_num == np.array([mapping[l] for l in km_labels]))
    mistakes = 9 - int(acc * 9)
    print(f"📊 Accuracy: {acc*100:.1f}% | Correct: {9-mistakes}/9 | Mistakes: {mistakes}/9")
    plot_kmeans(SENTENCES, LABELS, km_labels, acc, mistakes, conf_mat, LABEL_MAP)
    print("✅ Saved: kmeans_analysis.png")
    
    print("\n" + "="*70 + "\nSTEP 4: KNN\n" + "="*70)
    print("\n📝 Test Sentences:")
    for i, (s, l) in enumerate(zip(TEST_SENTENCES, TEST_LABELS)): print(f"{i+1}. {s} (Expected: {l})")
    test_vecs = normalize(sentences_to_vectors(TEST_SENTENCES, model))
    knn = KNN().fit(vectors, km_labels)
    preds = knn.predict(test_vecs)
    print("\n🔍 Predictions:")
    for i, (s, p) in enumerate(zip(TEST_SENTENCES, preds)): print(f"{i+1}. '{s}' → Cluster {p}")
    test_num = np.array([LABEL_MAP[l] for l in TEST_LABELS])
    knn_acc = np.mean(test_num == np.array([mapping[l] for l in preds]))
    knn_mistakes = 3 - int(knn_acc * 3)
    print(f"\n📊 KNN Accuracy: {knn_acc*100:.1f}% | Correct: {3-knn_mistakes}/3 | Mistakes: {knn_mistakes}/3")
    plot_knn(TEST_SENTENCES, TEST_LABELS, preds, knn_acc, knn_mistakes, LABEL_MAP, acc*100)
    print("✅ Saved: knn_results.png")
    
    print("\n" + "="*70 + "\n✨ COMPLETE! Check: kmeans_analysis.png, knn_results.png\n" + "="*70)

if __name__ == "__main__":
    main()