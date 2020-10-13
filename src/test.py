'''
Snake game
'''
import random
from tkinter import *
from settings import *

# Tkinter focus
window = Tk()
window.title("Snake Game")
window.geometry(str(GRID_SIZE * CELL_SIZE)+"x"+str(GRID_SIZE * CELL_SIZE))

game = Frame(window, bg="black")
game.pack(fill=BOTH, expand=True)


# Internal states, variables
state = "PLAYING"
step = MIN_STEP
movedir = (0, -1)


# Grid formation
grid = []
def makegrid():
    for y in range(GRID_SIZE):
        row = []
        for x in range(GRID_SIZE):
            frame = Frame(game, bg="black", height=CELL_SIZE, width=CELL_SIZE)
            frame.place(relx=x/GRID_SIZE, rely=y/GRID_SIZE)
            slot = {"frame":frame, "object":None}
            row.append(slot)
        grid.append(row)


# Utility
def makecell(cell_type, pos, data):
    cell = {"type": cell_type, "pos":pos}
    cell.update(data)
    return  cell

def occupy(cell):
    color_map = {
        "head": HEAD_COLOR,
        "body": BODY_COLOR,
        "free": GRID_COLOR
    }
    for index in range(len(FOOD_STEP_LOSSES)):
        loss = FOOD_STEP_LOSSES[index]
        color = FOOD_COLORS[index]
        name = "food"+str(loss)
        color_map.update({name:color})

    cellx, celly = cell["pos"][0], cell["pos"][1]
    slot = grid[celly][cellx]
    bg = color_map[cell["type"]]

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


# Generators
def makefood():
    global state
    if state != "PLAYING":
        return

    foodx, foody = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    while grid[foody][foodx]["object"]:
        foodx, foody = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    food_pos = (foodx, foody)

    weighted_losses = []
    for index in range(len(FOOD_STEP_LOSSES)):
        loss = FOOD_STEP_LOSSES[index]
        probability = FOOD_RARITY[index]

        weighted_losses.extend([loss] * int(probability * 10)) # total weight = 10
    loss = random.choice(weighted_losses)

    food = {"type":"food"+str(loss), "pos":food_pos, "step_loss":loss}
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
    head_cell = makecell("head", head_pos, {"next": None, "previous":None})
    occupy(head_cell)
    snake.update({"head":head_cell, "cells_occupied":1})

    while snake["cells_occupied"] < MIN_LENGTH:
        if snake["cells_occupied"] == 1:
            latest = snake["head"]
        else:
            latest = snake["body"][-1]

        pos = random.choice(neighbours(latest))
        while pos in snake["positions"]:
            pos = random.choice(neighbours(latest))
        snake["positions"].append(pos)

        cell = makecell("body", pos, {"next": latest, "previous":None})
        occupy(cell)

        latest.update({"previous":cell})
        snake["cells_occupied"] += 1

        if snake["cells_occupied"] == MIN_LENGTH:
            snake["tail"] = cell
        else:
            snake["body"].append(cell)
            if snake["cells_occupied"] == 2:
                snake["head"]["previous"] = cell
    # outline(snake)
    print("Snake finished")
    return snake


# Movement
def collision(snake, obj):
    global state, step
    if obj["type"] == "body":
        state = "DEAD"
    elif obj["type"].startswith("food"):
        step -= obj["step_loss"]
        print(step)
        # Extend snake from TAIL
        tail = snake["tail"]
        pos = tail["pos"]
        pos1 = tail["next"]["pos"]
        new_pos = (-(pos[0] - pos1[0]), -(pos[1] - pos1[1]))
        new_tail = makecell("body", new_pos, {"next": tail, "previous":None})

        snake["tail"] = new_tail
        tail["previous"] = new_tail
        snake["body"].append(tail)

        # Make new food but after a delay
        gen_step = random.randint(FOOD_GEN_STEP_MIN, FOOD_GEN_STEP_MAX)
        game.after(gen_step, makefood)

def movesnake(snake):
    global state
    global movedir
    if state == "PLAYING":
        cell = snake["tail"]
        while cell:
            if cell == snake["tail"]:
                occupy({"type": "free", "pos":cell["pos"]}) # Tail clearing won't affect any previous cell

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

        # for frame in snake["outline"]:
            # frame.destroy()
        # outline(snake)

    if state == "PAUSED" or state == "PLAYING":
        def move_selfcall():
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


# One life
def startlife():
    makegrid()
    snake = makesnake()
    movesnake(snake)
    for _ in range(FOOD_CELLS_PRESENT):
        makefood()


# Start game
startlife()

window.bind("<KeyPress>", movebind)
window.mainloop()
