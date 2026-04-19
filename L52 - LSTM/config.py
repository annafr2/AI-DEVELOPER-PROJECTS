# config.py — all hyperparameters for L52 LSTM Signal Filter

FREQUENCIES = [1, 3, 5, 7]      # Hz — the 4 sinusoid frequencies
SAMPLE_RATE = 1000               # samples per second (1 kHz)
DURATION = 10                    # seconds → 10,000 total samples
N_SAMPLES = SAMPLE_RATE * DURATION  # 10,000

# Amplitude settings
BASE_AMPLITUDE = 1.0             # base amplitude for all sinusoids
AMP_LOW = 0.8                    # random amplitude lower bound
AMP_HIGH = 1.2                   # random amplitude upper bound
AMP_NOISE_STD = 0.005            # per-sample additive amplitude noise std (0.5%)

# Phase settings
PHASE_NOISE_STD = 0.05           # per-sample phase noise std (radians)

# Target frequency to filter/extract
TARGET_FREQ_HZ = 3               # which frequency the LSTM learns to isolate

# Dataset settings
WINDOW_SIZE = 10                 # context window: number of past samples as input
TRAIN_RATIO = 0.8                # 80% train, 20% test

# Model settings
HIDDEN_SIZE = 64                 # LSTM hidden units
NUM_LAYERS = 2                   # LSTM stacked layers
DROPOUT = 0.2

# Training settings
EPOCHS = 100
BATCH_SIZE = 256
LEARNING_RATE = 1e-3

# Output
OUTPUT_DIR = "outputs"
MODEL_PATH = "outputs/lstm_filter.pt"
SEED = 42
