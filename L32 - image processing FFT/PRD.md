# Product Requirements Document (PRD)
## Image Processing with FFT - Educational Assignment

---

## Document Information

| Field | Value |
|-------|-------|
| **Project Name** | Image Processing with FFT |
| **Document Type** | Product Requirements Document |
| **Version** | 1.0 |
| **Date** | January 2026 |
| **Author** | Anna |
| **Status** | ✅ Approved for Implementation |
| **Course** | AI Developer Expert |

---

## 1. Executive Summary

### 1.1 Purpose
Educational project demonstrating fundamental image processing techniques in the frequency domain using Fast Fourier Transform (FFT). This assignment fulfills course requirements for the Image Processing module.

### 1.2 Scope
Implementation of FFT-based filters, edge detection, and line detection algorithms with comprehensive visualization and analysis.

### 1.3 Objectives
- ✅ Understand frequency domain representation
- ✅ Implement three types of frequency filters
- ✅ Perform edge detection on synthetic shapes
- ✅ Apply Hough Transform for line detection
- ✅ Generate comprehensive visualizations and documentation

---

## 2. Stakeholders

| Role | Name/Group | Responsibility |
|------|------------|----------------|
| **Student** | Anna | Implementation, testing, documentation |
| **Instructor** | Course Staff | Requirements definition, evaluation |
| **Peer Reviewers** | Classmates | Feedback and validation |
| **End Users** | Future students | Learning from documentation |

---

## 3. Product Overview

### 3.1 Product Description
A Python-based image processing application that demonstrates:
- FFT transformation and filtering
- Frequency domain manipulation
- Edge detection techniques
- Shape reconstruction using Hough Transform

### 3.2 Target Audience
- Computer Science students learning image processing
- AI/ML practitioners exploring computer vision
- Educators teaching signal processing concepts

### 3.3 Use Cases

#### UC-1: Apply Frequency Filters
**Actor:** Student/Researcher  
**Goal:** Filter image in frequency domain  
**Steps:**
1. Load grayscale image
2. Apply FFT transformation
3. Select filter type (low/band/high-pass)
4. Apply filter and inverse FFT
5. View results and histograms

#### UC-2: Detect Edges in Synthetic Shape
**Actor:** Student  
**Goal:** Find optimal threshold for edge detection  
**Steps:**
1. Generate synthetic triangle
2. Apply high-pass FFT filter
3. Test multiple thresholds
4. Compare results
5. Select optimal threshold

#### UC-3: Reconstruct Shape with Hough Transform
**Actor:** Researcher  
**Goal:** Detect lines in image  
**Steps:**
1. Input edge-detected image
2. Apply Hough Transform
3. Extract line parameters
4. Visualize detected lines
5. Reconstruct shape

---

## 4. Functional Requirements

### 4.1 Core Features

#### FR-1: FFT Transformation
**Priority:** P0 (Critical)  
**Description:** Transform images between spatial and frequency domains

**Requirements:**
- FR-1.1: Implement 2D FFT using NumPy
- FR-1.2: Shift zero frequency to center
- FR-1.3: Compute magnitude spectrum
- FR-1.4: Implement inverse FFT (IFFT)
- FR-1.5: Handle grayscale images (512x512 or similar)

**Acceptance Criteria:**
- ✅ FFT produces complex frequency representation
- ✅ Magnitude spectrum visible and interpretable
- ✅ IFFT reconstructs original image accurately
- ✅ No data loss in transformation cycle

---

#### FR-2: Low-Pass Filter
**Priority:** P0 (Critical)  
**Description:** Remove high frequencies to smooth image

**Requirements:**
- FR-2.1: Create circular mask in frequency domain
- FR-2.2: Configurable cutoff radius (default: 30 pixels)
- FR-2.3: Apply mask to shifted FFT
- FR-2.4: Transform back to spatial domain

