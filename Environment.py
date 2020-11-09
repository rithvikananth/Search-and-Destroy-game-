import numpy as np
import random
from pprint import pprint


class Cell:
    def __init__(self, row, col):
        # Row number of cell in the grid
        self.row = row
        # Column number of cell in the grid
        self.col = col
        # terrain type of the cell
        self.terrain = None
        # target
        self.target = False


class Environment:
    def __init__(self, grid_size):
        # Initializing with empty grid
        self.grid = None
        # Dimension of the grid specified
        self.n = grid_size
        # creating cell objects
        self.cell = [[Cell(j, i) for i in range(self.n)] for j in range(self.n)]

    def generate_grid(self):
        # Initializing with all zeroes
        self.grid = np.zeros((self.n, self.n))
        self.assign_terrain()
        self.assign_target()

    def assign_terrain(self):
        count = 0
        # add terrains
        flat_count = self.n * self.n * 0.2
        hilly_count = self.n * self.n * 0.3
        forested_count = self.n * self.n * 0.3
        while count < flat_count:
            # Choosing a random cell
            row = random.randrange(0, self.n)
            col = random.randrange(0, self.n)
            c = self.cell[row][col]
            # If not already chosen, assign a terrain
            if c.terrain is None:
                c.terrain = "flat"
                count += 1
        count = 0
        while count < hilly_count:
            row = random.randrange(0, self.n)
            col = random.randrange(0, self.n)
            c = self.cell[row][col]
            # If not already chosen, assign a terrain
            if c.terrain is None:
                c.terrain = "hilly"
                count += 1
        count = 0
        while count < forested_count:
            row = random.randrange(0, self.n)
            col = random.randrange(0, self.n)
            c = self.cell[row][col]
            # If not already chosen, assign a terrain
            if c.terrain is None:
                c.terrain = "forest"
                count += 1
        # for remaining, assign a terrain as caves
        for row in range(self.n):
            for col in range(self.n):
                c = self.cell[row][col]
                if c.terrain is None:
                    c.terrain = "caves"

    def assign_target(self):
        row = random.randrange(0, self.n)
        col = random.randrange(0, self.n)
        c = self.cell[row][col]
        c.target = True
'''
    def check(self):
        c1 = 0
        c2 = 0
        c3 = 0
        c4 = 0
        for row in range(self.n):
            for col in range(self.n):
                b = self.cell[row][col]
                if b.terrain == "caves":
                    c1 += 1
                if b.terrain == "forest":
                    c2 += 1
                if b.terrain == "hilly":
                    c3 += 1
                if b.terrain == "flat":
                    c4 += 1
                if b.target == True:
                    print(row, col)
        print("caves", c1)
        print("forr", c2)
        print("hilly", c3)
        print("flat", c4)
'''

# env = Environment(10)
# env.generate_grid()
# env.check()
