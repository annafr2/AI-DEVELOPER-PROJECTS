"""
Utility functions for printing and logging
"""


def print_header(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(title)
    print("="*70)


def print_training_sentences(sentences, labels):
    """Print training sentences with their labels"""
    print("\n📝 Training Sentences:")
    for i, (sent, label) in enumerate(zip(sentences, labels)):
        print(f"{i+1}. [{label:>10}] {sent}")


def print_word2vec_info(model):
    """Print Word2Vec model information"""
    print(f"✅ Word2Vec model trained successfully!")
    print(f"   - Vocabulary size: {len(model.wv)} words")
    print(f"   - Vector dimensions: {model.wv.vector_size}")


def print_vector_info(vectors):
    """Print vector shape information"""
    print(f"\n📊 Sentence vectors shape: {vectors.shape}")
    print(f"   ({vectors.shape[0]} sentences × {vectors.shape[1]} dimensions)")


def print_kmeans_assignments(sentences, true_labels, kmeans_labels):
    """Print K-Means cluster assignments"""
    print(f"\n🔍 K-Means cluster assignments:")
    for i, (sent, true_label, km_label) in enumerate(zip(sentences, true_labels, kmeans_labels)):
        print(f"{i+1}. Cluster {km_label} | True: {true_label:>10} | {sent}")


def print_kmeans_evaluation(accuracy, mistakes, correct):
    """Print K-Means evaluation metrics"""
    print(f"\n📊 Clustering Accuracy: {accuracy*100:.1f}%")
    print(f"❌ Number of mistakes: {mistakes}/9")
    print(f"✅ Correct classifications: {correct}/9")


def print_cluster_analysis(analysis, sentences, true_labels, kmeans_labels):
    """Print detailed cluster composition analysis"""
    print(f"\n🔬 Cluster Analysis:")
    for cluster_id in range(len(analysis)):
        print(f"\n   Cluster {cluster_id}:")
        for sent in analysis[cluster_id]['sentences']:
            print(f"      - {sent}")
        print(f"   Composition: {analysis[cluster_id]['composition']}")


def print_cluster_centroids(centroids):
    """Print cluster centroids information"""
    print(f"\n📍 Cluster Centroids:")
    for i, centroid in enumerate(centroids):
        centroid_norm = (centroid ** 2).sum() ** 0.5
        print(f"   Cluster {i}: ||centroid|| = {centroid_norm:.4f}")
        print(f"              First 5 dimensions: [{', '.join([f'{x:.3f}' for x in centroid[:5]])}...]")


def print_interpretation(accuracy):
    """Print interpretation of clustering results"""
    print_header("💡 INTERPRETATION")
    
    if accuracy >= 0.8:
        print("✅ K-Means did a GOOD job clustering!")
        print("   The algorithm found patterns similar to our categorization.")
        print("   Sentences with similar semantic meaning were grouped together.")
    elif accuracy >= 0.5:
        print("⚠️  K-Means found a DIFFERENT pattern!")
        print("   The algorithm may have discovered alternative semantic similarities.")
        print("   This could mean it focused on different features than we did.")
    else:
        print("❌ K-Means clustering was POOR compared to our categorization.")
        print("   The algorithm found patterns based on different semantic features.")
    
    print("\n🔍 Possible reasons for K-Means decisions:")
    print("   1. Word similarity: 'fly', 'high', 'sky' might connect airplanes and birds")
    print("   2. Action patterns: 'runs', 'drives', 'flies' indicate movement")
    print("   3. Context words: 'park', 'highway', 'clouds' create different contexts")


def print_test_sentences(test_sentences, test_labels):
    """Print test sentences"""
    print("\n📝 Test Sentences:")
    for i, sent in enumerate(test_sentences):
        print(f"{i+1}. {sent} (Expected: {test_labels[i]})")


def print_knn_predictions(test_sentences, knn_predictions, cluster_sentences):
    """Print KNN predictions with explanation"""
    print("\n🔍 KNN Predictions:")
    for i, (sent, pred_cluster) in enumerate(zip(test_sentences, knn_predictions)):
        cluster_examples = cluster_sentences[pred_cluster]
        print(f"\n{i+1}. '{sent}'")
        print(f"   → Assigned to Cluster {pred_cluster}")
        print(f"   → This cluster contains:")
        for ex in cluster_examples:
            print(f"      • {ex}")


def print_knn_evaluation(accuracy, mistakes, correct):
    """Print KNN evaluation metrics"""
    print(f"\n📊 KNN Accuracy: {accuracy*100:.1f}%")
    print(f"❌ Number of mistakes: {mistakes}/3")
    print(f"✅ Correct classifications: {correct}/3")


def print_knn_detailed_results(test_sentences, test_true_labels, 
                                knn_predictions, cluster_to_label_map,
                                reverse_label_mapping):
    """Print detailed KNN results"""
    print("\n🎯 Detailed Results:")
    for i, (sent, true_label, pred_cluster) in enumerate(
        zip(test_sentences, test_true_labels, knn_predictions)):
        pred_label = reverse_label_mapping[cluster_to_label_map[pred_cluster]]
        status = "✅" if true_label == pred_label else "❌"
        print(f"{status} '{sent}'")
        print(f"   Expected: {true_label} | Predicted: {pred_label}")


def print_final_conclusions(kmeans_accuracy, knn_accuracy):
    """Print final conclusions"""
    print_header("🎓 FINAL CONCLUSIONS")
    
    print("\n1️⃣  K-MEANS CLUSTERING:")
    if kmeans_accuracy >= 0.8:
        print("   ✅ Found patterns matching our categorization")
        print("   ✅ Successfully separated animals, airplanes, and cars")
    else:
        print("   ⚠️  Found different patterns than expected")
        print("   ⚠️  May have focused on linguistic features like:")
        print("      • Verb types (motion verbs: fly, drive, run)")
        print("      • Noun categories (living vs. non-living)")
        print("      • Context words (environment: sky, highway, park)")
    
    print("\n2️⃣  KNN CLASSIFICATION:")
    print("   📌 KNN follows K-MEANS clustering, not our original labels!")
    print("   📌 This is by design - KNN learned from K-Means results")
    if knn_accuracy >= 0.66:
        print("   ✅ Successfully classified new sentences")
        print("   ✅ Consistent with K-Means learned patterns")
    else:
        print("   ⚠️  Some misclassifications occurred")
        print("   ⚠️  Test sentences may have ambiguous features")
    
    print("\n3️⃣  KEY INSIGHTS:")
    print("   💡 Unsupervised learning (K-Means) finds hidden patterns")
    print("   💡 These patterns may differ from human categorization")
    print("   💡 Supervised learning (KNN) then learns these patterns")
    print("   💡 Word embeddings capture semantic similarity")
    
    print("\n" + "="*70)
    print("✨ ANALYSIS COMPLETE!")
    print("="*70)
    print("\n📊 Check the generated visualizations for detailed insights!")
    print("📄 README.md contains full documentation")