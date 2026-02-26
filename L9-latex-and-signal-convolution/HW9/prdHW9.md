# Sine Wave Peak Detection using Convolution

## Product Requirements Document (PRD)

### Overview
A Python implementation that demonstrates peak detection in periodic signals using convolution/correlation techniques. This is an educational project for understanding signal processing fundamentals.

### Objectives
- Generate a synthetic sine wave signal with multiple cycles
- Create a kernel template representing one peak
- Apply convolution to detect all peak locations
- Visualize the results with clear graphs

### Technical Requirements

#### Input Specifications
- **Signal**: 10 complete sine wave cycles
- **Sampling Rate**: 200 samples per cycle (2000 total samples)
- **Kernel**: Single sine wave peak (30 samples)
- **Peak Detection**: Identify top 10 maximum correlation values

#### Output Specifications
- **Visualization**: 3-panel graph showing:
  1. Original sine wave signal
  2. Kernel template
  3. Convolution result with detected peaks marked
- **Console Output**: Peak locations (indices) and correlation values
- **File Output**: High-resolution PNG graph (150 DPI)

#### Success Criteria
- All 10 peaks correctly identified
- Peak spacing approximately 200 samples apart
- Correlation values show clear distinction at peak locations
- Code runs without errors on standard Python environment

### Dependencies
- Python 3.7+
- NumPy (numerical computing)
- Matplotlib (visualization)

### Use Cases
1. **Educational**: Learn correlation and convolution concepts
2. **Signal Processing**: Template matching in periodic signals
3. **Feature Detection**: Identify repeating patterns in data

---

