'''
Authors: Kunal Dani, Marina Morrow, Shyanne Salen
Last Modified: April 17th, 2019
Lazor Project
Software Carpentry
Blocks

This file conatians the block class to create blocks that can be placed
in a grid for the game Lazors. Inside the block class there is a 
function hit_block which determines what happens when the lazor hits
a block. This file also contains the function block_wall which 
determines if the lazor hits a block and what side of the block it 
hits.

This file also contains the stationary_block function, which uses a 
grid to create block objects in a list. Also, the function place_blocks
places new blocks in a grid to be able to be able to test the different
configurations.

This file relies on the lazor_func.py file for the lazor class.

***FILES***
    lazor_func.py
        This file contains the lazor class, which has the direction and
        points of the lazor. This class has the move function, which 
        allows the lazor to move. 

        For more information about the functions see lazor_func.py.

***CLASSES***
    block
        This class creates an a block object that is able to move around
        a grid. The block can be a reflective, opaque, or refractive
        block, which are characterized by the letters A, B, and C.,
        respectively. This class has a hit_block function, which 
        determines what happens to a lazor when it hits one of the 
        three types of blocks.

***FUNCTIONS***
    block_wall
        This function determines if the lazor hits a block wall if that
        wall is horizontal or vertical.
    stationary_block
        This function looks a grid and creates block objects from that
        grid and determines their positions
    place_block
        This function places new blocks in a grid to be able to test
        a possible solution.
'''
from lazors_func import lazor
import copy
import random

class block():
    '''
    This class creates a block object to move around a grid and get hit
    by lazors.

     ***Functions***
        __init__
            This determines self for the block.
        hit_block
            This function determines what happens to the lazor 
            trajectory when the lazor hit a block.
    '''
    def __init__(self, blocktype):
        '''
        This function determines the self of the block.This block has 
        a position, which is a list of (x,y) tuples in a coordinate. 
        This block is either a reflect, opaque, and refract block and 
        has a reflect and transmit property, which varies with block 
        type. The lazor reflects off of reflect blocksm thus, reflect 
        is True. The lazor stops at opaque block, thus, it does not 
        reflect or transmit. The lazor transmits through the refract 
        block and also reflects off of it. Thus, it both reflects and 
        refracts.

        ***Parameters***
            blocktype: *str*
                This is the type of block desired, which can be A, B,
                or C. This is a reflect, opaque, and refract block,
                respectively.
        '''
        if blocktype == "A":
            self.blocktype = "A"
            self.transmit = False
            self.reflect = True
            self.position = []
        if blocktype == "B":
            self.blocktype = "B"
            self.transmit = False
            self.reflect = False
            self.position = []
        if  blocktype == "C":
            self.blocktype = "C"
            self.transmit = True
            self.reflect = True
            self.position = []

    def hit_block(self,x,y,vx,vy,vertical_wall,horizontal_wall):
        '''
        This function determines what happens if a  lazor hits a block and
        determines its new trajectory.

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
        veritcal_wall: *boolean*
            This is either True or False and determines if the lazor hit
            a vertical wall. This cannot be True if horizontal_wall is
            True.
        horizontal_wall: *boolean*
            This is either True or False and determines if the lazor hit
            a horizontal wall. This cannot be True if veritcal_wall is
            True.

        ***Returns***
            lazors: *list*
                This is a list of the lazor object after they hit the
                block.
            lazors_split: *object*
                This the new lazor object if the lazor splits when it
                hits a transmit block.
            transmits: *boolean*
                This is True if the lazor transmits through a block.
            reflect: *boolean*
                This is True if the lazor reflects off a block.
        '''
        lazors = []
        lazors_split = []
        transmits = False
        reflect = False

        if self.reflect:
            reflect = True
            if vertical_wall:
                new_vx = -1.0*vx
                new_vy = vy
            if horizontal_wall:
                new_vx = vx
                new_vy = -1.0*vy
            lazors = lazor(x, y, new_vx, new_vy)

        if self.transmit:
            lazors_split = lazor(x, y, vx, vy)
            transmits = True
            lazors_split.move()

        return lazors, lazors_split, transmits, reflect

