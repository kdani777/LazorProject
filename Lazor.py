'''
Authors: Kunal Dani, Marina Morrow, Shyanne Salen
Last Modified: April 17th, 2019
Lazor Project
Software Carpentry
Solution Code

This is the code that solves the lazor grid for the android/apple app 
Lazors.This code requires a .bff file to be read in as the grid. This 
file must contain the grid. The grid must begin with GRID START followed
by the grid and then GRID STOP. Each spot in the grid must be separated
by space and the rows in their own rows. The grid should look similar to:

GRID START
o o o o
o o o o
o o o o
GRID STOP

The legend for the grid is:

x = no block allowed
o = blocks allowed
A = fixed reflect block
B = fixed opaque block
C = fixed refract block

Then, the .bff files must have the number of reflect, opaque, and refract
blocks. Each of these should be in their own line proceeded by their 
corresponding letter:

A = reflect block
B = opaque block
C = refract block

Then, the .bff files must have the lazors. Each lazor is on its own line proceeded
by the letter L. Then, the starting points and direction are given in 
the order of x, y, vx, vy separated by spaces. Then, the points to 
intersect are given in their own line for each point. They start with a
 P and then are list x then y separated by a space.

The solution to the file is saved as a txt file and as a png file. The 
png file shows the places of the block in a grid. In this grid, the 
legend for the tiles is as follows:

White = reflect block
Black = opaque block
Light Blue = refract block
Gray = Empty spot

This code relies on the following files to solve the grid .bff files:
Blocks.py, lazors_func.py, print_solution.py, and Read_map.py

***FILES***
    Read_map.py
        This file contains the code to parse out the inputted .bff file 
        into grid, number_of_reflect_blocks, number_of_refract_blocks, 
        number_of_opaque_blocks, initial_lazor, and 
        positions_to_intersect. This file contains a unit test for the
        read_map function.

        For more information about the function see Read_map.py.

    Blocks.py
        This file contains the block class, which creates a block object
        that is either reflect, opaque, or refract and has the 
        properties of such. This block class contains the hit_block 
        function, which determines the lazor path after it encounters a 
        block. This file relies on the lazors_func.py file to move the 
        lazor when it hits a block. 

        Then, this file contains the block_wall function, which 
        determines if the lazor hits a vertical or horizontal wall. 
        Additionally, it contains stationary_blocks, which determines 
        the positions of the stationary blocks in the inputted grid.
        It also contains place_block, which places the available blocks 
        in the grid and makes a new_grid to try and solve. Then, this 
        file contains a unit test for block_wall\\\\

        For more information about the functions see Blocks.py.
    
    lazors_func.py
        This file contains the lazor class, which has the direction and
        points of the lazor. This class has the move function, which 
        allows the lazor to move. Then, it also contains the overlap 
        function, which determines if the lazor gets stuck and 
        continuously overlaps itself. Then, it contains the 
        lazors_in_grid, which determines if the lazor is inside the 
        grid. This file contains a unit test for lazors_in_grid\\\\
        
        For more information about the functions see lazor_func.py.

    print_solution.py
        This file prints the solution as a txt file and as an image 
        for ease. This file contains the gridmake function, which joins 
        the grid to export to a txt file. This file also contains the 
        get_colors function, which determines the colors of block. Then,
        he save_grid function saves the image of the grid as a png file.

        For more information about the functions see save_grid.py.

***FUNCTIONS***
    The functions in this file are:
        solve_grid
            This function solves the grid and saves a txt file and a png
            image.

        solve_gridUT
            This function unit tests the solve grid function.
'''

import copy
import numpy as np
from Blocks import block, block_wall, place_block, stationary_blocks
from lazors_func import lazor, overlap, lazors_in_grid
from Read_map import read_map
from print_solution import gridmaker, get_colors, save_grid

