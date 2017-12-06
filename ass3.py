#!/usr/bin/env python3

import sys

# Grid structure:
# ---------------
#   grid = [
#           4, # Num rows.
#           4, # Num columns.
#           [[N,W,S,E],], # Wall indices matrix.
#       ]

# Heading enumerations.
N=0
W=1
S=2
E=3

def grid_get(rows, columns):

    grid = [rows, columns]
    wall_matrix = []

    for index_row in range(rows):
        wall_matrix_row = []
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
            wall_matrix_row.append(current_tile)
        wall_matrix.append(wall_matrix_row)

    # Add wall matrix to grid data.
    grid.append(wall_matrix)

    return grid


def main(args):

    grid = grid_get(4,4)
    print(grid)

if __name__ == "__main__":
    main(sys.argv[1:])
