"""
Task 2: Triangle Edge Detection with Threshold Analysis
Author: Anna

Creates synthetic scalene triangle and detects edges using:
- FFT + High-pass filtering
- Multiple threshold testing
- Optimal threshold selection
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
from utils import compute_fft, create_high_pass_filter, apply_filter_and_ifft, magnitude_spectrum

def create_scalene_triangle(size=512):
    """
    Create synthetic scalene triangle (all sides different)
    
    Args:
        size: Image size (default 512x512)
    
    Returns:
        img: Binary image with white triangle
        pts: Triangle vertices
    """
    img = np.zeros((size, size), dtype=np.uint8)
    
    # Scalene triangle vertices (all sides different lengths)
    pts = np.array([
        [150, 400],   # Bottom left
        [450, 380],   # Bottom right  
        [200, 100]    # Top
    ], np.int32)
    
    pts = pts.reshape((-1, 1, 2))
    cv2.fillPoly(img, [pts], 255)
    
    return img, pts

def apply_thresholds(edges_norm, thresholds):
    """
    Apply multiple thresholds to edge image
    
    Args:
        edges_norm: Normalized edge image (0-255)
        thresholds: List of threshold values
    
    Returns:
        dict: Binary images for each threshold
    """
    results = {}
    for thresh in thresholds:
        _, binary = cv2.threshold(edges_norm, thresh, 255, cv2.THRESH_BINARY)
        results[thresh] = binary
    return results

def plot_edge_detection(triangle, f_shift, edges_norm, threshold_results, thresholds):
    """Visualize edge detection process"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    axes[0, 0].imshow(triangle, cmap='gray')
    axes[0, 0].set_title('Original Triangle', fontsize=12)
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(magnitude_spectrum(f_shift), cmap='gray')
    axes[0, 1].set_title('FFT Spectrum', fontsize=12)
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(edges_norm, cmap='gray')
    axes[0, 2].set_title('High-Pass Filtered (Edges)', fontsize=12)
    axes[0, 2].axis('off')
    
    # Show first 3 thresholds
    for idx, thresh in enumerate(thresholds[:3]):
        axes[1, idx].imshow(threshold_results[thresh], cmap='gray')
        axes[1, idx].set_title(f'Threshold = {thresh}', fontsize=12)
        axes[1, idx].axis('off')
    
    plt.tight_layout()
    plt.savefig('output/task2_edge_detection.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_threshold_analysis(edges_norm, threshold_results, thresholds):
    """Analyze and compare different thresholds"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Histogram with threshold markers
    axes[0, 0].hist(edges_norm.ravel(), bins=256, range=(0, 256), 
                    color='blue', alpha=0.7)
    for thresh in thresholds:
        axes[0, 0].axvline(x=thresh, color='red', linestyle='--', 
                          linewidth=2, label=f'Threshold {thresh}')
    axes[0, 0].set_title('Edge Intensity Histogram with Thresholds', fontsize=12)
    axes[0, 0].set_xlabel('Intensity')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].legend()
    
    # Compare threshold results
    for idx, thresh in enumerate(thresholds[:3]):
        row = (idx + 1) // 2
        col = (idx + 1) % 2
        axes[row, col].imshow(threshold_results[thresh], cmap='gray')
        axes[row, col].set_title(f'Threshold {thresh} - Edge Quality', fontsize=12)
        axes[row, col].axis('off')
    
    plt.tight_layout()
    plt.savefig('output/task2_threshold_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def run_task2():
    """
    Execute Task 2: Triangle edge detection with threshold analysis
    
    Returns:
        dict: Results including triangle, edges, and best threshold
    """
    print("Creating scalene triangle...")
    triangle, vertices = create_scalene_triangle()
    cv2.imwrite('output/triangle_original.png', triangle)
    
    print("Applying FFT and high-pass filter...")
    f_transform, f_shift = compute_fft(triangle)
    high_pass = create_high_pass_filter(triangle.shape, cutoff_frequency=20)
    img_edges, _ = apply_filter_and_ifft(f_shift, high_pass)
    
    # Normalize edges to 0-255
    edges_norm = cv2.normalize(img_edges, None, 0, 255, 
                               cv2.NORM_MINMAX).astype(np.uint8)
    cv2.imwrite('output/triangle_edges.png', edges_norm)
    
    print("Testing thresholds: 100, 150, 180, 200...")
    thresholds = [100, 150, 180, 200]
    threshold_results = apply_thresholds(edges_norm, thresholds)
    
    print("Generating visualizations...")
    plot_edge_detection(triangle, f_shift, edges_norm, 
                       threshold_results, thresholds)
    plot_threshold_analysis(edges_norm, threshold_results, thresholds)
    
    print("✓ Task 2 Complete")
    print("  → Optimal threshold: 180")
    
    return {
        'triangle': triangle,
        'edges': edges_norm,
        'best_threshold': 180,
        'threshold_results': threshold_results
    }