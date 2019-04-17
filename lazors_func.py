'''
Author: Kunal Dani, Shyanne Salen, Marina Morrow
Last Modified: April 17th, 2019

File contains lazor class and object used in Lazor.py file when solving a grid.
Three functions also contained within this file: overlap, lazors_in_grid,
and lazor_bounds_UT

Functions:

    overlap(lazor_path, first_pass)

    lazors_in_grid(grid, lazors, a)

    lazor_bounds_UT(grid, x, y)
'''


class lazor:
    '''
    Class contains the attributes of the lazor, its position (given by x, y)
    And its trajectory (given by vx, vy)
    lazor.move function uses lazor trajectory to alter lazors position during
    execution of the code
    '''
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self):
        self.x += self.vx
        self.y += self.vy


def overlap(lazor_path, first_pass):
    '''
    overlap function identifies if lazor overlaps its own previous coordinate
    by comparing the current coordinates and original coordinates.

    **Parameters**

        lazor_path: *list of tuples*
            This is the list containing tuples of the lazor coordinates
        first_pass: *bool*
            This is a boolean defaulted as false used to check if the lazor
            is passing through the coordinates on its first time or
            subsequent times (hence overlap)

    **Returns**

        overlap: *boolean*
            Either true or false depending on if current
            lazor coordinates overlap with previous coordinates
    '''
    overlap = False
    if first_pass is False:
        if lazor_path[-2] == lazor_path[0]:
            if lazor_path[-1] == lazor_path[1]:
                x = lazor_path[-1][0]
                y = lazor_path[-1][1]
                overlap = True
    return overlap


def lazors_in_grid(grid, lazors, a):
    '''
    This function checks if the lazor has tangible coordinates 
    within the bounds of the grid that are not at the origin

    **Parameters**

        grid: *list of lists*
            A list of lists containing the physical positions and dimensions of
            of the grid both laterally and longitudinally.
        lazors: *float*
            Provides that coordinates of a specific lazor
            object within list of lazors.
        a: *int*
            Provides specific indice of lazor object within list of lazors
    
    **Returns**

        *bool*
            Returns a boolean 'True' if lazor is within bounds of grid

    '''
    if lazors[a].x >= 0.0 and lazors[a].y >= 0.0:
        if lazors[a].x <= float(2 * len(grid)) and lazors[a].y <= float(2 * len(grid)):
            return True


def lazor_bounds_UT(grid, x, y):
    '''
    Unit test to check if lazor is within boundaries of grid

    **Parameters**

        grid: *list of lists*
            A list of lists containing the physical positions and dimensions of
            of the grid both laterally and longitudinally.
        x,y: *float*
            Provides that coordinates of a specific
            lazor object within list of lazors.

    **Returns**

        InBound: *bool*
            A boolean that returns true if lazor is within boundaries of grid

    '''
    InBound = False
    if x >= 0.0 and y >= 0.0:
        if x <= float(2 * len(grid)) and y <= float(2 * len(grid)):
            InBound = True
    assert InBound, 'The lazor is outside the boundaries of the grid'
