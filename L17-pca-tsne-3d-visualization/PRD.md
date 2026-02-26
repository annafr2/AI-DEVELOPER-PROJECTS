# Product Requirements Document (PRD)
# Assignment 17: 3D Visualization with PCA and T-SNE

---

## 📋 Project Overview

**Project Name:** 3D Sentence Visualization  
**Assignment:** 17  
**Student:** Anna  
**Course:** AI Developer Course  
**Date:** November 2025

---

## 🎯 Objectives

### Primary Goal
Visualize high-dimensional sentence vectors in 3D space using two dimensionality reduction techniques:
1. **PCA** (Principal Component Analysis) - implemented from scratch
2. **T-SNE** (t-SNE) - using sklearn library

### Learning Goals
- Understand dimensionality reduction
- Compare linear (PCA) vs non-linear (T-SNE) methods
- Measure computational performance
- Visualize high-dimensional data

---

## 📊 Dataset

### Source
Same sentences from Assignment 16:
- **9 sentences** total
- **3 categories:** Animals, Airplanes, Cars
- **3 sentences per category**

---

## 🔧 Technical Requirements

### 1. Word Embeddings
- **Method:** Word2Vec (Gensim)
- **Vector Size:** 50 dimensions
- **Output:** 9 vectors × 50 dimensions

### 2. PCA Implementation
- **Must:** Implement from scratch using NumPy only
- **No sklearn PCA allowed**
- **Components:** Reduce to 3 dimensions

### 3. T-SNE Implementation
- **Allowed:** Use sklearn.manifold.TSNE
- **Components:** 3 dimensions

### 4. Time Measurement
- Measure execution time for both
- Show T-SNE is slower than PCA

### 5. Visualization
- 3D scatter plots
- Color-coded by category
- High-resolution PNG (300 DPI)

---

## 📁 Deliverables

### Code Files
1. main.py
2. requirements.txt
3. setup.sh / setup.bat

### Documentation
1. README.md - Comprehensive guide
2. PRD.md - This file
3. TASKS.md - Task breakdown

### Output Files
1. pca_visualization.png
2. tsne_visualization.png
3. time_comparison.png

---

## 🎯 Success Criteria

✅ PCA from scratch (no sklearn)  
✅ T-SNE uses sklearn  
✅ Time measurement working  
✅ 3D visualizations generated  
✅ Documentation complete  
✅ English comments  

---

## 📊 Expected Results

### PCA
- Time: ~0.001-0.1 seconds (fast)
- Linear projection

### T-SNE
- Time: ~0.5-2 seconds (slower)
- 20-50x slower than PCA

### Why Separation Isn't Perfect
1. Only 9 sentences (too few)
2. Similar content (all about motion)
3. 50D is relatively small

---

**Status:** ✅ Complete  
**Version:** 1.0