**Acceptance Criteria:**
- ✅ Resulting image is smoothed/blurred
- ✅ High-frequency noise removed
- ✅ Low-frequency content preserved
- ✅ Histogram shows reduced variation

---

#### FR-3: Band-Pass Filter
**Priority:** P0 (Critical)  
**Description:** Isolate middle-range frequencies

**Requirements:**
- FR-3.1: Create ring-shaped mask
- FR-3.2: Define inner and outer radii (default: 20-60 pixels)
- FR-3.3: Apply band-pass filtering
- FR-3.4: Visualize mid-frequency content

**Acceptance Criteria:**
- ✅ Only mid-range frequencies retained
- ✅ Both low and high frequencies removed
- ✅ Texture/pattern information isolated
- ✅ Distinct from low-pass and high-pass results

---

#### FR-4: High-Pass Filter
**Priority:** P0 (Critical)  
**Description:** Extract edges and fine details

**Requirements:**
- FR-4.1: Create inverted circular mask
- FR-4.2: Configurable cutoff radius (default: 30 pixels)
- FR-4.3: Emphasize high frequencies
- FR-4.4: Generate edge-like output

**Acceptance Criteria:**
- ✅ Edges clearly visible
- ✅ Smooth regions suppressed
- ✅ Suitable for edge detection
- ✅ Histogram concentrated near zero

---

#### FR-5: Synthetic Triangle Generation
**Priority:** P0 (Critical)  
**Description:** Create test image with scalene triangle

**Requirements:**
- FR-5.1: Generate 512x512 black background
- FR-5.2: Draw white scalene triangle (all sides different)
- FR-5.3: Triangle must be filled
- FR-5.4: High contrast (0 and 255 values only)

**Acceptance Criteria:**
- ✅ All three sides have different lengths
- ✅ Clean binary image (no anti-aliasing)
- ✅ Triangle clearly visible
- ✅ Suitable for edge detection

---

#### FR-6: Threshold-Based Edge Detection
**Priority:** P0 (Critical)  
**Description:** Find optimal threshold for edge extraction

**Requirements:**
- FR-6.1: Apply high-pass filter to triangle
- FR-6.2: Normalize edge intensities to 0-255
- FR-6.3: Test thresholds: 100, 150, 180, 200
- FR-6.4: Compare quality of results
- FR-6.5: Identify optimal threshold

**Acceptance Criteria:**
- ✅ All thresholds tested and visualized
- ✅ Clear comparison available
- ✅ Optimal threshold documented (expected: ~180)
- ✅ Triangle edges cleanly extracted

---

#### FR-7: Hough Transform Line Detection
**Priority:** P0 (Critical)  
**Description:** Detect and reconstruct triangle using Hough Transform

**Requirements:**
- FR-7.1: Apply Canny edge detection preprocessing
- FR-7.2: Implement Probabilistic Hough Line Transform
- FR-7.3: Configure parameters (threshold, min length, max gap)
- FR-7.4: Draw detected lines on original image
- FR-7.5: Reconstruct triangle from detected lines

**Acceptance Criteria:**
- ✅ Triangle sides detected as lines
- ✅ 3-6 lines typically detected
- ✅ Lines accurately follow triangle edges
- ✅ Reconstruction visually similar to original
- ✅ Parameters documented

---

#### FR-8: Visualization and Plotting
**Priority:** P0 (Critical)  
**Description:** Generate comprehensive visual outputs

**Requirements:**
- FR-8.1: Multi-panel comparison plots
- FR-8.2: Histogram visualizations
- FR-8.3: Filter mask visualizations
- FR-8.4: Before/after comparisons
- FR-8.5: High-resolution output (300 DPI)
- FR-8.6: Proper titles and labels

**Acceptance Criteria:**
- ✅ All tasks have visualization
- ✅ Images clear and readable
- ✅ Proper labeling and titles
- ✅ Saved to output directory
- ✅ Suitable for report inclusion

---

### 4.2 Documentation Requirements

