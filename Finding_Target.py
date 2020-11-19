import numpy as np
from Environment import Cell, Environment
from pprint import pprint
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
        # checking for target in the given terrain
        if q_cell.terrain == "flat":
            a = int(np.random.binomial(1, 0.1, 1))  # probability of failure is 0.1, so a = 1 only with 0.1 prob
            if (a != 1 and not target) or (a == 1):
                # update the belief values if target is not found or for false negative.
                self.rambo_grid[q_cell.row][q_cell.col].belief = 0.1 * q_cell.belief
                self.rambo_grid[q_cell.row][q_cell.col].belief2 = 0.9 * q_cell.belief
                return "failure"
            elif a != 1 and target:
                return "success"
        elif q_cell.terrain == "hilly":
            a = int(np.random.binomial(1, 0.3, 1))
            if (a != 1 and not target) or (a == 1):
                self.rambo_grid[q_cell.row][q_cell.col].belief = 0.3 * q_cell.belief
                self.rambo_grid[q_cell.row][q_cell.col].belief2 = 0.7 * q_cell.belief
                return "failure"
            elif a != 1 and target:
                return "success"
        elif q_cell.terrain == "forest":
            a = int(np.random.binomial(1, 0.7, 1))
            if (a != 1 and not target) or (a == 1):
                self.rambo_grid[q_cell.row][q_cell.col].belief = 0.7 * q_cell.belief
                self.rambo_grid[q_cell.row][q_cell.col].belief2 = 0.3 * q_cell.belief
                return "failure"
            elif a != 1 and target:
                return "success"
        elif q_cell.terrain == "caves":
            a = int(np.random.binomial(1, 0.9, 1))
            if (a != 1 and not target) or (a == 1):
                self.rambo_grid[q_cell.row][q_cell.col].belief = 0.9 * q_cell.belief
                self.rambo_grid[q_cell.row][q_cell.col].belief2 = 0.1 * q_cell.belief
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
                    if rambo_cell.belief > be:  # selecting a cell with the highest belief
                        be = rambo_cell.belief
                        search_cell = rambo_cell
            if self.search(search_cell) == "success":
                break
        return self.search_count

    def rule2(self):
        # Assigning the terrain and initial belief of finding the target in the cell for that terrain
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.rambo_grid[row][col].belief = 1 / (self.grid_size * self.grid_size)

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.env.grid[row][col].terrain == "caves":
                    self.rambo_grid[row][col].belief2 = 0.1 * self.rambo_grid[row][col].belief
                elif self.env.grid[row][col].terrain == "forest":
                    self.rambo_grid[row][col].belief2 = 0.3 * self.rambo_grid[row][col].belief
                elif self.env.grid[row][col].terrain == "hilly":
                    self.rambo_grid[row][col].belief2 = 0.7 * self.rambo_grid[row][col].belief
                elif self.env.grid[row][col].terrain == "flat":
                    self.rambo_grid[row][col].belief2 = 0.9 * self.rambo_grid[row][col].belief

        while 1:
            be2 = 0
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    rambo_cell = self.rambo_grid[row][col]
                    if rambo_cell.belief2 > be2:    # selecting a cell with the highest belief 2
                        be2 = rambo_cell.belief2
                        search_cell = rambo_cell
            if self.search(search_cell) == "success":
                break
        return [self.search_count, search_cell.terrain]

    def BasicAgent1(self):
        # Initial beliefs of target in the cell
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.rambo_grid[row][col].belief = 1 / (self.grid_size * self.grid_size)
        # initially pick a cell at random
        curr_cell = self.rambo_grid[random.randrange(0, len(self.rambo_grid))][
            random.randrange(0, len(self.rambo_grid))]

        if self.search(curr_cell) == "success":
            return [self.search_count, curr_cell.terrain]
        while 1:
            # neighbours
            be = 0
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if not self.isCellValid(curr_cell.row + i, curr_cell.col + j):
                        continue
                    # neighbours of the current cell
                    neighbour = self.rambo_grid[curr_cell.row + i][curr_cell.col + j]
                    if neighbour.belief > be:   # taking the neighbour cell with the highest belief according to rule 1
                        be = neighbour.belief
                        target_cell = neighbour
            if self.search(target_cell) == "success":
                break
            curr_cell = target_cell
        return [self.search_count, target_cell.terrain]

    def BasicAgent2(self):
        # Initial beliefs of target in the cell
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.rambo_grid[row][col].belief = 1 / (self.grid_size * self.grid_size)

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.env.grid[row][col].terrain == "caves":
                    self.rambo_grid[row][col].belief2 = 0.1 * self.rambo_grid[row][col].belief
                elif self.env.grid[row][col].terrain == "forest":
                    self.rambo_grid[row][col].belief2 = 0.3 * self.rambo_grid[row][col].belief
                elif self.env.grid[row][col].terrain == "hilly":
                    self.rambo_grid[row][col].belief2 = 0.7 * self.rambo_grid[row][col].belief
                elif self.env.grid[row][col].terrain == "flat":
                    self.rambo_grid[row][col].belief2 = 0.9 * self.rambo_grid[row][col].belief
        # initially pick a cell at random
        curr_cell = self.rambo_grid[random.randrange(0, len(self.rambo_grid))][
            random.randrange(0, len(self.rambo_grid))]

        if self.search(curr_cell) == "success":
            return [self.search_count, curr_cell.terrain]

        while 1:
            # neighbours
            be = 0
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if not self.isCellValid(curr_cell.row + i, curr_cell.col + j):
                        continue
                    # neighbours of the current cell and we take that cell too
                    neighbour = self.rambo_grid[curr_cell.row + i][curr_cell.col + j]
                    if neighbour.belief2 > be:    # taking the neighbour cell with the highest belief 2
                        be = neighbour.belief2
                        target_cell = neighbour
            if self.search(target_cell) == "success":
                break
            curr_cell = target_cell
        return [self.search_count, target_cell.terrain]

    def BasicAgent3(self):
        # Initial beliefs of target in the cell
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.rambo_grid[row][col].belief = 1 / (self.grid_size * self.grid_size)

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.env.grid[row][col].terrain == "caves":
                    self.rambo_grid[row][col].belief2 = 0.1 * self.rambo_grid[row][col].belief
                elif self.env.grid[row][col].terrain == "forest":
                    self.rambo_grid[row][col].belief2 = 0.3 * self.rambo_grid[row][col].belief
                elif self.env.grid[row][col].terrain == "hilly":
                    self.rambo_grid[row][col].belief2 = 0.7 * self.rambo_grid[row][col].belief
                elif self.env.grid[row][col].terrain == "flat":
                    self.rambo_grid[row][col].belief2 = 0.9 * self.rambo_grid[row][col].belief
    # initially pick a cell at random
        curr_cell = self.rambo_grid[random.randrange(0, len(self.rambo_grid))][
            random.randrange(0, len(self.rambo_grid))]

        if self.search(curr_cell) == "success":
            return [self.search_count, curr_cell.terrain]

        while 1:
            score = 10000000  # initialization a random high value for the score
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    rambo_cell = self.rambo_grid[row][col]
                    # finding the manhattan distance
                    rambo_cell.distance = 1 + abs(rambo_cell.row - curr_cell.row) + abs(rambo_cell.col - curr_cell.col)
                    if rambo_cell.distance != 0 and rambo_cell.belief2 != 0:
                        # calculating the scores
                        rambo_cell.score = rambo_cell.distance / rambo_cell.belief2
                    if rambo_cell.score < score:    # taking the minimal score and searching that cell for the target
                        score = rambo_cell.score
                        search_cell = rambo_cell
            if self.search(search_cell) == "success":
                break
            curr_cell = search_cell
        return [self.search_count, search_cell.terrain]
    def Improved_Agent(self):
        # Initial beliefs of target in the cell
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                self.rambo_grid[row][col].belief = 1 / (self.grid_size * self.grid_size)

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.env.grid[row][col].terrain == "caves":
                    self.rambo_grid[row][col].belief2 = 0.1 * self.rambo_grid[row][col].belief
                elif self.env.grid[row][col].terrain == "forest":
                    self.rambo_grid[row][col].belief2 = 0.3 * self.rambo_grid[row][col].belief
                elif self.env.grid[row][col].terrain == "hilly":
                    self.rambo_grid[row][col].belief2 = 0.7 * self.rambo_grid[row][col].belief
                elif self.env.grid[row][col].terrain == "flat":
                    self.rambo_grid[row][col].belief2 = 0.9 * self.rambo_grid[row][col].belief
        # initially pick a cell at random
        curr_cell = self.rambo_grid[random.randrange(0, len(self.rambo_grid))][
            random.randrange(0, len(self.rambo_grid))]

        if self.search(curr_cell) == "success":
            return [self.search_count, curr_cell.terrain]

        while 1:
            score = 10000000  # initialization a random high value for the score
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    rambo_cell = self.rambo_grid[row][col]
                    # finding the manhattan distance
                    rambo_cell.distance = 1 + abs(rambo_cell.row - curr_cell.row) + abs(rambo_cell.col - curr_cell.col)
                    if rambo_cell.distance != 0 and rambo_cell.belief2 != 0:
                        # calculating the scores
                        rambo_cell.score = (rambo_cell.distance / rambo_cell.belief2) * (3/7)
                    if rambo_cell.score < score:  # taking the minimal score and searching that cell for the target
                        score = rambo_cell.score
                        search_cell = rambo_cell
            if self.search(search_cell) == "success":
                break
            curr_cell = search_cell
        return [self.search_count, search_cell.terrain]
    # checking if the cell is valid i.e. if the row and col values are in the boundaries

    def isCellValid(self, row: int, col: int):
        return (row >= 0) and (row < self.grid_size) and (col >= 0) and (col < self.grid_size)


# env = Environment(50)
# print(Rambo(env).rule2())

for j in range(1):
    s = 0
    for i in range(1000):
        env = Environment(30)
        ab = Rambo(env).Improved_Agent()
        s += ab[0]
    print(s / 1000)
#