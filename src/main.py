'''
Snake game
'''
from tkinter import *

# Game settings
GRID_SIZE = 20
CELL_SIZE = 30
WIN_SIZE = GRID_SIZE * CELL_SIZE

# Make separate window screens
window = Tk()
window.title("Snake Game")
window.geometry(str(WIN_SIZE)+"x"+str(WIN_SIZE))

menu = Frame(window, bg="black")
menu.pack(fill=BOTH, expand=True)

game = Frame(window, bg="black")
game.pack_forget()

# Build grid
grid, widgets = [], []
for y in range(GRID_SIZE):
    row = []
    for x in range(GRID_SIZE):
        row.append(None) # Make space for elements even if they aren't there yet
    grid.append(row)

def play():
    '''
    Display the game screen and begin all logic
    '''
    # Game screen
    menu.pack_forget()
    game.pack(fill=BOTH, expand=True)
    for y in range(GRID_SIZE):
        row = []
        for x in range(GRID_SIZE):
            color = "black" if (x+y)%2 == 0 else "white"
            cell = Frame(game, bg=color, height=CELL_SIZE, width=CELL_SIZE)
            cell.place(relx=x/GRID_SIZE, rely=y/GRID_SIZE)
            row.append(cell)
        grid.append(row)


# Parent screens


game_title = Label(menu,
                   text="Snake Game", font=("Arial", 30, "bold"),
                   fg="green", bg="black")
game_title.place(relx=0.25, rely=0.2)

play_btn = Button(menu,
                  borderwidth=3, relief=RIDGE,
                  text="Play", font=("Arial", 20, "bold"),
                  fg="black", bg="green", activebackground="light green",
                  width=7,
                  command=play)
play_btn.place(relx=.375, rely=0.4)

scores_btn = Button(menu,
                    borderwidth=3, relief=RIDGE,
                    text="Scores", font=("Arial", 20, "bold"),
                    fg="black", bg="green", activebackground="light green",
                    width=7)
scores_btn.place(relx=.375, rely=0.545)

credits_btn = Button(menu,
                     borderwidth=3, relief=RIDGE,
                     text="Credits", font=("Arial", 20, "bold"),
                     fg="black", bg="green", activebackground="light green",
                     width=7)
credits_btn.place(relx=0.375, rely=0.69)

window.mainloop()
