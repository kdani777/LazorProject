'''
Authors: Kunal Dani, Marina Morrow, Shyanne Salen
Last Modified: April 17th, 2019
Lazor Project
Software Carpentry
lazors_func

This file contains the lazor class for the lazor to move. It also
contains an overlap function which determines if the lazor gets stuck
in a loop. Additionally, the function lazors_in_grid determines if the
lazors are moving within the grid.

***CLASS***
    lazor
        This class creates a lazor object and uses the function move 
        to move the lazor through a grid.

***FUNCTIONS***
    overlap
        This function determines if the lazor overlaps itself for two
        consecutive points so the lazor does not get stuck in a loop
        between blocks where it keeps running over itself.
    lazors_in_grid
        This function determines in the lazor is within the bounds of 
        the grid.
'''

class lazor:
    '''
    This lazor class creates an lazor object that can move around a
    grid using x, y cordinates and the directions vx and vy.

    ***Functions***
        __init__
            This determines self for the lazor.
        move
            This function moves the lazor around the grid.
    '''
    def __init__(self, x, y, vx, vy):
        '''
        This function determines self for the lazor and can be used to
        create an instance of the object. The lazor contains an x and y 
        position and a direction in the form vx, vy.

        ***Parameters***
            x: *float*
                This is the x coordinate of the lazor position on a grid.
            y: *float*
                This is the y coordinate of the lazor position on a grid.
            vx: *float*
                This is used to define the direction that lazor is moving
                this is either 1 or -1 to describe the lazors path.
            vy: *float*
                This is used to define the direction that lazor is moving
                this is either 1 or -1 to describe the lazors path.
        '''
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    def move(self):
        '''
        This function allows the lazor to move around the grid. It uses
        the self variable vx and vy to change the x and y coordinate of
        the lazor to move it around the grid according the direction.
        '''
        self.x += self.vx
        self.y += self.vy

def overlap(lazor_path, first_pass): 
    '''
    This function determines if the lazor overlaps itself on more than
    two points to determine if the lazor is stuck in a loop between
    blocks. This function returns True if the lazor overlaps itself for
    more than one point.

    ***Parameter***
        lazor_path: *list*
            This is a list of the (x,y) tuples of where the lazor has 
            been.
        first_pass: *boolean*
            This is either True or False to determine if it is the 
            first point in the lazor path. If it is the first point
            then the lazor cannot overlap itself.
    ***Returns***
        overlap: *boolean*
            This returns either True or False if the lazor overlaps 
            itself. If it overlaps itself, it returns True.
    '''
    overlap = False
    if first_pass == False:
        if lazor_path[-2] == lazor_path[0]:
            if lazor_path[-1] == lazor_path[1]:
                x = lazor_path[-1][0]
                y = lazor_path[-1][1]
                overlap = True
    return overlap

def lazors_in_grid(grid, lazors, index):
    '''
    This function determines if the lazor path is inside the grid. If it
    is in the grid it returns True.

    ***Parameters***
        grid: *list*
            This is a list of the list of rows of the grid.
        lazors: *list*
            This is a list of the lazor objects.
        index: *int*
            This identifies which lazor is being tested of whether it is
            in the grid in the list lazors, which is a list of lazor 
            objects.

    ***Returns***
        True
            This returns a boolean of True if the lazors are outside
            of the grid.
    '''
    if lazors[index].x >= 0.0 and lazors[index].y >= 0.0:
        if lazors[index].x <= float(2*len(grid)) and lazors[index].y \
            <= float(2*len(grid)):
            return True