#### FR-9: Code Documentation
**Priority:** P1 (High)  

**Requirements:**
- FR-9.1: Function docstrings
- FR-9.2: Inline comments for complex operations
- FR-9.3: Parameter descriptions
- FR-9.4: Usage examples

#### FR-10: README Documentation
**Priority:** P0 (Critical)  

**Requirements:**
- FR-10.1: Installation instructions
- FR-10.2: Theoretical background explanations
- FR-10.3: Task descriptions and results
- FR-10.4: Visualizations embedded
- FR-10.5: Key findings and conclusions

#### FR-11: PRD Document
**Priority:** P1 (High)  

**Requirements:**
- FR-11.1: Complete requirements specification
- FR-11.2: Use cases and scenarios
- FR-11.3: Acceptance criteria
- FR-11.4: Technical specifications

#### FR-12: Tasks Document
**Priority:** P1 (High)  

**Requirements:**
- FR-12.1: Detailed task breakdown
- FR-12.2: Implementation checklist
- FR-12.3: Testing checklist
- FR-12.4: Completion status

---

## 5. Non-Functional Requirements

### 5.1 Performance

| Requirement | Target | Priority |
|-------------|--------|----------|
| **NFR-1.1** Image loading time | < 1 second | P2 |
| **NFR-1.2** FFT computation | < 2 seconds (512x512) | P1 |
| **NFR-1.3** Filter application | < 1 second | P1 |
| **NFR-1.4** Total execution time | < 30 seconds | P2 |
| **NFR-1.5** Memory usage | < 2 GB RAM | P2 |

### 5.2 Usability

| Requirement | Description | Priority |
|-------------|-------------|----------|
| **NFR-2.1** Simple execution | Single command to run | P0 |
| **NFR-2.2** Clear outputs | Organized file structure | P1 |
| **NFR-2.3** Error messages | Informative error handling | P2 |
| **NFR-2.4** Progress indicators | Console output for stages | P2 |

### 5.3 Reliability

| Requirement | Target | Priority |
|-------------|--------|----------|
| **NFR-3.1** Deterministic results | Same input → same output | P0 |
| **NFR-3.2** Numerical stability | No overflow/underflow | P1 |
| **NFR-3.3** Error handling | Graceful failure | P2 |

### 5.4 Maintainability

| Requirement | Description | Priority |
|-------------|-------------|----------|
| **NFR-4.1** Code structure | Modular functions | P1 |
| **NFR-4.2** Naming conventions | Clear, descriptive names | P1 |
| **NFR-4.3** Documentation | Comprehensive comments | P0 |
| **NFR-4.4** Version control | Git-friendly structure | P2 |

### 5.5 Portability

| Requirement | Description | Priority |
|-------------|-------------|----------|
| **NFR-5.1** Python version | 3.8+ compatible | P0 |
| **NFR-5.2** OS compatibility | Windows, macOS, Linux | P1 |
| **NFR-5.3** Dependencies | Common libraries only | P1 |
| **NFR-5.4** Package management | pip installable | P1 |

---

## 6. Technical Specifications

### 6.1 Technology Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Language** | Python | 3.8+ | Core implementation |
| **FFT Library** | NumPy | 1.20+ | FFT operations |
| **Image Processing** | OpenCV (cv2) | 4.x | Image I/O, filters |
| **Visualization** | Matplotlib | 3.x | Plotting, graphs |
| **Scientific** | SciPy | 1.7+ | Additional processing |

### 6.2 Data Specifications

#### Image Format
- **Type:** Grayscale (single channel)
- **Bit depth:** 8-bit (0-255 values)
- **Dimensions:** 512x512 pixels (preferred)
- **Format:** NumPy array, dtype=uint8

#### Frequency Domain
- **Type:** Complex128 (64-bit real + 64-bit imaginary)
- **Dimensions:** Same as input image
- **Zero frequency:** Centered after fftshift

