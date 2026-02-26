## README

### Installation

```bash
# Install required packages
pip install numpy matplotlib
```

### Usage

```bash
# Run the script
python sine_convolution_homework.py
```

### What It Does

1. **Generates Signal**: Creates a sine wave with 10 cycles (2000 samples)
2. **Creates Kernel**: Single sine peak template (30 samples)
3. **Performs Convolution**: Slides kernel across signal to find matches
4. **Detects Peaks**: Identifies 10 locations with highest correlation
5. **Visualizes Results**: Displays 3 graphs and saves as PNG

### Output

#### Console Output
```
Signal X created: 2000 samples
Kernel created: 30 samples
Convolution result length: 1971 samples

10 Peak locations (indices): [...]
Peak values: [...]
```

#### Graph Output
File: `sine_convolution_homework.png`
- Top: Original sine wave
- Middle: Kernel template
- Bottom: Convolution result with red dots marking detected peaks

### Key Concepts

**Convolution**: A mathematical operation that "slides" a template (kernel) across a signal to find matches. High correlation values indicate good matches.

**Why It Works**: When the kernel aligns with a peak in the signal, the correlation value is maximum. This allows automatic peak detection.

### Parameters You Can Modify

```python
num_cycles = 10          # Number of sine cycles
samples_per_cycle = 200  # Samples per cycle
kernel_samples = 30      # Kernel size
num_peaks = 10           # Number of peaks to detect
```

### Expected Results

- **Peak Spacing**: ~200 samples (one cycle length)
- **Number of Peaks**: 10 (one per cycle)
- **Correlation Values**: High values (>20) at peak locations

### Troubleshooting

| Issue | Solution |
|-------|----------|
| No graph displays | Check if `plt.show()` works, try saving file only |
| Wrong peak count | Adjust `kernel_samples` or check signal generation |
| Import errors | Install dependencies: `pip install numpy matplotlib` |

### License
MIT License - Free for educational use

### Author
AI Expert Dev Course - Homework Assignment

### Version
1.0.0

---

## Quick Start Example

```python
import numpy as np
import matplotlib.pyplot as plt

# Create signal
X = np.sin(np.linspace(0, 20*np.pi, 2000))

# Create kernel
kernel = np.sin(np.linspace(0, 2*np.pi, 30))

# Find peaks
result = np.correlate(X, kernel, mode='valid')
peaks = np.argsort(result)[-10:]

# Plot
plt.plot(result)
plt.scatter(peaks, result[peaks], color='red')
plt.show()
```

---

## Further Reading

- [NumPy Correlation Documentation](https://numpy.org/doc/stable/reference/generated/numpy.correlate.html)
- [Convolution Explained](https://en.wikipedia.org/wiki/Convolution)
- [Signal Processing Basics](https://en.wikipedia.org/wiki/Signal_processing)