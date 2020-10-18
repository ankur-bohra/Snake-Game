'''
All adjustable game settings
'''
GRID_SIZE = 20 # cells
CELL_SIZE = 30 # px
GRID_COLOR = "black"

MIN_LENGTH = 3 # cells
BODY_COLOR = "green" # body + tail
HEAD_COLOR = "dark green"

GAME_MODES = ["Easy", "Moderate", "Difficult", "Hard"]
GAME_STEPS = [250, 200, 150, 100] # corresponding to GAME_MODES

FOOD_CELLS_PRESENT = 3 # at a time
FOOD_GEN_STEP_MIN = 2000 # between eating and replacement
FOOD_GEN_STEP_MAX = 4000
FOOD_POINTS = [10, 15, 20]
FOOD_RARITY = [0.5, 0.3, 0.2] # probability, corresponding to FOOD_STEP_LOSSES, multiples of 0.1
FOOD_COLORS = ["red", "orange", "yellow"] # corresponding to FOOD_STEP_LOSSES

POWERUP_GEN_STEP_MIN = 3000 #10000 # between eating and replacement
POWERUP_GEN_STEP_MAX = 4000 #15000
POWERUPS_PRESENT = 2
POWERUP_TYPES = ["boost", "multiplier"]
POWERUP_DATA = [15, 2] # data concerned with respective powerup
POWERUP_COLORS = ["DarkOrchid1", "cyan2"] # corresponding to POWERUPS
POWERUP_DURATIONS = [5000, 8000] # ms
