'''
Core game and only required interface
'''
import random
from tkinter import *
from settings import *


# Globals
game = None
end_game = None # Pass down score update function from interface
score = {"frame": None, "value": 0}
step = 300

# Semi-globals
state = "PLAYING"
movedir = (0, 0)


# Grid formation
grid = []
def makegrid():
    global game
    for y in range(GRID_SIZE):
        row = []
        for x in range(GRID_SIZE):
            frame = Frame(game, bg="black", height=CELL_SIZE, width=CELL_SIZE)
            frame.place(relx=x/GRID_SIZE, rely=y/GRID_SIZE)
            slot = {"frame":frame, "object":None}
            row.append(slot)
        grid.append(row)


# Utility
def reset():
    global grid, game, end_game, score, state, movedir
    grid = []
    movedir = (0, 0) # So the next life find movedir again
    game, end_game = None, None
    score["value"] = 0

def makecell(cell_type, pos, data):
    cell = {"type": cell_type, "pos":pos}
    cell.update(data)
    return  cell

color_map = {
        "snakehead": HEAD_COLOR,
        "snakebody": BODY_COLOR,
        "free": GRID_COLOR
    }
for index in range(len(FOOD_POINTS)):
    points = FOOD_POINTS[index]
    color = FOOD_COLORS[index]
    name = "food"+str(points)
    color_map.update({name:color})
def occupy(cell):
    if grid != [] and state == "PLAYING":
        cellx, celly = cell["pos"][0], cell["pos"][1]

        bg = color_map[cell["type"]]

        slot = grid[celly][cellx]
        slot["frame"].config(bg=bg)
        slot["object"] = cell

def neighbours(cell):
    pos = cell["pos"]
    cellx = pos[0]
    celly = pos[1]
    cell_neighbours = []
    if cellx in [0, GRID_SIZE - 1] and celly in [0, GRID_SIZE - 1]:
        # Some corner
        cell_neighbours.append((1 if cellx == 0 else GRID_SIZE - 2, celly))
        cell_neighbours.append((cellx, 1 if celly == 0 else GRID_SIZE - 2))
    elif cellx in [0, GRID_SIZE - 1]:
        cell_neighbours.extend([(cellx, celly - 1), (cellx, celly + 1)]) # Above, below
        cell_neighbours.append((cellx + 1 if cellx == 0 else cellx - 1, celly)) # Left, right
    elif celly in [0, GRID_SIZE - 1]:
        cell_neighbours.extend([(cellx - 1, celly), (cellx + 1, celly)]) # Left, right
        cell_neighbours.append((cellx, celly + 1 if celly == 0 else celly - 1)) # Above, below
    else:
        # Not on edge
        cell_neighbours.extend([(cellx, celly - 1), (cellx, celly + 1)]) # Above, below
        cell_neighbours.extend([(cellx - 1, celly), (cellx + 1, celly)]) # Left, right
    return cell_neighbours

def die():
    global state, step, score
    state = "DEAD"
    end_game(score["value"], step)
    reset()

# Generators
def makefood():
    global state
    if state != "PLAYING":
        return

    foodx, foody = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    while grid[foody][foodx]["object"]:
        foodx, foody = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    food_pos = (foodx, foody)

    weighted_points = []
    for index in range(len(FOOD_POINTS)):
        points = FOOD_POINTS[index]
        probability = FOOD_RARITY[index]

        weighted_points.extend([points] * int(probability * 10)) # total weight = 10
    points = random.choice(weighted_points)

    food = {"type":"food"+str(points), "pos":food_pos, "points":points}
    occupy(food)

def makesnake():
    snake = {
        "head":[],
        "body":[],
        "tail":[],
        "positions":[],
        "outline": [],
        "cells_occupied": 0
    }
    head_pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    head_cell = makecell("snakehead", head_pos, {"next": None, "previous":None})
    occupy(head_cell)
    snake.update({"head":head_cell, "cells_occupied":1, "positions":[head_pos]})

    while snake["cells_occupied"] < MIN_LENGTH:
        if snake["cells_occupied"] == 1:
            latest = snake["head"]
        else:
            latest = snake["body"][-1]

        pos = random.choice(neighbours(latest))
        while pos in snake["positions"]:
            pos = random.choice(neighbours(latest))
        snake["positions"].append(pos)

        cell = makecell("snakebody", pos, {"next": latest, "previous":None})
        occupy(cell)

        latest.update({"previous":cell})
        snake["cells_occupied"] += 1

        if snake["cells_occupied"] == MIN_LENGTH:
            snake["tail"] = cell
        else:
            snake["body"].append(cell)
            if snake["cells_occupied"] == 2:
                snake["head"]["previous"] = cell
    return snake


