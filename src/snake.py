'''
Snake object, as independent as possible
'''
import random
from settings import *

def obj(**data):
    '''
    Make object and fill data
    '''
    return data

class Snake:
    '''
    Handles snake construction, movement
    '''
    def __init__(self, window):
        # Snake states, properties
        self.state = "INACTIVE"
        self.props = {
            'movedir': None,
            'step': None,
            'multiplier': None,
            'powerups': {}
        }

        # Snake cell data
        self.cells = {
            'head': None,
            'body': [],
            'tail': None,
            'positions': [],
            'n': 0
        }

        # Interface data
        self.window = window
  
    def create(self):
        '''
        Create the snake and fill cell data
        '''
        head_pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        head_cell = obj(type="snakehead", pos=head_pos, next=None, previous=None)
        occupy(head_cell)
        snake.update({"head":head_cell, "cells_occupied":1, "positions":[head_pos]})

        while snake["cells_occupied"] < MIN_LENGTH:
            if snake["cells_occupied"] == 1:
                latest = snake["head"]
            else:
                latest = snake["body"][-1]

            pos = random.choice(neighbours(latest))
            while pos in snake["positions"]:
                pos = random.choice(neighbours(latest))
            snake["positions"].append(pos)

            cell = makecell("snakebody", pos, {"next": latest, "previous":None})
            occupy(cell)

            latest.update({"previous":cell})
            snake["cells_occupied"] += 1

            if snake["cells_occupied"] == MIN_LENGTH:
                snake["tail"] = cell
            else:
                snake["body"].append(cell)
                if snake["cells_occupied"] == 2:
                    snake["head"]["previous"] = cell