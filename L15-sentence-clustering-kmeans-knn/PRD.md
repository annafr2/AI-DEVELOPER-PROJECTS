# Product Requirements Document (PRD)
## Sentence Clustering Analysis System

---

## 1. Executive Summary

### Project Name
Sentence Clustering Analysis: K-Means & KNN Educational Tool

### Version
1.0.0

### Date
November 2025

### Purpose
Educational tool demonstrating unsupervised and supervised machine learning algorithms for text classification, specifically showcasing the relationship between K-Means clustering and K-Nearest Neighbors classification.

### Target Audience
- Students learning machine learning
- Educators teaching NLP and clustering
- Data scientists exploring text classification
- Researchers in semantic analysis

---

## 2. Product Overview

### 2.1 Vision
Create an intuitive, visual learning tool that demystifies how machine learning algorithms process and categorize natural language, highlighting the distinction between human categorization logic and algorithmic pattern discovery.

### 2.2 Objectives

**Primary Objectives:**
1. Demonstrate K-Means unsupervised clustering on sentence data
2. Illustrate supervised learning with KNN
3. Visualize the relationship between clustering and classification
4. Provide clear, educational explanations of algorithm behavior

**Secondary Objectives:**
1. Compare algorithmic categorization with human intuition
2. Reveal semantic patterns in language
3. Show practical applications of Word2Vec embeddings
4. Encourage experimentation and exploration

---

## 3. Functional Requirements

### 3.1 Core Features

#### Feature 1: Text-to-Vector Conversion
**Priority:** Critical
**Description:** Convert natural language sentences into numerical vector representations

**Requirements:**
- FR-1.1: Implement Word2Vec embedding using Gensim library
- FR-1.2: Support training on custom sentence corpus
- FR-1.3: Generate 50-dimensional vectors per sentence
- FR-1.4: Average word vectors to create sentence vectors
- FR-1.5: Handle out-of-vocabulary words gracefully

**Acceptance Criteria:**
- ✅ All sentences converted to numerical vectors
- ✅ Vector dimensionality = 50
- ✅ Vocabulary built from training data
- ✅ No crashes on unknown words

---

#### Feature 2: Vector Normalization
**Priority:** Critical
**Description:** Normalize vectors to unit length for fair distance comparisons

**Requirements:**
- FR-2.1: Apply L2 normalization to all vectors
- FR-2.2: Ensure all normalized vectors have length = 1.0
- FR-2.3: Preserve vector direction (semantic meaning)

**Acceptance Criteria:**
- ✅ All vectors have ||v|| = 1.0 ± 0.001
- ✅ Semantic relationships preserved
- ✅ Distance calculations improved

---

#### Feature 3: K-Means Clustering
**Priority:** Critical
**Description:** Cluster sentences into K=3 groups using K-Means algorithm

**Requirements:**
- FR-3.1: Implement K-Means with K=3 clusters
- FR-3.2: Use scikit-learn KMeans implementation
- FR-3.3: Set random_state for reproducibility
- FR-3.4: Run with n_init=10 for stability
- FR-3.5: Assign each sentence to exactly one cluster

**Acceptance Criteria:**
- ✅ 3 distinct clusters created
- ✅ All sentences assigned to clusters
- ✅ Clustering converges successfully
- ✅ Results reproducible with same random_state

---

#### Feature 4: Clustering Evaluation
**Priority:** High
**Description:** Evaluate K-Means clustering quality against ground truth labels

**Requirements:**
- FR-4.1: Calculate accuracy score
- FR-4.2: Generate confusion matrix
- FR-4.3: Find optimal cluster-to-label mapping
- FR-4.4: Count misclassifications
- FR-4.5: Analyze cluster composition

**Acceptance Criteria:**
- ✅ Accuracy percentage calculated
- ✅ Confusion matrix displays correctly
- ✅ Cluster mapping optimized
- ✅ Detailed analysis provided

---

#### Feature 5: KNN Classification
**Priority:** Critical
**Description:** Train KNN classifier on K-Means labels and classify new sentences

**Requirements:**
- FR-5.1: Implement KNN with K=3 neighbors
- FR-5.2: Train on K-Means cluster labels (not original labels!)
- FR-5.3: Accept 3 test sentences
- FR-5.4: Predict cluster for each test sentence
- FR-5.5: Provide distance-based explanations