def solve_grid(filename):
    '''
    This function uses the functions in the following files to read and
    solve a grid from the game lazors: Blocks.py, lazors_func.py, 
    print_solution.py, and Read_map.py. For more information about the
    functions referenced in this solution see the .py files.

    **Parameters**
        filename: *str*
            The name of the game file formatted as described in the
            docstring at the begining of this file. This filename must 
            include a .bff to be read.

    **Returns**
        new_grid: *list*
            This is the solution to the grid.
    '''

    grid, number_of_reflect_blocks, number_of_refract_blocks, \
    number_of_opaque_blocks, initial_lazor, positions_to_intersect \
    = read_map(filename)

    initial_lazor_path = []
    initial_lazors = []
    for initial_values in initial_lazor:
        x = float(initial_values[0])
        y = float(initial_values[1])
        vx = float(initial_values[2])
        vy = float(initial_values[3])
        initial_lazor_path.append((x,y))
        initial_lazors.append(lazor(x,y,vx,vy))

    goal_met = False
    while not goal_met:
        lazor_path = copy.deepcopy(initial_lazor_path)
        lazors = copy.deepcopy(initial_lazors)

        blocks = stationary_blocks(grid)
        new_blocks, new_grid = place_block(grid, number_of_reflect_blocks, \
            number_of_refract_blocks, number_of_opaque_blocks)
        blocks += new_blocks

        grid_solved = False
        first_pass = True

        while grid_solved == False:
            exit = False
            if set(positions_to_intersect).issubset(lazor_path):
                goal_met = True 

            for a in range(len(lazors)):
                if first_pass == True:
                    first_pass == False
                if overlap(lazor_path, first_pass):
                    grid_solved = True

                else:
                    for b in range(len(blocks)):
                        vertical_wall, horizontal_wall = \
                            block_wall(lazors[a].x, lazors[a].y, \
                            blocks[b].position, lazors[a].vx, lazors[a].vy)

                        if vertical_wall or horizontal_wall:
                            lazors_reflect, lazors_split, transmit, \
                                reflect = blocks[b].hit_block(lazors[a].x, \
                                lazors[a].y, lazors[a].vx,lazors[a].vy, \
                                vertical_wall,horizontal_wall)
                            lazors[a] = lazors_reflect

                            if lazors_reflect == []:
                                lazors.remove(lazors[a])
                                exit = True
                                if lazors == []:
                                    grid_solved = True
                                break

                            if transmit == True:
                                lazors.append(lazors_split)

                            between_blocks = []
                            if reflect:
                                for b in range(len(blocks)):
                                    x = int(lazors[a].x)
                                    y = int(lazors[a].y)
                                    xy = [(x, y)]
                                    if set(xy).issubset(blocks[b].position):
                                        between_blocks.append(1)
                                        if len(between_blocks) > 1:
                                            lazors.remove(lazors[a])
                                            exit = True
                                            if lazors == []:
                                                grid_solved = True
                                            break
                                break

                    if exit:
                        break
                    else:
                        if lazors_in_grid(grid, lazors, a):
                            lazor_path.append((lazors[a].x, lazors[a].y))
                            lazors[a].move()
                            lazor_path.append((lazors[a].x, lazors[a].y))
                        else:
                            lazor_path.append((lazors[a].x, lazors[a].y))
                            lazors.remove(lazors[a])

                            if lazors == []:
                                grid_solved = True
                            break

    level = filename.replace('.bff','')
    f = open('Lazor_Solutions.txt', 'w+')
    f.write('This is the solution for Lazor level: ')
    f.write(level)
    f.write('\n\nLegend \nx = No Block Allowed Here \no = Block Allowed Here \nA = Reflect Block \nB = Opaque Block \nC = Refract Block\n\n')
    f.write('Using the above legend, place the blocks according to the solution below\n\n')
    f.write(gridmaker(new_grid))
    f.close()

    grid_colors = [
            [0 for j,value in enumerate(line)]
            for i,line in enumerate(new_grid)
        ]

    for i,line in enumerate(new_grid):
        for j,value in enumerate(line):
            if value == 'A':
                grid_colors[i][j] = 1
            if value == 'B':
                grid_colors[i][j] = 2
            if value == 'C':
                grid_colors[i][j] = 3

    save_grid(grid_colors, level) 
    return new_grid

def solve_grid_UT(solution):
    showstopper_4 = [['B', 'A', 'B'], ['B', 'o', 'A'], ['A', 'o', 'B']]
    numbered_6 = [['B', 'o', 'o'], ['A', 'x', 'x'], ['B', 'o', 'A'], ['A', 'x', 'o'], ['B', 'o', 'o']]
    mad_1 = [['o', 'o', 'C', 'o'], ['o', 'o', 'o', 'A'], ['A', 'o', 'o', 'o'], ['o', 'o', 'o', 'o']]
    mad_4 = [['o', 'o', 'o', 'o'], ['o', 'A', 'o', 'o'], ['A', 'o', 'o', 'o'], ['o', 'A', 'o', 'A'], ['o', 'o', 'A', 'o']]
    mad_7 = [['o', 'o', 'A', 'o', 'o'], ['o', 'o', 'o', 'A', 'o'], ['A', 'o', 'A', 'o', 'x'], ['o', 'o', 'o', 'A', 'o'], ['o', 'o', 'A', 'o', 'o']]
    tiny_5 = [['A', 'B', 'A'], ['o', 'o', 'o'], ['A', 'C', 'o']]
    yarn_5 = [['o', 'B', 'x', 'o', 'o'], ['o', 'A', 'o', 'o', 'o'], ['A', 'x', 'o', 'o', 'A'], ['o', 'x', 'A', 'o', 'x'], ['A', 'o', 'x', 'x', 'A'], ['B', 'A', 'x', 'A', 'o']]
    dark_1 = [['x', 'o', 'o'], ['o', 'B', 'o'], ['B', 'B', 'x']]
    standard = [showstopper_4, numbered_6, mad_1, mad_4, mad_7, tiny_5, yarn_5, dark_1]
    assert (solution == showstopper_4), 'It seems the blocks are not in the right place for any of these levels' 

if __name__ == '__main__':
    solve_grid("mad_4.bff")
