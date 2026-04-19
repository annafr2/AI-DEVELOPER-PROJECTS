# PRD — L52: LSTM Signal Filter

## Goal
Build an LSTM neural network that acts as a smart frequency filter.
Given a short window of a noisy, mixed signal, the model learns to extract
(predict) the clean value of one chosen frequency.

---

## Problem

A real-world signal is almost never clean.
Imagine 4 radio stations broadcasting at 1, 3, 5, and 7 Hz all at once —
mixed together with noise. We want to tune in to only 3 Hz.

Traditional filters (e.g., Butterworth) are good but dumb — they use fixed math.
An LSTM can learn the filtering task from data, potentially handling
more complex patterns or non-stationary signals.

---

## Signal Design

| Parameter          | Value                              |
|--------------------|------------------------------------|
| Frequencies        | 1, 3, 5, 7 Hz                      |
| Sampling rate      | 1000 Hz (1 kHz)                    |
| Duration           | 10 seconds → 10,000 samples        |
| Base amplitude     | 1.0 per sinusoid                   |
| Amplitude draw     | Uniform(0.8, 1.2) per signal       |
| Amplitude noise    | Gaussian(0, 0.005) per sample      |
| Phase draw         | Uniform(0°, 360°)                  |
| Phase noise        | Gaussian(0, 0.05 rad) per sample   |
| Normalization      | Zero-mean, unit-std per signal     |

---

## Dataset Design

| Item               | Details                                          |
|--------------------|--------------------------------------------------|
| Input X            | Sliding window of 10 noisy mixed samples         |
| Target y           | Next clean value of the target frequency (3 Hz)  |
| Total windows      | 9,990                                            |
| Train split        | 80% = 7,992 samples                              |
| Test split         | 20% = 1,998 samples                              |

Ground truth = clean sinusoid (no noise).
Input = noisy mixed signal (all 4 frequencies + noise).

---

## Model Architecture

```
Input  (batch, 10, 1)
   ↓
LSTM   (hidden=64, layers=2, dropout=0.2)
   ↓
Linear (64 → 1)
   ↓
Output (batch, 1)   ← predicted clean value of target frequency
```

Loss function: **MSE** (Mean Squared Error) against the clean target.

---

## Outputs

| File                       | Description                                  |
|----------------------------|----------------------------------------------|
| `outputs/01_individual_signals.png` | 4 sinusoids: clean vs noisy         |
| `outputs/02_mixed_signals.png`      | Sum of all 4: clean vs noisy        |
| `outputs/03_spectrum.png`           | FFT magnitude showing 4 peaks       |
| `outputs/04_loss_curves.png`        | Train and test MSE over epochs      |
| `outputs/05_predictions.png`        | Model output vs clean ground truth  |
| `outputs/lstm_filter.pt`            | Saved best model weights            |

---

## Success Criteria
- Test MSE < 0.05 on the target frequency
- Loss decreasing smoothly (no divergence)
- Prediction plot visually tracks the clean sinusoid
