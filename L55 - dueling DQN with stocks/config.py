"""Central configuration for L55 Dueling DQN Stock Trader."""
import os

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_DIR    = os.path.join(BASE_DIR, "data", "raw")
OUTPUT_DIR  = os.path.join(BASE_DIR, "outputs")
MODEL_DIR   = os.path.join(BASE_DIR, "outputs", "models")

os.makedirs(DATA_DIR,   exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MODEL_DIR,  exist_ok=True)

# ── Default data settings ─────────────────────────────────────────────────────
DEFAULT_TICKER     = "SMH"
DEFAULT_START      = "2020-01-01"
DEFAULT_END        = "2024-12-31"
WINDOW_SIZE        = 30          # look-back bars fed to the DQN
FEATURES_COUNT     = 10          # 8 engineered + position + unrealised_pnl
TRAIN_FRAC         = 0.70
VAL_FRAC           = 0.15
# TEST_FRAC is the remainder (0.15)

# ── Rate-limit settings (Yahoo Finance public endpoints) ──────────────────────
RATE_LIMIT_PER_MIN    = 10
RATE_LIMIT_PER_HOUR   = 100
MAX_CONCURRENT        = 2
BURST_LIMIT           = 5
BURST_WINDOW_SEC      = 10
MAX_RETRIES           = 3
RETRY_DELAY_SEC       = 5

# ── Trading environment ───────────────────────────────────────────────────────
INITIAL_CAPITAL       = 10_000.0
TRANSACTION_COST_PCT  = 0.001    # 0.1 % per trade
ACTIONS               = {0: "hold", 1: "buy", 2: "sell"}

# ── Dueling DQN hyper-parameters ─────────────────────────────────────────────
HIDDEN_DIM            = 128
LEARNING_RATE         = 1e-4
GAMMA                 = 0.99
EPSILON_START         = 1.0
EPSILON_END           = 0.05
EPSILON_DECAY         = 0.995
REPLAY_BUFFER_SIZE    = 50_000
BATCH_SIZE            = 64
TARGET_UPDATE_FREQ    = 200      # steps between target-net syncs
N_EPISODES            = 300
MAX_STEPS_PER_EPISODE = 500
