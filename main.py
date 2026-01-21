"""
Image Processing with FFT - Main Entry Point
Author: Anna
Course: AI Developer Expert

This is the main script that orchestrates all tasks.
Each task is implemented in a separate module.
"""

import os
import numpy as np
import cv2

# Import task modules
from task1_fft_filtering import run_task1
from task2_edge_detection import run_task2
from task3_hough_transform import run_task3
from utils import create_sample_image

def setup_environment():
    """Create necessary directories"""
    os.makedirs('output', exist_ok=True)
    print("=" * 60)
    print("Image Processing with FFT - Course Assignment")
    print("=" * 60)

def main():
    """Main execution function"""
    setup_environment()
    
    # Task 1: FFT filtering on sample image
    print("\n" + "=" * 60)
    print("TASK 1: FFT Filtering")
    print("=" * 60)
    sample_img = create_sample_image()
    cv2.imwrite('output/original_image.png', sample_img)
    task1_results = run_task1(sample_img)
    
    # Task 2: Synthetic triangle edge detection
    print("\n" + "=" * 60)
    print("TASK 2: Triangle Edge Detection")
    print("=" * 60)
    task2_results = run_task2()
    
    # Task 3: Hough Transform
    print("\n" + "=" * 60)
    print("TASK 3: Hough Transform")
    print("=" * 60)
    run_task3(task2_results)
    
    # Summary
    print("\n" + "=" * 60)
    print("Processing Complete!")
    print("=" * 60)
    print("\nGenerated files in 'output/' directory:")
    print("  - task1_fft_filtering.png - FFT filter comparisons")
    print("  - task1_histograms.png - Histogram analysis")
    print("  - task2_edge_detection.png - Edge detection results")
    print("  - task2_threshold_analysis.png - Threshold comparison")
    print("  - task3_hough_transform.png - Hough line detection")
    print("  - Various individual images")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()