'''
Snake game
'''
from tkinter import *

# Game settings
GRID_SIZE = 15
CELL_SIZE = 30
WIN_SIZE = GRID_SIZE * CELL_SIZE

# Construct window as grid
grid, widgets = [], []

window = Tk()
window.title("Snake Game")
window.geometry(str(WIN_SIZE)+"x"+str(WIN_SIZE))

game = Frame(window, bg="black")
game.pack(fill=BOTH, expand=True)
'''
for y in range(GRID_SIZE):
    row = []
    for x in range(GRID_SIZE):
        row.append(None) # Make space for elements even if they aren't there yet
    grid.append(row)
'''
for y in range(GRID_SIZE):
    row = []
    for x in range(GRID_SIZE):
        color = "black" if (x+y)%2 == 0 else "white"
        cell = Frame(game, bg=color, height=CELL_SIZE, width=CELL_SIZE)
        cell.place(relx=x/GRID_SIZE, rely=y/GRID_SIZE)
        row.append(cell)
    grid.append(row)
window.mainloop()
