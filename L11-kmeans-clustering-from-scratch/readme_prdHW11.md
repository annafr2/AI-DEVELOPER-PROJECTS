# K-means Clustering with Overlapping Data


---

## PRD (Product Requirements Document)

### Project Overview
Create a demonstration of K-means clustering algorithm limitations when dealing with overlapping data clusters. The assignment requires generating synthetic data with intentional overlap to illustrate how K-means handles ambiguous cluster boundaries.

### Objectives
1. Generate 6,000 2D data points organized into 3 clusters
2. Ensure exactly 1/3 of the data points are shared across all 3 clusters
3. Use Gaussian (Normal) distribution based on mean and variance parameters
4. Implement K-means algorithm from scratch (no sklearn)
5. Visualize the original data, K-means results, and comparison

### Technical Requirements

#### Data Generation Specifications
- **Total Points**: 6,000 samples
- **Number of Clusters**: 3
- **Points per Cluster**: 2,000
- **Overlap Requirement**: 1/3 (33.33%) of all points must belong to all 3 clusters simultaneously
- **Distribution**: Gaussian (Normal) distribution
- **Dimensions**: 2D (x, y coordinates)

#### Point Distribution Breakdown
- **Unique Points per Cluster**: 1,333 points (66.67% of each cluster)
- **Shared Points**: 2,001 points (33.33% of total, shared across all 3 clusters)
- **Total Records**: 12,003 (because shared points appear 3 times in the dataset)

#### Implementation Requirements
- **Language**: Python
- **Dependencies**: numpy, matplotlib only (no sklearn)
- **K-means Implementation**: Custom implementation required
- **Visualization**: 3 side-by-side plots showing original labels, K-means results, and comparison

#### Success Criteria
- Clear visualization of overlapping regions
- Demonstration of K-means limitation with overlapping data
- Accurate statistics and metrics reporting
- Reproducible results (using random seed)

---

## README

### What We Built

This assignment demonstrates a fundamental limitation of K-means clustering: its inability to handle overlapping clusters where data points legitimately belong to multiple clusters simultaneously.

### The Challenge

Traditional clustering algorithms like K-means assume **hard assignment** - each point belongs to exactly one cluster. However, in real-world scenarios, data often has ambiguous boundaries where points could reasonably belong to multiple categories.

### Our Approach

#### Step 1: Understanding the Requirements
The assignment asked for:
- 6,000 total data points
- 3 distinct clusters
- **1/3 of points shared across ALL 3 clusters** (this was the tricky part!)

#### Step 2: Data Generation Strategy

We created the overlap by:

1. **Unique Points (66.67% per cluster)**:
   - Generated 1,333 unique points for each cluster
   - Each cluster centered at a different location: [0,0], [5,5], [10,0]
   - Used Gaussian distribution with std=1.0 for tight clustering

2. **Shared Points (33.33% total)**:
   - Generated 2,001 points at the geometric center of all 3 clusters
   - Used larger std=2.5 to create wider spread
   - **Key innovation**: Added these same 2,001 points to ALL 3 clusters
   - This creates 6,003 total records (3,999 unique + 2,001 appearing 3x each)

#### Step 3: K-means Implementation

We implemented K-means from scratch with these steps:

1. **Initialization**: Randomly select k points as initial cluster centers
2. **Assignment**: Calculate distance from each point to each center, assign to nearest
3. **Update**: Recalculate centers as mean of assigned points
4. **Convergence**: Repeat until centers stop moving (or max iterations reached)
5. **Metrics**: Calculate inertia (sum of squared distances to centers)

#### Step 4: Visualization

Created three plots:

**Left Plot - Original True Labels**:
- Shows the ground truth with color-coded clusters
- The massive central overlap region is visible
- 2,001 points appear in all 3 colors (overlapping)
- Red X markers show true cluster centers

**Middle Plot - K-means Results**:
- Shows how K-means segments the data
- Forces hard assignment - each point gets exactly one label
- The overlap region is arbitrarily divided
- Red X markers show discovered centers

