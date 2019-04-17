from lazors import lazor
import copy
import random

class block(object):
    def __init__(self, blocktype):
        if blocktype == "A": # reflective block
            self.blocktype = "A"
            self.transmit = False
            self.reflect = True
            self.position = []
        if blocktype == "B": #opaque
            self.blocktype = "B"
            self.transmit = False
            self.reflect = False
            self.position = []
        if  blocktype == "C": #refract
            self.blocktype = "C"
            self.transmit = True
            self.reflect = True
            self.position = []

    def hit_block(self,x,y,vx,vy,vertical_wall,horizontal_wall):
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
    Determines if the lazor hits a block wall and if the wall is horizontal or vertical
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

def place_block(grid, number_of_reflect_blocks, number_of_refract_blocks, number_of_opaque_blocks):
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
                position_in_new_grid.append((2*position[0]+h,2*position[1]+k))
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
                position_in_new_grid.append((2*position[0]+h,2*position[1]+k))
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
                position_in_new_grid.append((2*position[0]+h,2*position[1]+k))
        blocks[where_in_blocks].position = position_in_new_grid
        position_in_new_grid = []
    return blocks, new_grid

def stationary_blocks(grid):
    '''
    Creates objects for the stationary blocks
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
        blocks[position_in_grid.index(a)].position = position_in_new_grid
        position_in_new_grid = []
    return blocks