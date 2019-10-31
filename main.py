"""""""""""""""""""""""""""""
#  A* PATHFINDER ALGORITHM  #
#  Object Oriented Version  #
#  using SimpleGraphics.py  #
"""""""""""""""""""""""""""""

import SimpleGraphics
import random
import math

WINDOW_SIZE = 500
CELL_SIZE = 10
OBSTACLE_PROBABILITY = 0.3

""" class that represents a cell in the grid """
class Cell:

    def __init__(self, size, x, y, is_obstacle=False):
        self.size = size                # size of the cell
        self.x = x                      # cell's x position in the grid
        self.y = y                      # cell's y position in the grid
        self.is_obstacle = is_obstacle  # type of the cell (empty / obstacle)
        self.neighbors = []             # list of the cell's neighbors
        self.previous = None            # previous cell in the path
        self.f = 0                      # cell's f cost (f(cell) = g(cell) + h(cell))
        self.g = 0                      # cell's g cost (distance from the start cell)
        self.h = 0                      # cell's h cost (estimated distance to the end cell)

    """ displays a cell by rendering a rectangle of specified color (r, g, b) """
    def render_cell(self, r, g, b):
        SimpleGraphics.setFill(r,g,b)
        SimpleGraphics.rect(self.x * self.size , self.y * self.size, self.size, self.size)

""" class that represents a grid """
class Grid:

    def __init__(self, window_size, cell_size):
        self.cell_size = cell_size                                                                  # size of the grid cell
        self.grid_size = window_size // cell_size                                                   # size of the grid
        self.cell_matrix = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]   # 2D list of the grid cells
        self.open_list = []                                                                         # cells left to evaluate
        self.closed_list = []                                                                       # already evaluated cells
        self.grid_img = SimpleGraphics.createImage(WINDOW_SIZE, WINDOW_SIZE)                        # image of the grid

    """ constructs a grid with the specified obstacle probability """
    def construct_grid(self, obstacle_probability):
        for x in range(len(self.cell_matrix)):
            for y in range(len(self.cell_matrix[0])):

                self.cell_matrix[x][y] = Cell(self.cell_size, x, y)

                if random.random() < obstacle_probability:
                    self.cell_matrix[x][y].is_obstacle = True

        self.cell_matrix[0][0].is_obstacle = False
        self.add_cell_neighbors()
        self.generate_image()

    """ creates an image of the grid to optimize the rendering """
    def generate_image(self):
        for x in range(WINDOW_SIZE):
            for y in range(WINDOW_SIZE):
                if self.cell_matrix[x // self.cell_size][y // self.cell_size].is_obstacle:
                    SimpleGraphics.putPixel(self.grid_img, x, y, 0, 0, 0)
                else:
                    SimpleGraphics.putPixel(self.grid_img, x, y, 255, 255, 255)

    """ determines the neighbours of each cell of the grid """
    def add_cell_neighbors(self):
        for x in range(len(self.cell_matrix)):
            for y in range(len(self.cell_matrix[0])):
                for i in range(x - 1, x + 2):
                    for j in range(y - 1, y + 2):
                        if 0 <= i < self.grid_size and 0 <= j < self.grid_size and (i != x or j != y):
                            self.cell_matrix[x][y].neighbors.append(self.cell_matrix[i][j])

    """ renders an image of the grid """
    def render_grid(self):
        SimpleGraphics.drawImage(self.grid_img, 0, 0)

""" heuristic that computes the euclidean distance between two cells """
def heuristic(cell_1, cell_2):
    return math.sqrt(pow(cell_2.x - cell_1.x, 2) + pow(cell_2.y - cell_1.y, 2))

""" computes the shortest path between start and end cells in a grid """
def find_path():
    # create a grid
    grid = Grid(WINDOW_SIZE, CELL_SIZE)
    grid.construct_grid(OBSTACLE_PROBABILITY)

    # set start and end cells
    start_cell = grid.cell_matrix[0][0]
    end_cell = grid.cell_matrix[grid.grid_size - 1][grid.grid_size - 1]

    # initialize open and closed lists
    open_list = [start_cell]
    closed_list = []

    found_path = False

    # algorithm keeps executing until open list becomes empty
    while len(open_list) > 0:

        if SimpleGraphics.closed():
            return

        next_cell_index = 0

        # find the cell with lowest f cost
        for i in range(len(open_list)):
            if open_list[i].f < open_list[next_cell_index].f:
                next_cell_index = i

        # cell with lowest f cost becomes the current cell
        current_cell = open_list[next_cell_index]

        # path between start and end cells is found
        if current_cell == end_cell:
            found_path = True

        # remove current cell from the open list and add it to the closed list
        open_list.remove(current_cell)
        closed_list.append(current_cell)

        # evaluate the neighboring cells
        for neighbor_cell in current_cell.neighbors:

            # neighbor is considered if it is not in closed set and is not an obstacle
            if neighbor_cell not in closed_list and not neighbor_cell.is_obstacle:

                # calculate a temporary g cost of neighbor cell based on the g cost of current cell
                temp_neighbor_cell_g = current_cell.g + heuristic(neighbor_cell, current_cell)

                found_new_path = False

                # if the neighbor is already in the open list, compare its temporary and current g cost
                if neighbor_cell in open_list:
                    # if the temporary g cost of the neighbor is smaller than its current g score, the shorter path is found.
                    if neighbor_cell.g > temp_neighbor_cell_g:
                        found_new_path = True
                # Otherwise, add a newly discovered cell to the open list
                else:
                    open_list.append(neighbor_cell)
                    found_new_path = True

                # if shorter path to the neighbor is found (or a new cell is discovered), update the neighbor's f, g and h costs and set its previous cell to the current cell
                if found_new_path:
                    neighbor_cell.g = temp_neighbor_cell_g
                    neighbor_cell.h = heuristic(neighbor_cell, end_cell)
                    neighbor_cell.f = neighbor_cell.g + neighbor_cell.h
                    neighbor_cell.previous = current_cell


        # render a grid and cells in open and closed lists
        SimpleGraphics.clear()

        grid.render_grid()

        for cell in open_list:
            cell.render_cell(0,255,0)

        for cell in closed_list:
            cell.render_cell(255,0,0)

        # build a path from the start to current cell
        current_path = []
        temp = current_cell
        current_path.append(temp)

        while temp.previous is not None:
            current_path.append(temp.previous)
            temp = temp.previous

        # render a path from the start to current cell
        for cell in current_path:
            cell.render_cell(0,0,255)

        SimpleGraphics.update()

        # path between start and end cells is found, terminate the algorithm
        if found_path:
            break

    if found_path:
        print("Done")
    else:
        print("No solution")

def main():
    setup()
    find_path()

""" SimpleGraphics setup """
def setup():
    SimpleGraphics.setAutoUpdate(False)
    SimpleGraphics.resize(WINDOW_SIZE, WINDOW_SIZE)
    SimpleGraphics.setWindowTitle("A* Pathfinding Algorithm")

if __name__ == "__main__":
    main()