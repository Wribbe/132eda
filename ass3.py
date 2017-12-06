#!/usr/bin/env python3

import sys

# Grid structure:
# ---------------
#   grid = [
#           4, # Num rows.
#           4, # Num columns.
#           [[N,W,S,E],[...]], # Wall indices matrix.
#           [[N,W,S,E],[...]], # Directional probabilities matrix.
#           [[N,W,S,E],[...]], # Sensor data values.
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
# Data enumerations.
grid_walls=2; grid_directional=3; grid_sensor=4

current_view = grid_directional
current_view = grid_sensor

def grid_get(rows, columns):

    grid = [rows, columns]
    grid_wall_matrix = []

    grid_direction_probablities = [[[0.0]*4]*columns for _ in range(rows)]
    grid_sensor_values = [[[0.0]+[""]*3]*columns for _ in range(rows)]

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

    tile_body_width = tile_width-1

    grid_rows = grid[0]
    grid_columns = grid[1]

    body_index_north = 0
    body_index_south = (tile_height-1)
    body_index_middle = body_index_south/2

    format_body_north = "{{: ^{}.4}}|".format(tile_body_width)
    format_body_south = format_body_north

    format_body_middle_space = int((tile_body_width-3)/2)
    format_body_middle_left = "{{: <{}.4}}".format(format_body_middle_space)
    format_body_middle_center = "{: ^3}"
    format_body_middle_right = "{{: >{}.4}}".format(format_body_middle_space)
    format_body_middle = "{}{}{}|".format(format_body_middle_left,
            format_body_middle_center,
            format_body_middle_right)

    def print_end_line():
        print("")

    def print_top():
        print(" ", end='')
        for _ in range(grid_columns):
            print("{} ".format('-'*(tile_body_width)), end='')
        print_end_line()

    def print_body(index_row):
        for index_body_row in range(tile_height):
            print("|", end ='')
            for index_column in range(grid_columns):
                tile_data = grid[current_view][index_row][index_column]

                tile_val_north = tile_data[N]
                tile_val_east = tile_data[E]
                tile_val_south = tile_data[S]
                tile_val_west = tile_data[W]

                tile_status = ""

                if index_body_row == body_index_north:
                    print(format_body_north.format(tile_val_north), end='')
                elif index_body_row == body_index_middle:
                    print(format_body_middle.format(tile_val_west, tile_status,
                        tile_val_east), end='')
                elif index_body_row == body_index_south:
                    print(format_body_south.format(tile_val_south), end='')
                else:
                    print("{}|".format(' '*(tile_body_width)), end='')
            print_end_line()

    def print_row(index_row):
        print_top()
        print_body(index_row)

    for index_row in range(grid_rows):
        print_row(index_row)
    print_top()

def main(args):

    grid = grid_get(4,4)
    print_grid(grid)

if __name__ == "__main__":
    main(sys.argv[1:])
