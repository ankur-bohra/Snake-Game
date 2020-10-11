'''
Snake game
'''
from tkinter import *
import random
import time

# Game settings
GRID_SIZE = 20
CELL_SIZE = 30
MIN_LENGTH = 10
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
    print(g)
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

def move(snake, direction):
    time.sleep(3)
    print(snake, direction)

snake = {"head":None, "body":[], "tail":None, "cells_occupied": 0, "all":[]}
head_cell = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
head_data = {"position":head_cell, "next":None}
change_cell(head_cell, cell_color(snake))
snake.update({"head":head_data, "cells_occupied":1, "cells":[head_cell]})
while snake["cells_occupied"] <= MIN_LENGTH:
    front = snake["head"] if snake["cells_occupied"] == 1 else snake["body"][-1]
    snake_cell = random.choice(neighbours(front if front else snake["head"]))
    while snake_cell in snake["cells"]:
        snake_cell = random.choice(neighbours(front))
    snake["cells"].append(snake_cell)
    change_cell(snake_cell, cell_color(snake))
    cell_data = {"position":snake_cell, "next": front}

    snake["cells_occupied"] += 1
    if snake["cells_occupied"] == MIN_LENGTH:
        snake["tail"] = cell_data
    else:
        snake["body"].append(cell_data)

window.mainloop()