**Right Plot - Comparison**:
- Blue X markers: Original cluster centers
- Red circles: K-means discovered centers
- Shows how close K-means came to finding true centers
- Demonstrates the algorithm's reasonable performance despite limitations

### Key Insights

#### What Worked Well
- K-means successfully identified approximately correct cluster centers
- The algorithm converged quickly (typically 10-20 iterations)
- Clear visualization of the overlap problem

#### What K-means Struggled With
- **Cannot handle soft clustering**: Must assign each point to exactly one cluster
- **Arbitrary decisions in overlap regions**: Points that should belong to multiple clusters get forced into one
- **Ignores the true data structure**: The 2,001 shared points are split artificially

#### Why This Matters
This demonstration shows that:
1. K-means works best with **well-separated, spherical clusters**
2. Real-world data often has **ambiguous boundaries**
3. Alternative algorithms (Fuzzy C-means, Gaussian Mixture Models) can handle overlapping clusters better
4. Understanding algorithm limitations is crucial for choosing the right tool

### How to Interpret the Results

When you run the code, you'll see:

**Console Output**:
```
=== Data Planning ===
Unique points per cluster: 1333
Shared points across all 3 clusters: 2001
Total points: 6000

=== Running K-means ===
K-means converged after X iterations

=== K-means Statistics ===
Inertia: XXXX.XX
Cluster sizes and centers...
```

**Visual Output**:
- A saved image file: `kmeans_overlap_output.png`
- Three subplots showing the progression from true labels → K-means results → comparison

### Parameters You Can Adjust

```python
# Cluster center positions
centers = np.array([
    [0, 0],      # Cluster 1
    [5, 5],      # Cluster 2
    [10, 0]      # Cluster 3
])

# Standard deviations
std_unique = 1.0   # Smaller = tighter clusters
std_shared = 2.5   # Larger = more spread in overlap region
```

### Technical Implementation Details

#### Why We Added Points 3 Times
To create true overlap where points belong to multiple clusters, we added the shared points to the dataset three times - once labeled for each cluster. This way:
- Each shared point has 3 entries in the dataset
- Each entry has a different label (0, 1, or 2)
- This simulates multi-label classification in a single-label framework

#### Why We Used Different Standard Deviations
- **std_unique = 1.0**: Keeps cluster-specific points close to their centers
- **std_shared = 2.5**: Creates wider spread for ambiguous points
- This difference makes the overlap visually clear and realistic

#### Convergence Criteria
K-means stops when:
- Centers move less than 1e-6 (very small threshold)
- OR maximum iterations (100) reached
- This ensures reliable convergence

### Expected Results
img attached

**What You Should See**:
1. **Left**: Colorful overlap in the center with 3 distinct outer regions
2. **Middle**: Clean segmentation by K-means with clear boundaries
3. **Right**: Both center markers close together, showing K-means found approximate locations

### Conclusion

This assignment successfully demonstrates:
- ✅ Generation of overlapping clusters using Gaussian distributions
- ✅ Implementation of K-means from scratch
- ✅ Visualization of algorithm limitations
- ✅ Understanding of when K-means is appropriate vs. when it struggles

The 1/3 overlap requirement was achieved by having 2,001 out of 6,000 unique points appear in all three clusters simultaneously, creating a realistic scenario where hard clustering algorithms like K-means face inherent limitations.

---

## Assignment Completion Checklist

- [x] 6,000 total data points generated
- [x] 3 clusters created
- [x] 1/3 overlap implemented (2,001 shared points)
- [x] Gaussian distribution with mean and variance
- [x] 2D coordinate system
- [x] Custom K-means implementation (no sklearn)
- [x] Three visualization plots
- [x] Statistics and metrics calculated
- [x] Output image saved
- [x] Reproducible results (seed=42)
- [x] Clear documentation

---

**Course**: AI DEV EXPERT  
**Topic**: Clustering & K-means Algorithm  
**Date**: 2025