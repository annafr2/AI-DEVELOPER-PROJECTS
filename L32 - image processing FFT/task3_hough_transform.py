"""
Task 3: Hough Transform Line Detection
Author: Anna

Detects lines in triangle using Hough Transform:
- Canny edge detection preprocessing
- Probabilistic Hough Line Transform
- Triangle reconstruction from detected lines
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt

def apply_canny_edges(edge_image):
    """
    Apply Canny edge detection for cleaner edges
    
    Args:
        edge_image: Edge-detected image from Task 2
    
    Returns:
        edges_canny: Binary edge image
    """
    edges_canny = cv2.Canny(edge_image, 50, 150)
    return edges_canny

def detect_hough_lines(edges_canny):
    """
    Detect lines using Probabilistic Hough Transform
    
    Args:
        edges_canny: Binary edge image
    
    Returns:
        lines: Detected line segments
    """
    lines = cv2.HoughLinesP(
        edges_canny, 
        rho=1,                  # Distance resolution: 1 pixel
        theta=np.pi/180,        # Angle resolution: 1 degree
        threshold=50,           # Minimum votes
        minLineLength=50,       # Minimum line length
        maxLineGap=10           # Maximum gap between segments
    )
    return lines

def draw_lines_on_image(image, lines):
    """
    Draw detected lines on image
    
    Args:
        image: Base image
        lines: Detected lines
    
    Returns:
        line_image: Image with lines drawn
    """
    line_image = cv2.cvtColor(image.copy(), cv2.COLOR_GRAY2BGR)
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    return line_image

def reconstruct_triangle(image_shape, lines):
    """
    Reconstruct triangle from detected lines
    
    Args:
        image_shape: Shape of output image
        lines: Detected lines
    
    Returns:
        reconstruction: Image with only detected lines
    """
    reconstruction = np.zeros(image_shape, dtype=np.uint8)
    reconstruction = cv2.cvtColor(reconstruction, cv2.COLOR_GRAY2BGR)
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(reconstruction, (x1, y1), (x2, y2), 
                    (255, 255, 255), 2)
    
    return reconstruction

def plot_hough_results(triangle, edges_canny, line_image, 
                       reconstruction, num_lines):
    """Visualize Hough Transform results"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    axes[0, 0].imshow(triangle, cmap='gray')
    axes[0, 0].set_title('Original Triangle', fontsize=12)
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(edges_canny, cmap='gray')
    axes[0, 1].set_title('Canny Edge Detection', fontsize=12)
    axes[0, 1].axis('off')
    
    axes[1, 0].imshow(cv2.cvtColor(line_image, cv2.COLOR_BGR2RGB))
    axes[1, 0].set_title(f'Hough Lines Detected: {num_lines}', fontsize=12)
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(cv2.cvtColor(reconstruction, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title('Triangle Reconstruction', fontsize=12)
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('output/task3_hough_transform.png', dpi=300, bbox_inches='tight')
    plt.close()

def run_task3(task2_results):
    """
    Execute Task 3: Hough Transform line detection
    
    Args:
        task2_results: Results from Task 2 (edges and triangle)
    """
    print("Applying Canny edge detection...")
    best_edges = task2_results['threshold_results'][180]
    edges_canny = apply_canny_edges(best_edges)
    
    print("Detecting lines with Hough Transform...")
    lines = detect_hough_lines(edges_canny)
    
    num_lines = len(lines) if lines is not None else 0
    print(f"  → Detected {num_lines} lines")
    
    print("Drawing lines on original triangle...")
    triangle = task2_results['triangle']
    line_image = draw_lines_on_image(triangle, lines)
    cv2.imwrite('output/triangle_hough_lines.png', line_image)
    
    print("Reconstructing triangle from lines...")
    reconstruction = reconstruct_triangle(triangle.shape, lines)
    
    print("Generating visualizations...")
    plot_hough_results(triangle, edges_canny, line_image, 
                      reconstruction, num_lines)
    
    print("✓ Task 3 Complete")
    
    return {
        'lines': lines,
        'num_lines': num_lines,
        'reconstruction': reconstruction
    }