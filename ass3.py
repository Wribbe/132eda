#!/usr/bin/env python3

import random
import sys

# Grid structure:
# ---------------
#   grid = [
#           4, # Num rows.
#           4, # Num columns.
#           [[N,W,S,E],[...]], # Wall indices matrix.
#           [[N,W,S,E],[...]], # Transition probabilities matrix.
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
grid_walls=2; grid_transitions=3; grid_sensor=4

current_view = grid_transitions
#current_view = grid_sensor

grid = [[]]

def grid_get(rows, columns):

    grid = [rows, columns]
    grid_wall_matrix = []

    grid_heading_probablities = [[[0.0]*4]*columns for _ in range(rows)]
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
    # Add heading probabilities.
    grid.append(grid_heading_probablities)
    # Add sensor values.
    grid.append(grid_sensor_values)

    return grid

def grid_wall_at(x, y, heading):
    return grid[grid_walls][y][x][heading]

def print_clear():
    print('\n'*200)

def print_grid(grid, robot_x, robot_y, robot_heading):

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

    def print_cap():
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

                if index_column == robot_x and index_row == robot_y:
                    tile_status = "R"
                    if robot_heading == E:
                        tile_status = tile_status+">"
                    elif robot_heading == W:
                        tile_status = "<"+tile_status
                    elif robot_heading == N:
                        tile_status = tile_status+"^"
                    elif robot_heading == S:
                        tile_status = tile_status+"V"
                else:
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
        print_cap()
        print_body(index_row)

    for index_row in range(grid_rows):
        print_row(index_row)
    print_cap()

def robot_step(x, y, heading):

    def new_coords(x, y, heading):
        adjustments = {
            N : (x, y-1),
            E : (x+1, y),
            S : (x, y+1),
            W : (x-1, y),
        }
        return adjustments[heading]

    return new_coords(x, y, heading)

PROB_FACING = 0.7

def get_available_headings(x, y, heading):
    return [h for h in [N,E,S,W] if not robot_faces_wall(x, y, h)]

def robot_new_heading(x, y, heading):
    if (robot_faces_wall(x, y, heading) or random.random() > PROB_FACING):
        return random.choice(get_available_headings(x, y, heading))
    return heading

def robot_faces_wall(x, y, heading):
    return  grid_wall_at(x, y, heading)

def robot_print_status(x, y, heading):
    heading_string = {
            N : "N",
            E : "E",
            S : "S",
            W : "W",
        }
    print("({0},{1}:{2}) -- x: {0}, y:{1} heading: {2}.".format(x, y, heading_string[heading]))

def get_next_tile_by_heading(grid, x, y, heading):
    new_x, new_y = robot_step(x, y, heading)
    return grid[new_y][new_x]

def martix_get_transitions(grid, x, y, heading):
    rows, cols = (grid[0], grid[1])
    matrix_trans = [ [[0.0]*4 for _ in range(cols) ] for _ in range(rows)]
    available_headings = get_available_headings(x, y, heading)
    prob_left = 1.0
    # See if the current heading is available.
    if heading in available_headings:
        prob_left -= PROB_FACING
        get_next_tile_by_heading(matrix_trans, x, y, heading)[heading] = PROB_FACING
        available_headings.remove(heading)
    # Split remaining probability among the other possible headings.
    prob_split = prob_left / len(available_headings)
    for h in available_headings:
        get_next_tile_by_heading(matrix_trans, x, y, h)[h] = prob_split
    return matrix_trans

def main(args):

    global grid

    grid_width = 4
    grid_height = 4

    grid = grid_get(grid_width, grid_height)

    robot_pos_x = random.choice(range(0,grid_width))
    robot_pos_y = random.choice(range(0,grid_height))
    robot_heading = random.choice([N,W,S,E])

    transitions = martix_get_transitions(grid, robot_pos_x, robot_pos_y,
            robot_heading)
    grid[grid_transitions] = transitions

    print_grid(grid, robot_pos_x, robot_pos_y, robot_heading)
    robot_print_status(robot_pos_x, robot_pos_y, robot_heading)
    #for _ in range(10):
    #    robot_heading = robot_new_heading(robot_pos_x, robot_pos_y,
    #            robot_heading)
    #    robot_pos_x, robot_pos_y = robot_step(robot_pos_x, robot_pos_y,
    #            robot_heading)
    #    robot_print_status(robot_pos_x, robot_pos_y, robot_heading)
    #robot_step()

if __name__ == "__main__":
    main(sys.argv[1:])
