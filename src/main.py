'''
Menu and other interface of game
'''
from tkinter import *
from settings import *


def buildwindow():
    WIN_SIZE = GRID_SIZE * CELL_SIZE

    window = Tk()
    window.title("Snake Game")
    window.geometry(str(WIN_SIZE)+"x"+str(WIN_SIZE))

    return window

def switchandplay(menu, command):
    def callback():
        menu.pack_forget()
        command()
    return callback


def displaymenu(window, play):
    menu = Frame(window, bg="black")
    menu.pack(fill=BOTH, expand=True)
    game_title = Label(menu,
                       text="Snake Game", font=("Arial", 30, "bold"),
                       fg="green", bg="black")
    game_title.place(relx=0.25, rely=0.2)

    play_btn = Button(menu,
                      borderwidth=3, relief=RIDGE,
                      text="Play", font=("Arial", 20, "bold"),
                      fg="black", bg="green", activebackground="light green",
                      width=7,
                      command=switchandplay(menu, play))
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