**Acceptance Criteria:**
- ✅ KNN trained successfully
- ✅ Test sentences classified
- ✅ Predictions use K-Means labels
- ✅ Neighbor distances computed

---

#### Feature 6: Visualization Suite
**Priority:** High
**Description:** Create comprehensive visualizations of clustering and classification results

**Requirements:**
- FR-6.1: Generate K-Means analysis visualization (4 subplots)
  - Original classification display
  - K-Means classification display
  - Accuracy bar chart
  - Confusion matrix heatmap
  
- FR-6.2: Generate KNN results visualization (4 subplots)
  - Expected classification
  - KNN predictions
  - KNN accuracy chart
  - Summary comparison

- FR-6.3: Use clear colors and labels
- FR-6.4: Include legends and annotations
- FR-6.5: Save as high-resolution PNG files

**Acceptance Criteria:**
- ✅ All visualizations render correctly
- ✅ Images saved at 300 DPI
- ✅ Labels are readable
- ✅ Color schemes are consistent

---

### 3.2 Data Requirements

#### Input Data Specifications

**Training Sentences:**
- Count: 9 sentences
- Categories: 3 (Animals, Airplanes, Cars)
- Distribution: 3 sentences per category
- Language: English
- Format: Python list of strings

**Test Sentences:**
- Count: 3 sentences
- Categories: 1 per category (Animals, Airplanes, Cars)
- Language: English
- Format: Python list of strings

---

## 4. Technical Specifications

### 4.1 Technology Stack

**Programming Language:**
- Python 3.8+

**Core Libraries:**
```python
numpy>=1.21.0          # Numerical operations
matplotlib>=3.5.0      # Visualization
scikit-learn>=1.0.0    # ML algorithms
gensim>=4.0.0          # Word2Vec
seaborn>=0.11.0        # Enhanced visualizations
scipy>=1.7.0           # Optimization
```

---

### 4.2 Algorithms

#### K-Means Clustering
**Algorithm:** Lloyd's Algorithm (1982)
**Parameters:**
- n_clusters = 3
- random_state = 42
- n_init = 10
- max_iter = 300

#### K-Nearest Neighbors
**Algorithm:** KNN Classification
**Parameters:**
- n_neighbors = 3
- weights = 'uniform'
- metric = 'euclidean'

#### Word2Vec
**Algorithm:** Skip-gram with Negative Sampling
**Parameters:**
- vector_size = 50
- window = 5
- min_count = 1
- epochs = 100

---

## 5. Success Metrics

### Educational Effectiveness

**Metric 1: Comprehension**
- Target: Users understand clustering vs. classification
- Measurement: Clear visualizations and explanations

**Metric 2: Technical Performance**
- Target: < 30 seconds total runtime
- Measurement: Time profiling

---

## 6. Future Enhancements

### Phase 2 Features

1. **Interactive Mode** - User inputs custom sentences
2. **Multiple Embeddings** - Support for GloVe, FastText, BERT
3. **Advanced Clustering** - Hierarchical, DBSCAN, GMM
4. **Extended Analysis** - PCA, t-SNE, 3D visualizations
5. **Export Features** - PDF reports, CSV data export

---

## 7. Documentation

### User Documentation
- README.md with comprehensive guide
- Code comments and docstrings
- Example usage

### Technical Documentation
- PRD.md (this document)
- API documentation
- Algorithm specifications

---

## 8. Appendix

### Glossary

**K-Means:** Unsupervised clustering algorithm that partitions data into K clusters

**KNN:** K-Nearest Neighbors, supervised classification algorithm

**Word2Vec:** Neural network model for learning word embeddings

**Embedding:** Dense vector representation of words or sentences

**Normalization:** Scaling vectors to unit length

---

### References

1. Mikolov, T., et al. (2013). "Efficient Estimation of Word Representations in Vector Space"
2. Lloyd, S. (1982). "Least squares quantization in PCM"
3. Cover, T., & Hart, P. (1967). "Nearest neighbor pattern classification"

---

**Document Version:** 1.0.0  
**Last Updated:** November 2025  
**Status:** Approved