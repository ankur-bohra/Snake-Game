'''
Menu and other interface of game
'''
import json
from tkinter import *
from core import playgame
from settings import *

window = None
screens = []

def makewindow():
    '''
    Makes the main game window, created only once
    '''
    WIN_SIZE = GRID_SIZE * CELL_SIZE

    global window
    window = Tk()
    window.title("Snake Game")
    window.geometry(str(WIN_SIZE)+"x"+str(WIN_SIZE))
    window.resizable(width=False, height=False)

    return window

def clearscreens():
    '''
    Destroys all screens, called before making a new one.
    Screen frames are not stored indefinitely, they are created on demand.
    '''
    for screen in screens:
        screen.destroy()

def endgame(mode_step, score):
    '''
    Shows the death interface. Updates the score after awaiting for activity response.
    '''
    # Show a dying screen
    game = screens[-1]
    window.unbind("<KeyPress>")

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
    cont_label.place(relx=0.3, rely=0.85)

    player_label = Label(game,
                         text="Player:", font=("Arial", 15),
                         fg="white", bg="black")
    player_label.place(relx=0.45, rely=0.6, anchor=E)

    player_entry = Entry(game,
                         font=("Arial", 15),
                         width=15)
    player_entry.place(relx=0.48, rely=0.6, anchor=W)
    player_entry.insert(0, "Unknown")

    def resume(key):
        if key.keysym == "Return":
            if score > 0:
                with open("src/scores.json", "r+") as scores_file:
                    mode = GAME_MODES[GAME_STEPS.index(mode_step)]

                    scores = json.load(scores_file)
                    scores[mode].update({score: player_entry.get().title()})

                    scores_file.seek(0)
                    scores_file.truncate()
                    json.dump(scores, scores_file)

            clearscreens()
            displaymenu()
    window.bind("<Return>", resume)

def displaycredits(screen):
    '''
    Shows creator credits on any given screen (omitted in game)
    '''
    credits_label = Label(screen,
                          fg="grey", bg="black",
                          text="Made by Ankur Bohra in tkinter", font=("Arial", 10))
    credits_label.place(relx=0.5, rely=0.935, anchor=CENTER)

def displaymodes():
    '''
    Shows game mode/difficulty screen. Game is started with respective step from here.
    '''
    global window
    clearscreens()

    modes_screen = Frame(window, bg="black")
    screens.append(modes_screen)
    displaycredits(modes_screen)
    modes_screen.pack(fill=BOTH, expand=True)

    mode_title = Label(modes_screen,
                       text="Game Mode", font=("Arial", 30, "bold"),
                       fg="green", bg="black")
    mode_title.place(relx=0.5, rely=0.2, anchor=CENTER)

    def playmode(mode_step):
        '''
        Returns a callback but "injects" the mode_step variable into the environment
        '''
        def command():
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
        button.place(relx=0.5, rely=0.4 + index*0.12, anchor=CENTER)

    back_button = Button(modes_screen,
                         borderwidth=3, relief=RIDGE,
                         text="Back", font=("Arial", 15, "bold"),
                         fg="white", bg="grey", activebackground="light grey",
                         width=5,
                         command=displaymenu)
    back_button.place(relx=0.03, rely=0.9)

