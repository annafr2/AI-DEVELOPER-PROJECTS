"""
Utility Functions for FFT Image Processing
Author: Anna

This module contains common utility functions used across all tasks:
- FFT/IFFT operations
- Filter creation
- Sample image generation
"""

import numpy as np
import cv2

def create_sample_image():
    """Create a sample image for demonstration"""
    img = np.zeros((512, 512), dtype=np.uint8)
    # Add geometric shapes
    cv2.rectangle(img, (100, 100), (400, 400), 255, -1)
    cv2.circle(img, (256, 256), 80, 128, -1)
    cv2.line(img, (50, 50), (450, 450), 200, 5)
    return img

def compute_fft(image):
    """
    Compute FFT and shift zero frequency to center
    
    Args:
        image: Grayscale image (numpy array)
    
    Returns:
        f_transform: FFT of image
        f_shift: Shifted FFT (zero frequency at center)
    """
    f_transform = np.fft.fft2(image)
    f_shift = np.fft.fftshift(f_transform)
    return f_transform, f_shift

def magnitude_spectrum(f_shift):
    """
    Compute magnitude spectrum for visualization
    
    Args:
        f_shift: Shifted FFT
    
    Returns:
        magnitude_scaled: Scaled magnitude for display
    """
    magnitude = np.abs(f_shift)
    # Scale for better visualization (logarithmic)
    magnitude_scaled = 20 * np.log(magnitude + 1)
    return magnitude_scaled

def create_low_pass_filter(shape, cutoff_frequency):
    """
    Create low-pass filter (circular mask)
    Keeps low frequencies - smooths image
    
    Args:
        shape: Image shape (rows, cols)
        cutoff_frequency: Radius in pixels
    
    Returns:
        mask: Binary mask for filtering
    """
    rows, cols = shape
    crow, ccol = rows // 2, cols // 2
    
    mask = np.zeros((rows, cols), np.uint8)
    r = cutoff_frequency
    center = [crow, ccol]
    x, y = np.ogrid[:rows, :cols]
    mask_area = (x - center[0])**2 + (y - center[1])**2 <= r*r
    mask[mask_area] = 1
    
    return mask

def create_high_pass_filter(shape, cutoff_frequency):
    """
    Create high-pass filter (inverted circular mask)
    Keeps high frequencies - enhances edges
    
    Args:
        shape: Image shape (rows, cols)
        cutoff_frequency: Radius in pixels
    
    Returns:
        mask: Binary mask for filtering
    """
    rows, cols = shape
    crow, ccol = rows // 2, cols // 2
    
    mask = np.ones((rows, cols), np.uint8)
    r = cutoff_frequency
    center = [crow, ccol]
    x, y = np.ogrid[:rows, :cols]
    mask_area = (x - center[0])**2 + (y - center[1])**2 <= r*r
    mask[mask_area] = 0
    
    return mask

def create_band_pass_filter(shape, low_cutoff, high_cutoff):
    """
    Create band-pass filter (ring mask)
    Keeps middle frequencies - isolates textures
    
    Args:
        shape: Image shape (rows, cols)
        low_cutoff: Inner radius in pixels
        high_cutoff: Outer radius in pixels
    
    Returns:
        mask: Binary mask for filtering
    """
    rows, cols = shape
    crow, ccol = rows // 2, cols // 2
    
    mask = np.zeros((rows, cols), np.uint8)
    center = [crow, ccol]
    x, y = np.ogrid[:rows, :cols]
    
    # Create ring between low and high cutoff
    distances = (x - center[0])**2 + (y - center[1])**2
    mask_area = (distances >= low_cutoff**2) & (distances <= high_cutoff**2)
    mask[mask_area] = 1
    
    return mask

def apply_filter_and_ifft(f_shift, mask):
    """
    Apply filter mask and perform inverse FFT
    
    Args:
        f_shift: Shifted FFT
        mask: Filter mask
    
    Returns:
        img_back: Filtered image (spatial domain)
        f_shift_filtered: Filtered frequency domain
    """
    f_shift_filtered = f_shift * mask
    f_ishift = np.fft.ifftshift(f_shift_filtered)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    return img_back, f_shift_filtered