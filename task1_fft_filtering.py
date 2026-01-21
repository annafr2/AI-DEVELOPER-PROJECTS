"""
Task 1: FFT Filtering
Author: Anna

Implements FFT transformation and three types of filters:
- Low-pass filter (smoothing)
- Band-pass filter (texture isolation)
- High-pass filter (edge detection)
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
from utils import (compute_fft, magnitude_spectrum, 
                   create_low_pass_filter, create_band_pass_filter,
                   create_high_pass_filter, apply_filter_and_ifft)

def plot_filter_results(image, f_shift, filters_data):
    """
    Create comprehensive visualization of all filters
    
    Args:
        image: Original image
        f_shift: FFT of image
        filters_data: Dict with filter results
    """
    fig, axes = plt.subplots(3, 4, figsize=(20, 15))
    
    magnitude = magnitude_spectrum(f_shift)
    
    # Row 1: Low-pass filter
    axes[0, 0].imshow(image, cmap='gray')
    axes[0, 0].set_title('Original Image', fontsize=12)
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(magnitude, cmap='gray')
    axes[0, 1].set_title('FFT Magnitude Spectrum', fontsize=12)
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(filters_data['low_mask'], cmap='gray')
    axes[0, 2].set_title('Low-Pass Filter Mask', fontsize=12)
    axes[0, 2].axis('off')
    
    axes[0, 3].imshow(filters_data['low_result'], cmap='gray')
    axes[0, 3].set_title('Low-Pass Result (Smoothed)', fontsize=12)
    axes[0, 3].axis('off')
    
    # Row 2: Band-pass filter
    axes[1, 0].imshow(image, cmap='gray')
    axes[1, 0].set_title('Original Image', fontsize=12)
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(magnitude_spectrum(filters_data['band_freq']), cmap='gray')
    axes[1, 1].set_title('Band-Pass Spectrum', fontsize=12)
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(filters_data['band_mask'], cmap='gray')
    axes[1, 2].set_title('Band-Pass Filter Mask', fontsize=12)
    axes[1, 2].axis('off')
    
    axes[1, 3].imshow(filters_data['band_result'], cmap='gray')
    axes[1, 3].set_title('Band-Pass Result', fontsize=12)
    axes[1, 3].axis('off')
    
    # Row 3: High-pass filter
    axes[2, 0].imshow(image, cmap='gray')
    axes[2, 0].set_title('Original Image', fontsize=12)
    axes[2, 0].axis('off')
    
    axes[2, 1].imshow(magnitude_spectrum(filters_data['high_freq']), cmap='gray')
    axes[2, 1].set_title('High-Pass Spectrum', fontsize=12)
    axes[2, 1].axis('off')
    
    axes[2, 2].imshow(filters_data['high_mask'], cmap='gray')
    axes[2, 2].set_title('High-Pass Filter Mask', fontsize=12)
    axes[2, 2].axis('off')
    
    axes[2, 3].imshow(filters_data['high_result'], cmap='gray')
    axes[2, 3].set_title('High-Pass Result (Edges)', fontsize=12)
    axes[2, 3].axis('off')
    
    plt.tight_layout()
    plt.savefig('output/task1_fft_filtering.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_histograms(image, low, band, high):
    """Plot histograms for all filtered images"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    axes[0, 0].hist(image.ravel(), bins=256, range=(0, 256), 
                    color='blue', alpha=0.7)
    axes[0, 0].set_title('Original Image Histogram', fontsize=12)
    axes[0, 0].set_xlabel('Pixel Intensity')
    axes[0, 0].set_ylabel('Frequency')
    
    axes[0, 1].hist(low.ravel(), bins=256, color='green', alpha=0.7)
    axes[0, 1].set_title('Low-Pass Filtered Histogram', fontsize=12)
    axes[0, 1].set_xlabel('Pixel Intensity')
    axes[0, 1].set_ylabel('Frequency')
    
    axes[1, 0].hist(band.ravel(), bins=256, color='orange', alpha=0.7)
    axes[1, 0].set_title('Band-Pass Filtered Histogram', fontsize=12)
    axes[1, 0].set_xlabel('Pixel Intensity')
    axes[1, 0].set_ylabel('Frequency')
    
    axes[1, 1].hist(high.ravel(), bins=256, color='red', alpha=0.7)
    axes[1, 1].set_title('High-Pass Filtered Histogram', fontsize=12)
    axes[1, 1].set_xlabel('Pixel Intensity')
    axes[1, 1].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig('output/task1_histograms.png', dpi=300, bbox_inches='tight')
    plt.close()

def run_task1(image):
    """
    Execute Task 1: FFT filtering with three filter types
    
    Args:
        image: Input grayscale image
    
    Returns:
        dict: Results including filtered images
    """
    print("Computing FFT...")
    f_transform, f_shift = compute_fft(image)
    
    print("Creating filters...")
    # Create three types of filters
    low_mask = create_low_pass_filter(image.shape, cutoff_frequency=30)
    high_mask = create_high_pass_filter(image.shape, cutoff_frequency=30)
    band_mask = create_band_pass_filter(image.shape, 
                                        low_cutoff=20, 
                                        high_cutoff=60)
    
    print("Applying filters...")
    # Apply filters and get results
    img_low, f_low = apply_filter_and_ifft(f_shift, low_mask)
    img_high, f_high = apply_filter_and_ifft(f_shift, high_mask)
    img_band, f_band = apply_filter_and_ifft(f_shift, band_mask)
    
    # Prepare data for visualization
    filters_data = {
        'low_mask': low_mask,
        'low_result': img_low,
        'low_freq': f_low,
        'band_mask': band_mask,
        'band_result': img_band,
        'band_freq': f_band,
        'high_mask': high_mask,
        'high_result': img_high,
        'high_freq': f_high
    }
    
    print("Generating visualizations...")
    plot_filter_results(image, f_shift, filters_data)
    plot_histograms(image, img_low, img_band, img_high)
    
    print("✓ Task 1 Complete")
    
    return {
        'original': image,
        'low_pass': img_low,
        'band_pass': img_band,
        'high_pass': img_high
    }