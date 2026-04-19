import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# Dataset
VOCAB_SIZE = 10000      # top 10k words
TRAIN_RATIO = 0.8       # 80% train, 20% held as final test
MAX_SEQUENCES = 100000  # max sequences to create from corpus

# Experiment sequence lengths
EXP_SHORT_LEN = 5
EXP_LONG_LEN = 15

# Default model hyperparameters
DEFAULT_EMBED_SIZE = 128
DEFAULT_HIDDEN_SIZE = 128
DEFAULT_NUM_LAYERS = 2
DEFAULT_DROPOUT = 0.3

# Training
BATCH_SIZE = 64
EPOCHS = 15
LEARNING_RATE = 0.001
CLIP_GRAD = 5.0

# Parameter sweep (SWEEP_EPOCHS kept low to save time)
SWEEP_HIDDEN_SIZES = [64, 128, 256]
SWEEP_NUM_LAYERS = [1, 2, 3]
SWEEP_SEQ_LENS = [5, 10, 20]
SWEEP_EPOCHS = 5

# Text generation
SEED_WORDS = ["the", "a", "he", "she", "they", "in", "it"]
GENERATE_LENGTH = 20
TEMPERATURE = 0.8

# Visualization
PLOT_BG = "#0d0d1a"
ACCENT = "#00D4FF"
COLORS = ["#2ECC71", "#F39C12", "#E74C3C", "#9B59B6", "#3498DB", "#1ABC9C", "#E67E22"]

EXPERIMENTS = {
    "short": {
        "seq_len": EXP_SHORT_LEN,
        "label": "Short Sentences (5 words)",
        "desc": "Can RNN learn from short sequences?",
        "color": COLORS[0],
    },
    "long": {
        "seq_len": EXP_LONG_LEN,
        "label": "Long Sentences (15 words)",
        "desc": "Watch the vanishing gradient appear!",
        "color": COLORS[2],
    },
}