### 6.3 Filter Specifications

#### Low-Pass Filter
```python
{
    "type": "circular",
    "radius": 30,  # pixels from center
    "shape": (512, 512),
    "pass": "low_frequencies"
}
```

#### Band-Pass Filter
```python
{
    "type": "ring",
    "inner_radius": 20,
    "outer_radius": 60,
    "shape": (512, 512),
    "pass": "mid_frequencies"
}
```

#### High-Pass Filter
```python
{
    "type": "inverted_circular",
    "radius": 30,
    "shape": (512, 512),
    "pass": "high_frequencies"
}
```

### 6.4 Hough Transform Parameters

```python
{
    "rho": 1,              # Distance resolution (pixels)
    "theta": np.pi/180,    # Angle resolution (radians)
    "threshold": 50,       # Minimum votes
    "minLineLength": 50,   # Minimum line length (pixels)
    "maxLineGap": 10       # Maximum gap in line (pixels)
}
```

---

## 7. Constraints and Assumptions

### 7.1 Constraints

| ID | Constraint | Impact |
|----|------------|--------|
| **C-1** | Educational context | Focus on clarity over optimization |
| **C-2** | Time limit | 1-2 weeks for completion |
| **C-3** | No external data | Use synthetic/sample images |
| **C-4** | Standard libraries | No proprietary tools |

### 7.2 Assumptions

| ID | Assumption | Risk if Invalid |
|----|------------|-----------------|
| **A-1** | Python 3.8+ available | Code won't run |
| **A-2** | Libraries installable via pip | Setup issues |
| **A-3** | 2GB RAM minimum | Performance degradation |
| **A-4** | Display available | Visualization issues |

---

## 8. Dependencies

### 8.1 External Dependencies

```python
# requirements.txt
numpy>=1.20.0
opencv-python>=4.5.0
matplotlib>=3.3.0
scipy>=1.7.0
```

### 8.2 Internal Dependencies

**Module Structure:**
```
image_fft_processing.py (main)
├── FFT functions
│   ├── compute_fft()
│   ├── magnitude_spectrum()
│   └── apply_filter_and_ifft()
├── Filter functions
│   ├── create_low_pass_filter()
│   ├── create_band_pass_filter()
│   └── create_high_pass_filter()
├── Task 1: task1_fft_filtering()
├── Task 2: detect_edges_with_threshold()
├── Task 3: detect_lines_hough()
└── Visualization: plot_*()
```

---

## 9. Testing Requirements

### 9.1 Unit Testing

| Test ID | Test Case | Expected Result |
|---------|-----------|-----------------|
| **UT-1** | FFT → IFFT cycle | Recover original image |
| **UT-2** | Filter mask creation | Correct shape and values |
| **UT-3** | Threshold application | Binary output |
| **UT-4** | Hough line count | 3-10 lines for triangle |

### 9.2 Integration Testing

| Test ID | Test Case | Expected Result |
|---------|-----------|-----------------|
| **IT-1** | End-to-end Task 1 | 3 filtered images |
| **IT-2** | End-to-end Task 2 | Edge detection with threshold |
| **IT-3** | End-to-end Task 3 | Lines detected and visualized |
| **IT-4** | All tasks together | All outputs generated |

### 9.3 Acceptance Testing

| Test ID | Criteria | Status |
|---------|----------|--------|
| **AT-1** | All visualizations generated | ✅ Pass |
| **AT-2** | README complete and clear | ✅ Pass |
| **AT-3** | Code documented | ✅ Pass |
| **AT-4** | Results match expectations | ✅ Pass |

---

## 10. Deliverables

### 10.1 Code Deliverables

- [x] `image_fft_processing.py` - Main implementation
- [x] `requirements.txt` - Dependencies
- [x] Comments and docstrings

### 10.2 Documentation Deliverables

- [x] `README.md` - Comprehensive guide
- [x] `PRD.md` - This document
- [x] `TASKS.md` - Task breakdown