# Movement
def collision(snake, obj):
    global state
    global step
    global game
    global grid
    if obj["type"].startswith("snake"):
        die()
    elif obj["type"].startswith("food"):
        score["value"] += obj["points"]
        score["label"].config(text="Score: "+str(score["value"]))
        # Extend snake from TAIL
        tail = snake["tail"]
        pos = tail["pos"]
        pos1 = tail["next"]["pos"]
        new_pos = (-(pos[0] - pos1[0]), -(pos[1] - pos1[1]))
        new_tail = makecell("snakebody", new_pos, {"next": tail, "previous":None})

        snake["tail"] = new_tail
        tail["previous"] = new_tail
        snake["body"].append(tail)

        # Make new food but after a delay
        gen_step = random.randint(FOOD_GEN_STEP_MIN, FOOD_GEN_STEP_MAX)
        game.after(gen_step, makefood)

def defaultdir(snake):
    neighbour_pos = neighbours(snake["head"])
    for pos in neighbour_pos:
        if pos in snake["positions"]:
            neighbour_pos.remove(pos)

    next_pos = random.choice(neighbour_pos)
    pos = snake["head"]["pos"]
    randomdir = (next_pos[0] - pos[0], - (next_pos[1] - pos[1])) # Y axis is flipped
    return randomdir

def movesnake(snake):
    global state
    global movedir
    global game
    if movedir == (0, 0): # Set starting direction
        movedir = defaultdir(snake)
    if state == "PLAYING":
        cell = snake["tail"]
        while cell:
            if cell == snake["tail"]:
                occupy({"type": "free", "pos":cell["pos"]}) # Clear tail cell

            if cell == snake["head"]:
                oldx, oldy = cell["pos"][0], cell["pos"][1]
                newx, newy = oldx + movedir[0], oldy + movedir[1]

                # Handle edge movement
                if newx == GRID_SIZE:
                    newx = 0
                elif newx == -1:
                    newx = GRID_SIZE - 1
                elif newy == GRID_SIZE:
                    newy = 0
                elif newy == -1:
                    newy = GRID_SIZE - 1

                cell["pos"] = (newx, newy)

                slot = grid[newy][newx]
                if slot["object"]:
                    collision(snake, slot["object"])
                occupy(cell)
            else:
                cell["pos"] = cell["next"]["pos"]
                occupy(cell)

            cell = cell["next"]

        if state == "PLAYING": # When the loop breaks check the state again, state may have changed
            def move_selfcall():
                global state
                movesnake(snake)
            game.after(step, move_selfcall)

def movebind(key):
    global movedir, state
    key_map = { # The Y signs are flipped since the Y axis is flipped
        "w": (0, -1),
        "s": (0, 1),
        "a": (-1, 0),
        "d": (1, 0)
    }
    key = key.char.lower()
    # Validate key
    validkey = key in key_map.keys() and key_map[key][movedir.index(0)] != 0 # in wasd, must be across other axis
    if validkey and state == "PLAYING":
        movedir = key_map[key]


# Combine game
def startlife(window):
    global state
    state = "PLAYING"
    # Start core logic
    makegrid()
    snake = makesnake()

    # Listen for some input before starting movement
    label = Label(game,
                  text="Press [ENTER] to start", font=("Arial", 15, "bold"),
                  fg="white", bg="black", width=30)
    label.place(relx=0.2, rely=0.45)

    def startmechanics(key):
        if key.keysym == "Return":
            global state
            state = "PLAYING"
            movesnake(snake)
            for _ in range(FOOD_CELLS_PRESENT):
                makefood()
            window.unbind("<Return>")
            label.destroy()

    state = "WAITING"
    window.bind("<Return>", startmechanics)

def playgame(window, mode_step, passed_ender):
    global game, step, score, end_game

    # Initialize globals
    step = mode_step

    game = Frame(window, bg="black")
    game.pack(fill=BOTH, expand=True)

    end_game = passed_ender

    # Start a single life
    startlife(window)

    def completesetup(): # Don't overwrite bind before input
        global state, game
        if state == "PLAYING":
            # Score above cell not the other way round
            label = Label(game,
                          text="Score: 0", font=("Arial", 10, "bold"),
                          fg="white", bg="black", width=8)
            label.place(x=10, y=10)
            score["label"] = label

            window.bind("<KeyPress>", movebind) # Don't need to bind right before mainloop
        elif game:
            game.after(500, completesetup)
    completesetup()

    return game # Pass up the window so interface can clean it
