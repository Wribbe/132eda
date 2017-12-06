#!/usr/bin/env python3

import sys

# Grid structure:
# ---------------
#   grid = [
#           4, # Num rows.
#           4, # Num columns.
#           [[N,W,S,E],[...]], # Wall indices matrix.
#           [[N,W,S,E],[...]], # Directional probabilities matrix.
#           [x.xx,[...]],      # Sensor value matrix.
#       ]


rep_tile = """
 ----------------
|  L   0.7       |
|                |
|                |
| 0.0   T    0.0 |
|                |
|                |
|      0.3       |
 ----------------
""".strip()

# Heading enumerations.
N=0; W=1; S=2; E=3

def grid_get(rows, columns):

    grid = [rows, columns]
    grid_wall_matrix = []

    grid_direction_probablities = [[[0.0]*4]*columns for _ in range(rows)]
    grid_sensor_values = [[0.0]*columns for _ in range(rows)]

    for index_row in range(rows):
        grid_wall_matrix_row = []
        for index_col in range(columns):
            current_tile = [False]*4
            if index_col == 0: # First column has wall to West.
                current_tile[W] = True
            if index_col == columns-1: # Last column has wall to East.
                current_tile[E] = True
            if index_row == 0: # First row has wall to North.
                current_tile[N] = True
            if index_row == rows-1: # Last row has wall to South.
                current_tile[S] = True
            grid_wall_matrix_row.append(current_tile)
        grid_wall_matrix.append(grid_wall_matrix_row)

    # Add wall matrix to grid data.
    grid.append(grid_wall_matrix)
    # Add directional probabilities.
    grid.append(grid_direction_probablities)
    # Add sensor values.
    grid.append(grid_sensor_values)

    return grid

def print_clear():
    print('\n'*200)

def print_grid(grid):

    tile_width = len(rep_tile.splitlines()[0])
    tile_height = len(rep_tile.splitlines())-2

    grid_rows = grid[0]
    grid_columns = grid[1]

    def print_end_line():
        print("")

    def print_top():
        print(" ", end='')
        for _ in range(grid_columns):
            print("{} ".format('-'*(tile_width-1)), end='')
        print_end_line()

    def print_body():
        for _ in range(tile_height):
            print("|", end ='')
            for _ in range(grid_rows):
                print("{}|".format(' '*(tile_width-1)), end='')
            print_end_line()

    def print_row(index_row):
        print_top()
        print_body()

    for index_row in range(grid_rows):
        print_row(index_row)
    print_top()

def main(args):

    grid = grid_get(4,4)
    print_grid(grid)

if __name__ == "__main__":
    main(sys.argv[1:])
