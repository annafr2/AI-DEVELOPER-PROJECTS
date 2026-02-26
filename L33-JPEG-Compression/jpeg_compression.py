"""
JPEG Image Compression Analysis Tool
Demonstrates JPEG compression at multiple quality levels with metrics and visualizations.
"""

import os
import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

def generate_test_image(width=800, height=600):
    """Generate a synthetic test image with gradients, patterns, and text."""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    pixels = img.load()
    
    # Create gradient background
    for y in range(height):
        for x in range(width):
            r = int(255 * x / width)
            g = int(255 * y / height)
            b = int(128 + 127 * np.sin(x / 50) * np.cos(y / 50))
            pixels[x, y] = (r, g, b)
    
    # Add geometric shapes
    draw.rectangle([50, 50, 200, 200], fill=(255, 0, 0), outline=(255, 255, 255), width=3)
    draw.ellipse([250, 50, 400, 200], fill=(0, 255, 0), outline=(255, 255, 255), width=3)
    draw.polygon([(500, 50), (600, 200), (450, 200)], fill=(0, 0, 255), outline=(255, 255, 255), width=3)
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    draw.text((width//2 - 150, height//2), "JPEG Compression Test", fill=(255, 255, 255), font=font)
    
    # Add fine details (to show compression artifacts)
    for i in range(10, 200, 20):
        draw.line([(50, height-200+i), (300, height-200+i)], fill=(255, 255, 0), width=1)
    
    return img

def compress_jpeg(image, quality):
    """Compress image to JPEG at specified quality and return bytes and decompressed image."""
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG', quality=quality)
    compressed_bytes = buffer.getvalue()
    buffer.seek(0)
    decompressed_image = Image.open(buffer).convert('RGB')
    return compressed_bytes, decompressed_image

def calculate_metrics(original, compressed, original_bytes, compressed_bytes):
    """Calculate compression metrics including MSE and file sizes."""
    orig_array = np.array(original, dtype=np.float32)
    comp_array = np.array(compressed, dtype=np.float32)
    
    # Calculate squared differences (positive values)
    squared_diff = (orig_array - comp_array) ** 2
    
    # Mean Squared Error
    mse = np.mean(squared_diff)
    
    # Compression ratio
    compression_ratio = len(original_bytes) / len(compressed_bytes)
    
    return {
        'original_bytes': len(original_bytes),
        'compressed_bytes': len(compressed_bytes),
        'compression_ratio': compression_ratio,
        'mse': mse,
        'squared_diff': squared_diff
    }

def plot_histogram(squared_diff, quality, output_dir):
    """Generate and save histogram of squared differences."""
    plt.figure(figsize=(10, 6))
    plt.hist(squared_diff.flatten(), bins=100, color='steelblue', edgecolor='black', alpha=0.7)
    plt.title(f'Histogram of Squared Differences (Q={quality})', fontsize=14, fontweight='bold')
    plt.xlabel('Squared Difference (Positive Values)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'histogram_q{quality}.png'), dpi=150)
    plt.close()

def plot_comparisons(results, output_dir):
    """Create comparison charts for file size and MSE vs quality."""
    qualities = sorted(results.keys())
    file_sizes = [results[q]['compressed_bytes'] / 1024 for q in qualities]  # KB
    mses = [results[q]['mse'] for q in qualities]
    
    # File size comparison
    plt.figure(figsize=(10, 6))
    plt.plot(qualities, file_sizes, marker='o', linewidth=2, markersize=8, color='coral')
    plt.title('JPEG Quality vs File Size', fontsize=14, fontweight='bold')
    plt.xlabel('Quality Level', fontsize=12)
    plt.ylabel('File Size (KB)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'comparison_filesize.png'), dpi=150)
    plt.close()
    
    # MSE comparison
    plt.figure(figsize=(10, 6))
    plt.plot(qualities, mses, marker='s', linewidth=2, markersize=8, color='mediumseagreen')
    plt.title('JPEG Quality vs Mean Squared Error', fontsize=14, fontweight='bold')
    plt.xlabel('Quality Level', fontsize=12)
    plt.ylabel('Mean Squared Error (MSE)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'comparison_mse.png'), dpi=150)
    plt.close()

def main():
    """Main execution function."""
    # Create output directory
    output_dir = 'outputs'
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("JPEG Image Compression Analysis Tool")
    print("=" * 60)
    
    # Generate test image
    print("\n[1/4] Generating test image...")
    original_image = generate_test_image()
    original_image.save(os.path.join(output_dir, 'original.png'))
    
    # Get original image bytes (as PNG for fair comparison)
    buffer = io.BytesIO()
    original_image.save(buffer, format='PNG')
    original_bytes = buffer.getvalue()
    print(f"✓ Original image saved (PNG: {len(original_bytes) / 1024:.2f} KB)")
    
    # Quality levels to test
    quality_levels = [10, 30, 50, 70, 90, 95]
    results = {}
    
    # Compress at each quality level
    print(f"\n[2/4] Compressing at {len(quality_levels)} quality levels...")
    for quality in quality_levels:
        compressed_bytes, decompressed_image = compress_jpeg(original_image, quality)
        decompressed_image.save(os.path.join(output_dir, f'image_q{quality}.jpg'))
        
        metrics = calculate_metrics(original_image, decompressed_image, original_bytes, compressed_bytes)
        results[quality] = metrics
        
        print(f"  Q={quality:2d}: {metrics['compressed_bytes']/1024:6.2f} KB | "
              f"Ratio: {metrics['compression_ratio']:5.2f}x | MSE: {metrics['mse']:8.2f}")
    
    # Generate histograms
    print(f"\n[3/4] Generating histograms...")
    for quality in quality_levels:
        plot_histogram(results[quality]['squared_diff'], quality, output_dir)
    print(f"✓ Generated {len(quality_levels)} histograms")
    
    # Generate comparison charts
    print(f"\n[4/4] Creating comparison charts...")
    plot_comparisons(results, output_dir)
    print("✓ Generated comparison charts")
    
    print("\n" + "=" * 60)
    print("Analysis complete! Check the 'outputs' directory for results.")
    print("=" * 60)

if __name__ == '__main__':
    main()
