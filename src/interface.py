'''
Menu and other interface of game
'''
from tkinter import *
from core import playgame
from settings import *

window = None
scores = {}
screens = []

def makewindow():
    WIN_SIZE = GRID_SIZE * CELL_SIZE

    global window
    window = Tk()
    window.title("Snake Game")
    window.geometry(str(WIN_SIZE)+"x"+str(WIN_SIZE))

    return window

def clearscreens():
    for screen in screens:
        screen.destroy()

def endgame(score, mode_step):
    # Show a dying screen
    game = screens[-1]
    window.unbind("<KeyPress")

    died_label = Label(game,
                       text="You Died :(", font=("Arial", 30, "bold"),
                       fg="white", bg="black")
    died_label.place(relx=0.34, rely=0.3)
    score_label = Label(game,
                        text="Score: "+str(score), font=("Arial", 19),
                        fg="white", bg="black")
    score_label.place(relx=0.5, rely=0.41, anchor=CENTER)
    cont_label = Label(game,
                       text="Press [ENTER] to continue", font=("Arial", 15, "bold"),
                       fg="grey", bg="black")
    cont_label.place(relx=0.3, rely=0.8)

    def resume(key):
        if key.keysym == "Return":
            if score > 0:
                global scores
                mode = GAME_MODES[GAME_STEPS.index(mode_step)]
                scores[mode].append(score)
                clearscreens()
                displaymenu()
    window.bind("<Return>", resume)

def displaymodes():
    global window, scores
    clearscreens()

    modes_screen = Frame(window, bg="black")
    screens.append(modes_screen)
    modes_screen.pack(fill=BOTH, expand=True)

    mode_title = Label(modes_screen,
                       text="Game Mode", font=("Arial", 30, "bold"),
                       fg="green", bg="black")
    mode_title.place(relx=0.3, rely=0.2)

    def playmode(mode_step):
        def command():
            global scores
            modes_screen.pack_forget()
            game = playgame(window, mode_step, endgame)
            screens.append(game)
        return command

    for index in range(len(GAME_MODES)):
        mode = GAME_MODES[index]
        step = GAME_STEPS[index]
        button = Button(modes_screen,
                        borderwidth=3, relief=RIDGE,
                        text=mode, font=("Arial", 20, "bold"),
                        fg="black", bg="green", activebackground="light green",
                        width=9,
                        command=playmode(step))
        button.place(relx=.34, rely=0.4 + index*0.12)

    back_button = Button(modes_screen,
                         borderwidth=3, relief=RIDGE,
                         text="Back", font=("Arial", 15, "bold"),
                         fg="white", bg="grey", activebackground="light grey",
                         width=5,
                         command=displaymenu)
    back_button.place(relx=0.03, rely=0.9)

def displayscore():
    def showmode(mode_no):
        if mode_no > len(GAME_MODES) - 1:
            mode_no = 0
        global window, scores
        mode = GAME_MODES[mode_no]
        scores[mode].sort(reverse=True)
        scores[mode] = scores[mode][:7] # upto 7 highscores stored

        clearscreens()

        score_screen = Frame(window, bg="black")
        screens.append(score_screen)
        score_screen.pack(fill=BOTH, expand=True)

        screen_title = Label(score_screen,
                             text="Highscores", font=("Arial", 30, "bold"),
                             fg="green", bg="black")
        screen_title.place(relx=0.32, rely=0.1)

        mode_label = Label(score_screen,
                           text=mode, font=("Arial", 15, "bold"),
                           fg="light green", bg="black")
        mode_label.place(relx=0.5, rely=0.22, anchor=CENTER)

        def prevmode():
            showmode(mode_no - 1)
        def nextmode():
            showmode(mode_no + 1)
        previous_button = Button(score_screen,
                                 borderwidth=0,
                                 text="<", font=("Arial", 10, "bold"),
                                 fg="white", bg="black", activebackground="light grey",
                                 height=1, width=1,
                                 command=prevmode)
        previous_button.place(relx=0.3, rely=0.2)

        next_button = Button(score_screen,
                             borderwidth=0,
                             text=">", font=("Arial", 10, "bold"),
                             fg="white", bg="black", activebackground="light grey",
                             height=1, width=1,
                             command=nextmode)
        next_button.place(relx=0.7, rely=0.2)

        rank_header = Label(score_screen,
                            text="Rank", font=("Arial", 15, "bold"),
                            fg="grey", bg="black")
        rank_header.place(relx=0.25, rely=0.25)

        score_header = Label(score_screen,
                             text="Score", font=("Arial", 15, "bold"),
                             fg="grey", bg="black")
        score_header.place(relx=0.65, rely=0.25)

        back_button = Button(score_screen,
                             borderwidth=3, relief=RIDGE,
                             text="Back", font=("Arial", 15, "bold"),
                             fg="white", bg="grey", activebackground="light grey",
                             width=5,
                             command=displaymenu)
        back_button.place(relx=0.03, rely=0.9)

        if len(scores[mode]) == 0:
            scores[mode] = ["N.A"] * 3 # Fill with placeholders

        rank_map = ["gold", "thistle3", "sienna4"]

        for index in range(len(scores[mode])):
            score = scores[mode][index]
            rank = index + 1
            if rank <= len(rank_map):
                color = rank_map[rank - 1]
            else:
                color = "white"
            rank_header = Label(score_screen,
                                text=rank, font=("Arial", 15, "bold"),
                                fg=color, bg="black")
            rank_header.place(relx=0.28, rely=0.25 + rank * 0.075)

            score_header = Label(score_screen,
                                 text=score, font=("Arial", 15, "bold"),
                                 fg=color, bg="black")
            score_header.place(relx=0.66, rely=0.25 + rank * 0.075)

        if scores[mode] == ["N.A"] * 3:
            scores[mode] = [] # Placeholders only temporary
    showmode(0)

def displaymenu():
    global window, scores
    clearscreens()

    menu = Frame(window, bg="black")
    screens.append(menu)
    menu.pack(fill=BOTH, expand=True)

    buttons = {
        "Play":displaymodes,
        "Scores": displayscore
    }
    game_title = Label(menu,
                       text="Snake Game", font=("Arial", 30, "bold"),
                       fg="green", bg="black")
    game_title.place(relx=0.29, rely=0.2)

    n = 0
    for buttonName in buttons:
        command = buttons[buttonName]
        button = Button(menu,
                        borderwidth=3, relief=RIDGE,
                        text=buttonName, font=("Arial", 20, "bold"),
                        fg="black", bg="green", activebackground="light green",
                        width=7,
                        command=command)
        button.place(relx=.375, rely=0.4 + 0.145 * n)
        n += 1

    # Intialise scores
    for mode in GAME_MODES:
        scores[mode] = []
