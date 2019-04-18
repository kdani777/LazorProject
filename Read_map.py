'''
Authors: Kunal Dani, Marina Morrow, Shyanne Salen
Last Modified: April 17th, 2019
Lazor Project
Software Carpentry
Read_map

This code reads a .bff file for the Lazors game on android/apple. This
.bff file must contain the grid. The grid must begin with GRID START 
followed by the grid and then GRID STOP. Each spot in the grid must be 
separated by space and the rows in their own rows. The grid should look 
similar to:

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

Then, the .bff files must have the number of reflect, opaque, and 
refract blocks. Each of these should be in their own line proceeded by 
their corresponding letter:

A = reflect block
B = opaque block
C = refract block

Then, the .bff files must have the lazors. Each lazor is on its own 
line proceeded by the letter L. Then, the starting points and direction
are given in the order of x, y, vx, vy separated by spaces. Then, the 
points to intersect are given in their own line for each point. They 
start with a P and then are list x then y separated by a space.

***FUNCTIONS***
    read_map
        This function parses the information in a .bff file for the
        initial start of a grid for the game Lazors.
'''
def read_map(filename):
    '''
    This function reads the map and parse the information in a .bff
    file that represents a grid in the Lazors game. This function will
    read the file according to the format outlined above in the 
    docstring.

    **Parameters**
        filename: **str**
            This is the name of the file you want to read with .bff

    **Returns**
        grid: **list**
            The grid map of the game with o, A, B, C, or x
        number_of_reflect_blocks: **int**
            The number of reflect blocks available to move
        number_of_refract_blocks: **int**
            The number of refract blocks available to move
        number_of_opaque_blocks: **int**
            The number of opaque blocks available to move
        initial_lazor: **list**
            The direction the lazor is initially pointing
        positions_to_intersect: **list**
            The positions the lazor must intersect
    '''
    data = open(filename, 'r').read()
    split_strings = data.strip().split('\n')
    grid = []
    in_grid = False
    positions_to_intersect = []
    initial_lazor = []
    number_of_opaque_blocks = 0
    number_of_reflect_blocks = 0
    number_of_refract_blocks = 0

    for line in split_strings:
        if not in_grid:
            if line.startswith('GRID START'):
                in_grid = True
            elif line.startswith("A"): 
                number_of_reflect_blocks = int(line.strip().split()[1])
            elif line.startswith("B"):
                number_of_opaque_blocks = int(line.strip().split()[1])
            elif line.startswith("C"):
                number_of_refract_blocks = int(line.strip().split()[1])
            elif line.startswith("L"):
                initial_lazor.append(line.strip().split()[1:])
            elif line.startswith("P"):
                positions_to_intersect.append(tuple(map(float, \
                    line.strip().split()[1:])))
            else:
                continue
        elif line.startswith('GRID STOP'):
                in_grid = False
        else:
            grid.append(line.strip().split())

    return grid, number_of_reflect_blocks, number_of_refract_blocks, \
    number_of_opaque_blocks, initial_lazor, positions_to_intersect
