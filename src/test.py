'''
Snake game
'''
from tkinter import *
import random
import time

# Game settings
GRID_SIZE = 20
CELL_SIZE = 30
MIN_LENGTH = 5
MAX_LENGTH = 50
MIN_SPEED = 3
WIN_SIZE = GRID_SIZE * CELL_SIZE

# Make separate window screens
window = Tk()
window.title("Snake Game")
window.geometry(str(WIN_SIZE)+"x"+str(WIN_SIZE))

game = Frame(window, bg="black")
game.pack(fill=BOTH, expand=True)

grid = [[None] * GRID_SIZE for row in range(GRID_SIZE)]

for y in range(GRID_SIZE):
    for x in range(GRID_SIZE):
        color = "black" if (x+y)%2 == 0 else "white"
        cell = Frame(game, bg="black", height=CELL_SIZE, width=CELL_SIZE)
        cell.place(relx=x/GRID_SIZE, rely=y/GRID_SIZE)
        grid[y][x] = cell

def change_cell(pos, color):
    cellx = pos[0]
    celly = pos[1]
    cell = grid[celly][cellx]
    cell.config(bg=color)

def from_rgb(rgb):
    return "#%02x%02x%02x" % rgb

def cell_color(snake):
    no_cells = snake["cells_occupied"]
    g = 255 - no_cells * 5
    return from_rgb((0, g, 0))

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
            borders.remove(dir1)
        if link2:
            pos2 = link2["pos"]
            offset2 = (pos[0] - pos2[0], pos[1] - pos2[1])
            dir2 = dirs[offset2] # pos - pos2
            borders.remove(dir2)

        print("Filling borders for", pos, "=>", borders)

        for side in borders:
            border(focus, side)

        # Move to another cell
        if link1:
            focus = focus["next"]
            link1 = focus["next"]
            link2 = focus["previous"]
        else:
            break

snake = {
    "head":[],
    "body":[],
    "tail":[],
    "cells_occupied": 0,
    "all":[]
}
head_cell = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
head_data = {"pos":head_cell, "next":None, "previous":None}
change_cell(head_cell, "dark green")
snake.update({"head":head_data, "cells_occupied":1, "cells":[head_cell]})

while snake["cells_occupied"] < MIN_LENGTH:
    latest = snake["head"] if snake["cells_occupied"] == 1 else snake["body"][-1]
    pos = random.choice(neighbours(latest))
    while pos in snake["cells"]:
        pos = random.choice(neighbours(latest))
    snake["cells"].append(pos)
    change_cell(pos, "green")
    cell = {"pos":pos, "next": latest, "previous": None}
    latest.update({"previous":cell})

    snake["cells_occupied"] += 1
    if snake["cells_occupied"] == MIN_LENGTH:
        snake["tail"] = cell
    else:
        snake["body"].append(cell)
        if snake["cells_occupied"] == 2:
            snake["head"]["previous"] = cell

outline(snake)


window.mainloop()
