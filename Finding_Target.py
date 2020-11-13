import numpy as np
from Environment import Cell, Environment
import random


class Rambo:
    def __init__(self, env):
        self.env = env
        self.grid_size = self.env.n
        self.rambo_grid = [[Cell(j, i) for i in range(self.grid_size)] for j in range(self.grid_size)]
        self.search_count = 0

    def search(self, q_cell):
        if not self.isCellValid(q_cell.row, q_cell.col):
            return
        self.search_count += 1
        q_cell.terrain = self.env.grid[q_cell.row][q_cell.col].terrain
        target = self.env.grid[q_cell.row][q_cell.col].target
        # checking for target
        if q_cell.terrain == "flat":
            a = int(np.random.binomial(1, 0.1, 1))   # probability of failure is 0.1, so a = 1 only with 0.1 prob
            if (a != 1 and not target) or (a == 1):
                self.rambo_grid[q_cell.row][q_cell.col].belief = 0.1 * q_cell.belief
                self.rambo_grid[q_cell.row][q_cell.col].belief2 = 0.9 * q_cell.belief2
                return "failure"
            elif a != 1 and target:
                return "success"
        elif q_cell.terrain == "hilly":
            a = int(np.random.binomial(1, 0.3, 1))
            if (a != 1 and not target) or (a == 1):
                self.rambo_grid[q_cell.row][q_cell.col].belief = 0.3 * q_cell.belief
                self.rambo_grid[q_cell.row][q_cell.col].belief2 = 0.7 * q_cell.belief2
                return "failure"
            elif a != 1 and target:
                return "success"
        elif q_cell.terrain == "forest":
            a = int(np.random.binomial(1, 0.7, 1))
            if (a != 1 and not target) or (a == 1):
                self.rambo_grid[q_cell.row][q_cell.col].belief = 0.7 * q_cell.belief
                self.rambo_grid[q_cell.row][q_cell.col].belief2 = 0.3 * q_cell.belief2
                return "failure"
            elif a != 1 and target:
                return "success"
        elif q_cell.terrain == "caves":
            a = int(np.random.binomial(1, 0.9, 1))
            if (a != 1 and not target) or (a == 1):
                self.rambo_grid[q_cell.row][q_cell.col].belief = 0.9 * q_cell.belief
                self.rambo_grid[q_cell.row][q_cell.col].belief2 = 0.1 * q_cell.belief2
                return "failure"
            elif a != 1 and target:
                return "success"

    # search for target and if failed return failure and update belief, else return success if found.
    def rule1(self):
        # Initial belief of target in the cell
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.rambo_grid[row][col].belief = 1 / (self.grid_size * self.grid_size)
        while 1:
            be = 0
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    rambo_cell = self.rambo_grid[row][col]
                    if rambo_cell.belief > be:
                        be = rambo_cell.belief
                        search_cell = rambo_cell
            if self.search(search_cell) == "success":
                break
        return self.search_count

    def rule2(self):
        # Assigning the terrain and initial belief of finding the target in the cell for that terrain
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.env.grid[row][col].terrain == "caves":
                    self.rambo_grid[row][col].belief2 = 0.1
                elif self.env.grid[row][col].terrain == "forest":
                    self.rambo_grid[row][col].belief2 = 0.3
                elif self.env.grid[row][col].terrain == "hilly":
                    self.rambo_grid[row][col].belief2 = 0.7
                elif self.env.grid[row][col].terrain == "flat":
                    self.rambo_grid[row][col].belief2 = 0.9

        while 1:
            be2 = 0
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    rambo_cell = self.rambo_grid[row][col]
                    if rambo_cell.belief2 > be2:
                        be2 = rambo_cell.belief2
                        search_cell = rambo_cell
            if self.search(search_cell) == "success":
                break
        return [self.search_count, search_cell.terrain]

    def isCellValid(self, row: int, col: int):
        return (row >= 0) and (row < self.grid_size) and (col >= 0) and (col < self.grid_size)


# env = Environment(50)
# print(Rambo(env).rule2())

s = 0
for i in range(10):
    env = Environment(50)
    ab = Rambo(env).rule2()
    print(ab[0], ab[1])
    s += ab[0]
print(s/10)

