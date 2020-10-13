'''
One program to combine all screens and the game
'''
from interface import *
from core import *

window = buildwindow()
displaymenu(window, playgame(window))

window.mainloop()
