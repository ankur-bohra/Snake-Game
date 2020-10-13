'''
All adjustable game settings
'''
GRID_SIZE = 20 # cells
CELL_SIZE = 30 # px

MIN_LENGTH = 5 # cells
MIN_STEP = 330 # ms

FOOD_CELLS_PRESENT = 3 # at a time
FOOD_GEN_STEP_MIN = 2000 # between eating and replacement
FOOD_GEN_STEP_MAX = 4000
FOOD_STEP_LOSSES = [10, 15, 20]
FOOD_RARITY = [0.5, 0.3, 0.2] # probability, corresponding to FOOD_STEP_LOSSES, multiples of 0.1

GRID_COLOR = "black"
BODY_COLOR = "green" # body + tail
HEAD_COLOR = "dark green"
FOOD_COLORS = ["red", "orange", "yellow"] # corresponding to FOOD_STEP_LOSSES