def displayscore():
    '''
    Shows stored scores sorted by mode and rank. Implements player filtered scores.
    '''
    def showmode(mode_no, filter_player):
        global window
        if mode_no > len(GAME_MODES) - 1:
            mode_no = 0
        mode = GAME_MODES[mode_no]
        with open("src/scores.json", "r+") as scores_file:
            scores = json.load(scores_file)
            sorted_scores = list(scores[mode])
            for index in range(len(sorted_scores)):
                score = sorted_scores[index]
                sorted_scores[index] = int(score)
            sorted_scores.sort(reverse=True)
            sorted_scores = sorted_scores[:7] # upto 7 highscores shown
            clearscreens()

            score_screen = Frame(window, bg="black")
            screens.append(score_screen)
            displaycredits(score_screen)
            score_screen.pack(fill=BOTH, expand=True)

            screen_title = Label(score_screen,
                                text="Highscores", font=("Arial", 30, "bold"),
                                fg="green", bg="black")
            screen_title.place(relx=0.5, rely=0.15, anchor=CENTER)

            mode_label = Label(score_screen,
                            text=mode, font=("Arial", 15, "bold"),
                            fg="light green", bg="black")
            mode_label.place(relx=0.5, rely=0.23, anchor=CENTER)

            def prevmode():
                showmode(mode_no - 1, filter_player)
            def nextmode():
                showmode(mode_no + 1, filter_player)
            previous_button = Button(score_screen,
                                    borderwidth=0,
                                    text="<", font=("Arial", 10, "bold"),
                                    fg="white", bg="black", activebackground="light grey",
                                    height=1, width=1,
                                    command=prevmode)
            previous_button.place(relx=0.3, rely=0.23, anchor=CENTER)

            next_button = Button(score_screen,
                                borderwidth=0,
                                text=">", font=("Arial", 10, "bold"),
                                fg="white", bg="black", activebackground="light grey",
                                height=1, width=1,
                                command=nextmode)
            next_button.place(relx=0.7, rely=0.23, anchor=CENTER)

            rank_header = Label(score_screen,
                                text="Rank", font=("Arial", 15, "bold"),
                                fg="grey", bg="black")
            rank_header.place(relx=0.2, rely=0.3, anchor=CENTER)

            score_header = Label(score_screen,
                                text="Score", font=("Arial", 15, "bold"),
                                fg="grey", bg="black")
            score_header.place(relx=0.5, rely=0.3, anchor=CENTER)

            name_header = Label(score_screen,
                                text="Player", font=("Arial", 15, "bold"),
                                fg="grey", bg="black")
            name_header.place(relx=0.8, rely=0.3, anchor=CENTER)


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

            placed = 0
            for index in range(len(sorted_scores)):
                score = sorted_scores[index]
                player = scores[mode][str(score)]
                if filter_player and player != filter_player:
                    continue
                rank = index + 1
                offset = (placed + 1) * 0.075
                if rank <= len(rank_map):
                    color = rank_map[rank - 1]
                else:
                    color = "white"
                rank_no = Label(score_screen,
                                    text=rank, font=("Arial", 15, "bold"),
                                    fg=color, bg="black")
                rank_no.place(relx=0.2, rely=0.3 + offset, anchor=CENTER)

                score = Label(score_screen,
                                    text=score, font=("Arial", 15, "bold"),
                                    fg=color, bg="black")
                score.place(relx=0.5, rely=0.3 + offset, anchor=CENTER)

                def filtergen(player):
                    def filtermode():
                        if filter_player == player:
                            showmode(mode_no, None)
                        else:
                            showmode(mode_no, player)
                    return filtermode

                name = Button(score_screen,
                                text=player, font=("Arial", 15, "bold"),
                                fg=color, bg="black",
                                command=filtergen(player))
                name.place(relx=0.8, rely=0.3 + offset, anchor=CENTER)

                index = index + 1
                placed = placed + 1

            if scores[mode] == ["N.A"] * 3:
                scores[mode] = [] # Placeholders only temporary
    showmode(0, None)

def displaymenu():
    '''
    Shows main menu, links all screens together.
    '''
    global window
    clearscreens()

    menu = Frame(window, bg="black")
    screens.append(menu)
    displaycredits(menu)
    menu.pack(fill=BOTH, expand=True)

    buttons = {
        "Play":displaymodes,
        "Scores": displayscore
    }
    game_title = Label(menu,
                       text="Snake Game", font=("Arial", 30, "bold"),
                       fg="green", bg="black")
    game_title.place(relx=0.5, rely=0.2, anchor=CENTER)

    n = 0
    for buttonName in buttons:
        command = buttons[buttonName]
        button = Button(menu,
                        borderwidth=3, relief=RIDGE,
                        text=buttonName, font=("Arial", 20, "bold"),
                        fg="black", bg="green", activebackground="light green",
                        width=7,
                        command=command)
        button.place(relx=0.5, rely=0.4 + 0.145 * n, anchor=CENTER)
        n += 1

    # Intialise scores
    with open("src/scores.json", "r+") as scores_file:
        if scores_file.read() == "":
            scores_file.write("{}") # Empty scores
        scores_file.seek(0)
        scores = json.load(scores_file)
        for mode in GAME_MODES:
            if mode not in scores:
                scores[mode] = {}
        scores_file.seek(0)
        scores_file.truncate()
        json.dump(scores, scores_file)
