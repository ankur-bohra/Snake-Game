'''
Snake game
'''
from tkinter import *
import random
import asyncio

# Game settings
GRID_SIZE = 20
CELL_SIZE = 30
MIN_LENGTH = 5
MIN_SPEED = 3

# Make separate window screens
window = Tk()
window.title("Snake Game")
window.geometry(str(GRID_SIZE * CELL_SIZE)+"x"+str(GRID_SIZE * CELL_SIZE))

game = Frame(window, bg="black")
game.pack(fill=BOTH, expand=True)

grid = []

# State variables
canmove = True
movedir = (0, -1)

# Making grid, snake
for y in range(GRID_SIZE):
    row = []
    for x in range(GRID_SIZE):
        cell = Frame(game, bg="black", height=CELL_SIZE, width=CELL_SIZE)
        cell.place(relx=x/GRID_SIZE, rely=y/GRID_SIZE)
        row.append(cell)
    grid.append(row)

def makecell(pos, next_cell, previous_cell):
    return {"pos":pos, "next":next_cell, "previous":previous_cell}

def color(cell, target):
    cellx = cell["pos"][0]
    celly = cell["pos"][1]
    cell = grid[celly][cellx]
    cell.config(bg=target)

def neighbours(cell_pos):
    pos = cell_pos["pos"]
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

def border(cell, side):
    border_frame = Frame(game, bg="black")
    cellx = cell["pos"][0] * CELL_SIZE
    celly = cell["pos"][1] * CELL_SIZE
    if side in ["TOP", "BOTTOM"]:
        border_frame.config(width=CELL_SIZE, height=1, bg="light green")
        if side == "TOP":
            border_frame.place(x=cellx, y=celly)
        else:
            border_frame.place(x=cellx, y=celly + CELL_SIZE - 1)
    else:
        border_frame.config(width=1, height=CELL_SIZE, bg="light green")
        if side == "LEFT":
            border_frame.place(x=cellx, y=celly)
        else:
            border_frame.place(x=cellx + CELL_SIZE, y=celly)
    return border_frame

def outline(snake):
    dirs = {
        (0, 1): "TOP",
        (0, -1): "BOTTOM",
        (1, 0): "LEFT",
        (-1, 0): "RIGHT",
    }

    focus = snake["tail"]
    link1 = focus["next"]
    link2 = focus["previous"]
    while focus:
        borders = ["TOP", "BOTTOM", "LEFT", "RIGHT"]
        pos = focus["pos"]

        if link1:
            pos1 = link1["pos"]
            offset1 = (pos[0] - pos1[0], pos[1] - pos1[1])
            dir1 = dirs[offset1] # pos - pos1
            if dir1 in borders:
                borders.remove(dir1)
        if link2:
            pos2 = link2["pos"]
            offset2 = (pos[0] - pos2[0], pos[1] - pos2[1])
            dir2 = dirs[offset2] # pos - pos2
            if dir2 in borders:
                borders.remove(dir2)

        for side in borders:
            snake["outline"].append(border(focus, side))

        # Move to another cell
        if link1:
            focus = focus["next"]
            link1 = focus["next"]
            link2 = focus["previous"]
        else:
            break

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
    head_cell = makecell(head_pos, None, None)
    color(head_cell, "dark green")
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

        cell = makecell(pos, latest, None)
        color(cell, "green")

        latest.update({"previous":cell})
        snake["cells_occupied"] += 1

        if snake["cells_occupied"] == MIN_LENGTH:
            snake["tail"] = cell
        else:
            snake["body"].append(cell)
            if snake["cells_occupied"] == 2:
                snake["head"]["previous"] = cell
    outline(snake)
    return snake

def movesnake(snake):
    global canmove
    global movedir
    while canmove:
        cell = snake["tail"]
        while cell:
            if cell == snake["tail"]:
                color(cell, "black") # For tail, clearing won't affect any previous cell
            else:
                color(cell, "green") # Other cells will be taken up by previous cells

            if cell == snake["head"]:
                cell["pos"] = (cell["pos"][0] + movedir[0], cell["pos"][1] + movedir[1])
                color(cell, "dark green")
            else:
                cell["pos"] = cell["next"]["pos"]

            cell = cell["next"]

        for frame in snake["outline"]:
            frame.destroy()
        outline(snake)

        asyncio.sleep(0.5)

def movebind(key):
    key_map = { # The Y signs are flipped since the grid Y is flipped
        "w": (0, -1),
        "s": (0, 1),
        "a": (-1, 0),
        "d": (1, 0),
    }
    key = key.char
    if canmove and key in key_map.keys():
        global movedir
        movedir = key_map[key.lower()]

snake = makesnake()
movesnake(snake)

window.bind("<KeyPress>", movebind)
window.mainloop()