def block_wall(x,y,block_position,vx,vy):
    '''
    This function determines if the lazor hits a block wall and if the 
    wall is horizontal or vertical.

    **Parameters**
        x: *float*
            This is the x coordinate of the lazor position on a grid.
        y: *float*
            This is the y coordinate of the lazor position on a grid.
        block_position: *list*
            This is a list of the block's position, which is are (x,y)
            coordinate tuples.
        vx: *float*
            This is used to define the direction that lazor is moving
            this is either 1 or -1 to describe the lazors path.
        vy: *float*
            This is used to define the direction that lazor is moving
            this is either 1 or -1 to describe the lazors path.

    **Returns**
        veritcal_wall: *boolean*
            This is either True or False and determines if the lazor hit
            a vertical wall. This cannot be True if horizontal_wall is
            True.
        horizontal_wall: *boolean*
            This is either True or False and determines if the lazor hit
            a horizontal wall. This cannot be True if veritcal_wall is
            True.
    '''
    horizontal_wall = False
    vertical_wall = False 
    block_x = [i[0] for i in block_position]
    block_y = [i[1] for i in block_position]
    if x in block_x and y in block_y:
        inside_block = lazor(x,y,vx,vy)
        inside_block.move()
        if inside_block.x in block_x and inside_block.y in block_y:
            if x % 2 == 0 and y % 2 != 0:
                vertical_wall = True
            if y % 2 == 0 and x % 2 != 0:
                horizontal_wall = True
    return vertical_wall, horizontal_wall


def block_wallUT(x,y,block_position,vx,vy):
    vertical_wall, horizontal_wall = block_wall(x,y,block_position,vx,vy)
    assert (vertical_wall == True and horizontal_wall == False or 
            vertical_wall == False and horizontal_wall == True or
            vertical_wall == False and horizontal_wall == False),'The lazor should only hit one wall or no walls, here both walls were hit'

def stationary_blocks(grid):
    '''
    This function uses a grid to creates a list of objects for the 
    stationary blocks in the grid.

    ***Parameters***
        grid: *list*
            This is a list of the list of rows of the grid to be solved.

    ***Returns***
        blocks: *list*
            This is a list of the block objects for the stationary 
            blocks in the grid.
    '''
    position_in_grid = []
    position_in_new_grid = []
    blocks = []

    for i,line in enumerate(grid):
        for j,value in enumerate(line):
            if value != 'o':
                if value != 'x':
                    position_in_grid.append((j, i))
                    blocks.append(block(value))

    for a in position_in_grid:
        for h in range(0, 3):
            for k in range(0,3):
                position_in_new_grid.append((2*a[0]+h,2*a[1]+k))
        blocks[position_in_grid.index(a)].position = \
            position_in_new_grid
        position_in_new_grid = []

    return blocks

def place_block(grid, number_of_reflect_blocks, number_of_refract_blocks, \
    number_of_opaque_blocks):
    '''
    This function randomly places new blocks in a grid so that a solution
    for the grid can be found.

    ***Parameters***
        grid: *list*
            This is a list of the list of rows of the grid to be solved.
            This list should contain the stationary blocks.
        number_of_reflect_blocks: *int*
            The number of reflect blocks available to move
        number_of_refract_blocks: *int*
            The number of refract blocks available to move
        number_of_opaque_blocks: *int*
            The number of opaque blocks available to move

    ***Returns**
        blocks: *list*
            This is a list of the block objects placed in the grid.
        new_grid: *list*
        This is a list of the list of rows of the grid to be solved.
        This grid has all the blocks placed in it and it ready to be
        tried as a solution.
    '''
    position_in_grid = []
    position_in_new_grid = []
    blocks = []
    new_grid = copy.deepcopy(grid)

    for i,line in enumerate(grid):
        for j,value in enumerate(line):
            if value == 'o':
                position_in_grid.append((j, i))

    for a in range(number_of_reflect_blocks):
        blocks.append(block("A"))
        where_in_blocks = len(blocks)-1
        position = random.choice(position_in_grid)
        new_grid[position[1]][position[0]] = "A"
        position_in_grid.remove(position)

        for h in range(0, 3):
            for k in range(0,3):
                position_in_new_grid.append((2*position[0]+h,2* \
                    position[1]+k))
        blocks[where_in_blocks].position = position_in_new_grid
        position_in_new_grid = []

    for b in range(number_of_opaque_blocks):
        blocks.append(block("B"))
        where_in_blocks = len(blocks)-1
        position = random.choice(position_in_grid)
        new_grid[position[1]][position[0]] = "B"
        position_in_grid.remove(position)

        for h in range(0, 3):
            for k in range(0,3):
                position_in_new_grid.append((2*position[0]+h,2* \
                    position[1]+k))
        blocks[where_in_blocks].position = position_in_new_grid
        position_in_new_grid = []

    for c in range(number_of_refract_blocks):
        blocks.append(block("C"))
        where_in_blocks = len(blocks)-1
        position = random.choice(position_in_grid)
        new_grid[position[1]][position[0]] = "C"
        position_in_grid.remove(position)

        for h in range(0, 3):
            for k in range(0,3):
                position_in_new_grid.append((2*position[0]+h,2* \
                    position[1]+k))
        blocks[where_in_blocks].position = position_in_new_grid
        position_in_new_grid = []
    return blocks, new_grid

