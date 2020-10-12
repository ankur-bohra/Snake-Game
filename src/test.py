'''
Snake game
'''
from tkinter import *
import random
import time

# Game settings
GRID_SIZE = 20
CELL_SIZE = 30
MIN_LENGTH = 3
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
        cell = Frame(game, bg=color, height=CELL_SIZE, width=CELL_SIZE)
        cell.place(relx=x/GRID_SIZE, rely=y/GRID_SIZE)
        grid[y][x] = cell

def change_cell(position, color):
    cellx = position[0]
    celly = position[1]
    cell = grid[celly][cellx]
    cell.config(bg=color)

def from_rgb(rgb):
    return "#%02x%02x%02x" % rgb

def cell_color(snake):
    no_cells = snake["cells_occupied"]
    g = 255 - no_cells * 5
    return from_rgb((0, g, 0))

def neighbours(snake_cell):
    position = snake_cell["position"]
    cellx = position[0]
    celly = position[1]
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
    cellx = cell["position"][0] * CELL_SIZE
    celly = cell["position"][1] * CELL_SIZE
    if side in ["TOP", "BOTTOM"]:
        border_frame.config(width=CELL_SIZE, height=2, bg="blue" if side == "TOP" else "dark blue")
        if side == "TOP":
            border_frame.place(x=cellx, y=celly)
        else:
            border_frame.place(x=cellx, y=celly + CELL_SIZE - 2)
    else:
        border_frame.config(width=2, height=CELL_SIZE, bg="red" if side == "LEFT" else "dark red")
        if side == "LEFT":
            border_frame.place(x=cellx, y=celly)
        else:
            border_frame.place(x=cellx + CELL_SIZE, y=celly)


def outline(snake):
    current_cell = snake["tail"]
    while current_cell:
        linked_cell = current_cell["next"] or current_cell["previous"]
        current_pos, linked_pos = current_cell["position"], linked_cell["position"]
        diffx, diffy = current_pos[0] - linked_pos[0], current_pos[1] - linked_pos[1]
        if diffx == 1:
            sides = ["TOP", "BOTTOM", "LEFT"]
        elif diffx == -1:
            sides = ["TOP", "BOTTOM", "RIGHT"]
        elif diffy == 1:
            sides = ["BOTTOM", "LEFT", "RIGHT"]
        elif diffy == -1:
            sides = ["TOP", "LEFT", "RIGHT"]
        for side in sides:
            border(current_cell, side)
        current_cell = linked_cell if "previous" not in current_cell.keys() else None
'''
next_cell = {"position":(10, 11), "next":None, "previous": None}
test_cell = {"position":(10, 10), "next": next_cell}
next_cell.update({"previous": test_cell})
change_cell(test_cell["position"], "grey")
change_cell(next_cell["position"], "dark grey")
outline({"tail":test_cell})
'''
snake = {
    "head":[],
    "body":[],
    "tail":[],
    "cells_occupied": 0,
    "all":[]
}
head_cell = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
head_data = {"position":head_cell, "next":None, "previous":None}
change_cell(head_cell, "yellow")
snake.update({"head":head_data, "cells_occupied":1, "cells":[head_cell]})

while snake["cells_occupied"] < MIN_LENGTH:
    latest = snake["head"] if snake["cells_occupied"] == 1 else snake["body"][-1]
    snake_cell = random.choice(neighbours(latest))
    while snake_cell in snake["cells"]:
        snake_cell = random.choice(neighbours(latest))
    snake["cells"].append(snake_cell)
    change_cell(snake_cell, cell_color(snake))
    cell = {"position":snake_cell, "next": latest}

    snake["cells_occupied"] += 1
    if snake["cells_occupied"] == MIN_LENGTH:
        snake["tail"] = cell
        change_cell(snake_cell, "purple")
    else:
        snake["body"].append(cell)
        if snake["cells_occupied"] == 2:
            snake["head"]["previous"] = cell

outline(snake)


window.mainloop()
