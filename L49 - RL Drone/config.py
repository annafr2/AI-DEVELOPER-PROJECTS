# config.py — all constants for the RL Drone project

# --- Grid ---
GRID_SIZE = 12
START = (0, 0)
GOAL = (11, 11)

# --- Rewards ---
REWARD_GOAL = 100
REWARD_STEP = -1
REWARD_BUILDING = -20
REWARD_WIND = -5

# --- Q-Learning hyperparameters ---
ALPHA = 0.1            # learning rate
GAMMA = 0.99           # discount factor
EPSILON_START = 1.0    # start fully random
EPSILON_MIN = 0.01     # never fully greedy
EPSILON_DECAY = 0.997  # decay per episode

# --- Training ---
NUM_EPISODES = 1500
MAX_STEPS = 200

# --- Traps ---
# Buildings: drone cannot enter, costs -20 per attempt
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

# Wind zones: drone enters but gets pushed randomly, costs -5
WIND_ZONES = [
    (1, 5), (1, 6),
    (3, 1), (3, 2),
    (5, 4),
    (7, 7), (7, 8),
    (9, 3), (9, 4),
    (10, 8), (10, 9),
]

# --- Visualization ---
VIZ_UPDATE_INTERVAL = 20   # redraw every N episodes
SAVE_PATH = "outputs/"
FIGURE_TITLE = "RL Drone Navigation"
