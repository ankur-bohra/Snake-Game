'''
Snake game project, majorly based on a grid system
'''
from tkinter import *

debug = True

# Game settings
GRID_SIZE = 15
CELL_SIZE = 30

# Construct window as grid
grid = []
widgets = []
WIN_SIZE = GRID_SIZE * CELL_SIZE

window = Tk()
window.title("Snake Game")
window.geometry(str(WIN_SIZE)+"x"+str(WIN_SIZE))

for y in range(GRID_SIZE):
    row = []
    for x in range(GRID_SIZE):
        row.append(None) # Make space for elements even if they aren't there yet
    grid.append(row)


# Menu screen
menu_holder = Frame(window, bg="black")
menu_holder.pack(fill=BOTH, expand=True)

game_title = Label(menu_holder,
                   text="Snake Game", font=("Arial", 30, "bold"),
                   fg="green", bg="black")
game_title.place(relx=0.25, rely=0.2)

play_btn = Button(menu_holder,
                  borderwidth=3, relief=RIDGE,
                  text="Play", font=("Arial", 20, "bold"),
                  fg="black", bg="green", activebackground="light green",
                  width=7)
play_btn.place(relx=.375, rely=0.4)

scores_btn = Button(menu_holder,
                    borderwidth=3, relief=RIDGE,
                    text="Scores", font=("Arial", 20, "bold"),
                    fg="black", bg="green", activebackground="light green",
                    width=7)
scores_btn.place(relx=.375, rely=0.545)

credits_btn = Button(menu_holder,
                     borderwidth=3, relief=RIDGE,
                     text="Credits", font=("Arial", 20, "bold"),
                     fg="black", bg="green", activebackground="light green",
                     width=7)
credits_btn.place(relx=0.375, rely=0.69)

'''
# Game screen
for y in range(GRID_SIZE):
    row = []
    for x in range(GRID_SIZE):
        color = (x + y)%2 == 0 and "black" or "white" if debug else "black"
        cell = Frame(window, bg=color if debug else "black", height=CELL_SIZE, width=CELL_SIZE)
        print(x,y)
        cell.grid(column=x, row=y)
        row.append(cell)
    grid.append(row)
'''
window.mainloop()
