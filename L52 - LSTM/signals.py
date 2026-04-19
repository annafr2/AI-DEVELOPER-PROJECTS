# signals.py — generate clean and noisy sinusoidal signals

import numpy as np
import config


def _normalize(signal: np.ndarray) -> np.ndarray:
    """Zero-mean, unit-std normalization."""
    std = signal.std()
    return (signal - signal.mean()) / (std if std > 0 else 1.0)


def generate_signals(seed: int = config.SEED):
    """
    Generate 4 clean + 4 noisy sinusoids and their mixed versions.

    Each sinusoid has:
      - random amplitude in [AMP_LOW, AMP_HIGH]
      - random phase in [0, 2π]
      - per-sample amplitude noise (AMP_NOISE_STD)
      - per-sample phase noise (PHASE_NOISE_STD)

    Returns
    -------
    t               : time axis, shape (N,)
    clean_signals   : shape (4, N) — individual clean, normalized
    noisy_signals   : shape (4, N) — individual noisy, normalized
    clean_mixed     : shape (N,)   — sum of clean signals, normalized
    noisy_mixed     : shape (N,)   — sum of noisy signals, normalized
    amps            : list[float]  — drawn amplitudes per frequency
    phases          : list[float]  — drawn phases per frequency (radians)
    """
    rng = np.random.default_rng(seed)
    N = config.N_SAMPLES
    t = np.linspace(0, config.DURATION, N, endpoint=False)

    amps = rng.uniform(config.AMP_LOW, config.AMP_HIGH, size=4)
    phases = rng.uniform(0, 2 * np.pi, size=4)

    clean_signals = np.zeros((4, N))
    noisy_signals = np.zeros((4, N))

    for i, freq in enumerate(config.FREQUENCIES):
        omega = 2 * np.pi * freq

        # --- clean sinusoid ---
        clean_signals[i] = amps[i] * np.sin(omega * t + phases[i])

        # --- noisy sinusoid ---
        amp_noise = rng.normal(0, config.AMP_NOISE_STD, size=N)
        phase_noise = rng.normal(0, config.PHASE_NOISE_STD, size=N)
        noisy_signals[i] = (amps[i] + amp_noise) * np.sin(omega * t + phases[i] + phase_noise)

    # Normalize each individual signal
    clean_norm = np.array([_normalize(s) for s in clean_signals])
    noisy_norm = np.array([_normalize(s) for s in noisy_signals])

    # Mixed signals = sum across all 4 frequencies
    clean_mixed = _normalize(clean_norm.sum(axis=0))
    noisy_mixed = _normalize(noisy_norm.sum(axis=0))

    return t, clean_norm, noisy_norm, clean_mixed, noisy_mixed, amps, phases
