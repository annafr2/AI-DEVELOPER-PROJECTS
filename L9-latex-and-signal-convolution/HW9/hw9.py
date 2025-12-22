import numpy as np
import matplotlib.pyplot as plt

# ====================================
# STEP 1: Create sine wave signal (X)
# ====================================

# Parameters
num_cycles = 10          # Number of sine cycles
samples_per_cycle = 200  # Samples in each cycle
total_samples = num_cycles * samples_per_cycle  # Total: 2000 samples

# Create time vector
t = np.linspace(0, num_cycles * 2 * np.pi, total_samples)

# Create sine wave signal
X = np.sin(t)

print(f"Signal X created: {len(X)} samples")
print(f"X shape: {X.shape}")

# ====================================
# STEP 2: Create kernel (single peak)
# ====================================

# Parameters for kernel
kernel_samples = 30  # Number of samples in one peak

# Create one cycle of sine (one peak)
t_kernel = np.linspace(0, 2 * np.pi, kernel_samples)
kernel = np.sin(t_kernel)

print(f"\nKernel created: {len(kernel)} samples")
print(f"Kernel shape: {kernel.shape}")

# ====================================
# STEP 3: Perform convolution
# ====================================

# Convolve the signal with the kernel
# mode='valid' means we only get results where kernel fully overlaps with signal
convolution_result = np.correlate(X, kernel, mode='valid')

print(f"\nConvolution result length: {len(convolution_result)}")
print(f"Convolution result shape: {convolution_result.shape}")

# ====================================
# STEP 4: Find the 10 peaks
# ====================================

# Find indices of 10 maximum values in convolution result
# These correspond to the peak locations
num_peaks = 10
peak_indices = np.argsort(convolution_result)[-num_peaks:]  # Get top 10 indices
peak_indices = np.sort(peak_indices)  # Sort them in ascending order

# Get the convolution values at peak locations
peak_values = convolution_result[peak_indices]

print(f"\n10 Peak locations (indices): {peak_indices}")
print(f"10 Peak values: {peak_values}")

# ====================================
# STEP 5: Visualize results
# ====================================

# Create figure with 3 subplots
fig, axes = plt.subplots(3, 1, figsize=(12, 10))

# Plot 1: Original sine wave signal
axes[0].plot(X, linewidth=0.8)
axes[0].set_title('Original Sine Wave Signal (X) - 10 cycles, 2000 samples', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Sample Index')
axes[0].set_ylabel('Amplitude')
axes[0].grid(True, alpha=0.3)

# Plot 2: Kernel (single peak template)
axes[1].plot(kernel, linewidth=2, color='orange')
axes[1].set_title('Kernel (Single Sine Peak) - 30 samples', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Sample Index')
axes[1].set_ylabel('Amplitude')
axes[1].grid(True, alpha=0.3)

# Plot 3: Convolution result with detected peaks
axes[2].plot(convolution_result, linewidth=0.8, color='green')
axes[2].scatter(peak_indices, peak_values, color='red', s=100, zorder=5, label='Detected Peaks')
axes[2].set_title('Convolution Result (X ★ Kernel) - Peaks Detected', fontsize=12, fontweight='bold')
axes[2].set_xlabel('Index')
axes[2].set_ylabel('Correlation Value (r)')
axes[2].grid(True, alpha=0.3)
axes[2].legend()

# Add vertical lines at peak locations
for peak_idx in peak_indices:
    axes[2].axvline(x=peak_idx, color='red', linestyle='--', alpha=0.3, linewidth=1)

plt.tight_layout()
plt.savefig('sine_convolution_homework.png', dpi=150, bbox_inches='tight')
print("\nGraph saved as: sine_convolution_homework.png")
plt.show()
plt.savefig("convolution_plot.png", dpi=300, bbox_inches="tight")


# ====================================
# STEP 6: Print summary
# ====================================

print("\n" + "="*50)
print("SUMMARY")
print("="*50)
print(f"Signal length: {len(X)} samples")
print(f"Kernel length: {len(kernel)} samples")
print(f"Convolution result length: {len(convolution_result)} samples")
print(f"\nExpected peaks: {num_cycles} (one per sine cycle)")
print(f"Detected peaks: {num_peaks}")
print(f"\nPeak locations (sample indices):")
for i, (idx, val) in enumerate(zip(peak_indices, peak_values)):
    print(f"  Peak {i+1}: Index {idx:4d}, Value {val:8.2f}")

# Calculate expected peak spacing
expected_spacing = samples_per_cycle
actual_spacing = np.diff(peak_indices)
print(f"\nExpected spacing between peaks: ~{expected_spacing} samples")
print(f"Actual spacing between peaks: {actual_spacing}")
print(f"Average spacing: {np.mean(actual_spacing):.1f} samples")