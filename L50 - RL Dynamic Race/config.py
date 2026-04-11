# config.py — all constants for L50 RL Dynamic Race

# --- Grid ---
GRID_SIZE = 12
START = (0, 0)
GOAL = (11, 11)

# --- Static obstacles (same layout as L49) ---
BUILDINGS = [
    (1, 3), (2, 3), (3, 3),
    (1, 8), (2, 8),
    (4, 5), (4, 6), (5, 6),
    (6, 2), (7, 2), (7, 3),
    (5, 9), (6, 9), (6, 10),
    (8, 6), (9, 6), (9, 7),
    (3, 10), (4, 10),
    (8, 1), (8, 2),
]
WIND_ZONES = [
    (1, 5), (1, 6),
    (3, 1), (3, 2),
    (5, 4),
    (7, 7), (7, 8),
    (9, 3), (9, 4),
    (10, 8), (10, 9),
]

# --- Dynamic event config ---
EVENT_INTERVAL = 30      # new event every N episodes
EVENT_LIFETIME = 90      # episodes before event disappears
MAX_DYNAMIC = 6          # max active dynamic cells at once

EVENT_TYPES   = ["pit", "barrier", "bridge", "wind"]
EVENT_WEIGHTS = [0.25,   0.25,      0.25,    0.25]   # equal probability

# --- Rewards ---
REWARD_GOAL     = 100
REWARD_STEP     = -1
REWARD_BUILDING = -20
REWARD_WIND     = -5
REWARD_PIT      = -30    # drone falls in → big penalty, episode ends
REWARD_BRIDGE   = +15    # bonus tile

# --- Bellman / Value Iteration ---
VI_THETA    = 0.01   # convergence threshold (stop when max change < this)
VI_MAX_ITER = 300    # safety cap on iterations

# --- Q-Learning ---
ALPHA         = 0.1
GAMMA         = 0.95
EPSILON_START = 1.0
EPSILON_MIN   = 0.02
EPSILON_DECAY = 0.997

# --- Training ---
NUM_EPISODES        = 800
MAX_STEPS           = 200
VIZ_UPDATE_INTERVAL = 25

# --- Output ---
SAVE_PATH    = "outputs/"
FIGURE_TITLE = "RL vs Q-Learning: Dynamic Drone Race"