### 10.3 Output Deliverables

- [x] `output/task1_fft_filtering.png`
- [x] `output/task1_histograms.png`
- [x] `output/task2_edge_detection.png`
- [x] `output/task2_threshold_analysis.png`
- [x] `output/task3_hough_transform.png`
- [x] Additional individual images

---

## 11. Success Metrics

### 11.1 Completion Criteria

| Metric | Target | Status |
|--------|--------|--------|
| All tasks implemented | 100% | ✅ Complete |
| Visualizations generated | 5+ figures | ✅ Complete |
| Documentation complete | README + PRD + TASKS | ✅ Complete |
| Code quality | Clean, commented | ✅ Complete |

### 11.2 Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Edge detection accuracy | > 90% | Visual inspection |
| Filter effectiveness | Clear differences | Histogram analysis |
| Hough line detection | 80% of edges | Line count |
| Documentation clarity | Understandable by peers | Peer review |

---

## 12. Risk Management

### 12.1 Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Library compatibility | Low | High | Use stable versions |
| Performance issues | Medium | Low | Optimize critical sections |
| Unclear results | Low | Medium | Add extensive visualization |
| Documentation incomplete | Low | Medium | Plan time for writing |

### 12.2 Mitigation Strategies

**Technical Risks:**
- Use well-established libraries (NumPy, OpenCV)
- Test on multiple platforms
- Include fallbacks for sample images

**Documentation Risks:**
- Write documentation alongside code
- Use templates and examples
- Peer review before submission

---

## 13. Timeline and Milestones

### 13.1 Development Phases

| Phase | Duration | Deliverables | Status |
|-------|----------|--------------|--------|
| **Phase 1:** Setup | 0.5 days | Environment, dependencies | ✅ Complete |
| **Phase 2:** Task 1 | 1 day | FFT filtering | ✅ Complete |
| **Phase 3:** Task 2 | 1 day | Edge detection | ✅ Complete |
| **Phase 4:** Task 3 | 1 day | Hough transform | ✅ Complete |
| **Phase 5:** Documentation | 1 day | README, PRD, TASKS | ✅ Complete |
| **Phase 6:** Testing | 0.5 days | Validation | ✅ Complete |

### 13.2 Milestones

- ✅ M1: FFT implementation working
- ✅ M2: All three filters functional
- ✅ M3: Triangle edge detection successful
- ✅ M4: Hough lines detected
- ✅ M5: All visualizations generated
- ✅ M6: Documentation complete

---

## 14. Approval and Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| **Author** | Anna | January 2026 | ✅ Approved |
| **Instructor** | [Pending] | [Pending] | [ ] |
| **Self-Review** | Anna | January 2026 | ✅ Complete |

---

## 15. Appendices

### Appendix A: Glossary

| Term | Definition |
|------|------------|
| **FFT** | Fast Fourier Transform - efficient algorithm for computing DFT |
| **IFFT** | Inverse Fast Fourier Transform |
| **Frequency Domain** | Representation of signal/image in terms of frequencies |
| **Spatial Domain** | Standard pixel representation of image |
| **Low-pass Filter** | Removes high frequencies, smooths image |
| **High-pass Filter** | Removes low frequencies, enhances edges |
| **Band-pass Filter** | Keeps only mid-range frequencies |
| **Hough Transform** | Algorithm for detecting shapes (lines, circles) |
| **Scalene Triangle** | Triangle with all sides of different lengths |
| **Threshold** | Value used to convert grayscale to binary |

### Appendix B: References

- Digital Image Processing - Gonzalez & Woods (3rd Edition)
- OpenCV Documentation: https://docs.opencv.org
- NumPy FFT Documentation: https://numpy.org/doc/stable/reference/routines.fft.html

---

**Document Version:** 1.0  
**Last Updated:** January 2026  
**Status:** ✅ Approved for Implementation  
**Next Review:** Upon assignment completion