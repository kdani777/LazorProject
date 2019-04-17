'''
Authors: Kunal Dani, Marina Morrow, Shyanne Salen
Last Modified: April 7th, 2019
'''
from collections import Counter
import random
import copy
import numpy as np

def read_map(filename):
    '''
    This function reads the map and parse the information in it.

    **Parameters**
        filename: **str**
            This is the name of the file you want to read

    **Returns**
        grid: **list**
            The grid map of the game with o, A, B, C, or x.
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
                positions_to_intersect.append(tuple(map(float, line.strip().split()[1:])))
            else:
                continue
        elif line.startswith('GRID STOP'):
                in_grid = False
        else:
            grid.append(line.strip().split())
    return grid, number_of_reflect_blocks, number_of_refract_blocks, number_of_opaque_blocks, initial_lazor, positions_to_intersect

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

class lazor:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    def move(self):
        self.x += self.vx
        self.y += self.vy

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

def overlap(lazor_path, blocks, first_pass): 
    overlap = False
    if first_pass == False:
        if lazor_path[-2] == lazor_path[0]:
            if lazor_path[-1] == lazor_path[1]:
                x = lazor_path[-1][0]
                y = lazor_path[-1][1]
                overlap = True
    return overlap

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

def lazors_in_grid(grid, lazors, a):
    if lazors[a].x >= 0.0 and lazors[a].y >= 0.0:
        if lazors[a].x <= float(2*len(grid)) and lazors[a].y <= float(2*len(grid)):
            return True

def lazor_bounds_UT(grid, lazors):
    lazors_in_grid()
    assert 
def gridmaker(new_grid):
    ng = '\n'.join([' '.join(i) for i in new_grid])
    return(ng)

def solve_grid(filename):
    grid, number_of_reflect_blocks, number_of_refract_blocks, number_of_opaque_blocks, initial_lazor, positions_to_intersect = read_map(filename)
    lazor_path_initial = []
    initial_lazors = []
    for initial in initial_lazor:
        x = float(initial[0])
        y = float(initial[1])
        vx = float(initial[2])
        vy = float(initial[3])
        lazor_path_initial.append((x,y))
        initial_lazors.append(lazor(x,y,vx,vy))
    goal_met = False
    while not goal_met:
        lazor_path = copy.deepcopy(lazor_path_initial)
        lazor_1 = []
        lazor_2 = []
        lazors = copy.deepcopy(initial_lazors)
        not_a_solution = False
        exit = False
        blocks = stationary_blocks(grid)
        new_blocks, new_grid = place_block(grid, number_of_reflect_blocks, number_of_refract_blocks, number_of_opaque_blocks)
        blocks += new_blocks
        first_pass = True
        while not_a_solution == False:
            exit = False
            if set(positions_to_intersect).issubset(lazor_path):
                goal_met = True 
            for a in range(len(lazors)):
                if first_pass == True:
                    first_pass == False
                if overlap(lazor_path, blocks, first_pass):
                    not_a_solution = True
                else:
                    for b in range(len(blocks)):
                        vertical_wall, horizontal_wall = block_wall(lazors[a].x,lazors[a].y,blocks[b].position,lazors[a].vx,lazors[a].vy)
                        if vertical_wall or horizontal_wall:
                            lazors_reflect, lazors_split, transmit, reflect = blocks[b].hit_block(lazors[a].x,lazors[a].y,lazors[a].vx,lazors[a].vy,vertical_wall,horizontal_wall)
                            lazors[a] = lazors_reflect
                            if lazors_reflect == []:
                                lazors.remove(lazors[a])
                                exit = True
                                if lazors == []:
                                    not_a_solution = True
                                break
                            if transmit == True:
                                lazors.append(lazors_split)
                            p = []
                            if reflect:
                                for b in range(len(blocks)):
                                    x = int(lazors[a].x)
                                    y = int(lazors[a].y)
                                    xy = [(x, y)]
                                    if set(xy).issubset(blocks[b].position):
                                        p.append(1)
                                        if len(p) > 1:
                                            lazors.remove(lazors[a])
                                            exit = True
                                            if lazors == []:
                                                not_a_solution = True
                                            break
                                break
                    if exit:
                        break
                    else:
                        if lazors_in_grid(grid, lazors, a):
                            lazor_path.append((lazors[a].x, lazors[a].y))
                            lazors[a].move()
                            lazor_path.append((lazors[a].x, lazors[a].y))
                            lazor_1.append((lazors[0].x, lazors[0].y))
                            if len(lazors) > 1:
                                lazor_2.append((lazors[1].x, lazors[1].y))
                        else:
                            lazor_path.append((lazors[a].x, lazors[a].y))
                            lazors.remove(lazors[a])
                            if lazors == []:
                                not_a_solution = True
                            break
    # lvl = filename.replace('.bff','')
    # f = open('LazorSolutions.txt', 'w+')
    # f.write('This is the solution for Lazor level: ')
    # f.write(lvl)
    # f.write('\n\nLegend \nx = No Block Allowed Here \no = Block Allowed Here \nA = Reflect Block \nB = Opaque Block \nC = Refract Block\n\n')
    # f.write('Using the above legend, place the blocks according to the solution below\n\n')
    # f.write(gridmaker(new_grid))
    # f.close()
    # return new_grid

def block_wallUT(x,y,block_position,vx,vy):
    vertical_wall, horizontal_wall = block_wall(x,y,block_position,vx,vy)
    assert (vertical_wall == True and horizontal_wall == False or 
            vertical_wall == False and horizontal_wall == True or
            vertical_wall == False and horizontal_wall == False),'The lazor should only hit one wall or no walls, here both walls were hit'

def goalcheckUT(lazor_path, positions_to_intersect):
    goal_met = False
    if set(positions_to_intersect).issubset(lazor_path):
        goal_met = True
    assert goal_met, 'It seems the lazor did not hit the targets'

def solve_gridUT(solution): # Unit Test for Solve grid function
    showstopper_4 = [['B', 'A', 'B'], ['B', 'o', 'A'], ['A', 'o', 'B']]
    numbered_6 = [['B', 'o', 'o'], ['A', 'x', 'x'], ['B', 'o', 'A'], ['A', 'x', 'o'], ['B', 'o', 'o']]
    mad_1 = [['o', 'o', 'C', 'o'], ['o', 'o', 'o', 'A'], ['A', 'o', 'o', 'o'], ['o', 'o', 'o', 'o']]
    mad_4 = [['o', 'o', 'o', 'o'], ['o', 'A', 'o', 'o'], ['A', 'o', 'o', 'o'], ['o', 'A', 'o', 'A'], ['o', 'o', 'A', 'o']]
    mad_7 = [['o', 'o', 'A', 'o', 'o'], ['o', 'o', 'o', 'A', 'o'], ['A', 'o', 'A', 'o', 'x'], ['o', 'o', 'o', 'A', 'o'], ['o', 'o', 'A', 'o', 'o']]
    tiny_5 = [['A', 'B', 'A'], ['o', 'o', 'o'], ['A', 'C', 'o']]
    yarn_5 = [['o', 'B', 'x', 'o', 'o'], ['o', 'A', 'o', 'o', 'o'], ['A', 'x', 'o', 'o', 'A'], ['o', 'x', 'A', 'o', 'x'], ['A', 'o', 'x', 'x', 'A'], ['B', 'A', 'x', 'A', 'o']]
    dark_1 = [['x', 'o', 'o'], ['o', 'B', 'o'], ['B', 'B', 'x']]
    standard = [showstopper_4, numbered_6, mad_1, mad_4, mad_7, tiny_5, yarn_5, dark_1]
    assert any([solution == x for x in standard]), 'It seems the blocks are not in the right place for any of these levels' 

def read_mapUT(filename): # Unit Test for readmap function
    showstopper_4 = ([['B', 'o', 'o'], ['o', 'o', 'o'], ['o', 'o', 'o']], 3, 0, 3, [['3', '6', '-1', '-1']], [(2.0, 3.0)])
    numbered_6 = ([['o', 'o', 'o'], ['o', 'x', 'x'], ['o', 'o', 'o'], ['o', 'x', 'o'], ['o', 'o', 'o']], 3, 0, 3, [['4', '9', '-1', '-1'], ['6', '9', '-1', '-1']], [(2.0, 5.0), (5.0, 0.0)])
    mad_1 = ([['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o']], 2, 1, 0, [['2', '7', '1', '-1']], [(3.0, 0.0), (4.0, 3.0), (2.0, 5.0), (4.0, 7.0)])
    mad_4 = ([['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o']], 5, 0, 0, [['7', '2', '-1', '1']], [(3.0, 4.0), (7.0, 4.0), (5.0, 8.0)])
    mad_7 = ([['o', 'o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o', 'x'], ['o', 'o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o', 'o']], 6, 0, 0, [['2', '1', '1', '1'], ['9', '4', '-1', '1']], [(6.0, 3.0), (6.0, 5.0), (6.0, 7.0), (2.0, 9.0), (9.0, 6.0)])
    tiny_5 = ([['o', 'B', 'o'], ['o', 'o', 'o'], ['o', 'o', 'o']], 3, 1, 0, [['4', '5', '-1', '-1']], [(1.0, 2.0), (6.0, 3.0)])
    yarn_5 = [['o', 'B', 'x', 'o', 'o'], ['o', 'A', 'o', 'o', 'o'], ['A', 'x', 'o', 'o', 'A'], ['o', 'x', 'A', 'o', 'x'], ['A', 'o', 'x', 'x', 'A'], ['B', 'A', 'x', 'A', 'o']]
    dark_1 = ([['x', 'o', 'o'], ['o', 'o', 'o'], ['o', 'o', 'x']], 0, 0, 3, [['3', '0', '-1', '1'], ['1', '6', '1', '-1'], ['3', '6', '-1', '-1'], ['4', '3', '1', '-1']], [(0.0, 3.0), (6.0, 1.0)])
    standard = [showstopper_4, numbered_6, mad_1, mad_4, mad_7, tiny_5, yarn_5, dark_1]
    assert any([solution == x for x in standard]), 'It seems the levels were not loaded correctly' 




if __name__ == '__main__':
solve_gridUT(solve_grid('showstopper_4.bff'))
block_wallUT(6.0, 9.0, [(4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2), (6, 0), (6, 1), (6, 2)], 1.0, 1.0)
lazor_path = [(2.0, 7.0), (2.0, 7.0), (3.0, 6.0), (3.0, 6.0), (4.0, 5.0), (4.0, 5.0), 
            (5.0, 4.0), (5.0, 4.0), (6.0, 3.0), (6.0, 3.0), (5.0, 2.0), (5.0, 2.0), (4.0, 3.0), 
            (4.0, 3.0), (3.0, 4.0), (4.0, 1.0), (3.0, 0.0), (3.0, 4.0), (2.0, 5.0), (3.0, 0.0), (2.0, -1.0), 
            (2.0, 5.0), (3.0, 6.0), (2.0, -1.0), (3.0, 6.0), (4.0, 7.0), (4.0, 7.0), (5.0, 8.0), 
            (5.0, 8.0), (6.0, 9.0), (6.0, 9.0)]
positions_to_intersect = [(3.0, 0.0), (4.0, 3.0), (2.0, 5.0), (4.0, 7.0)]
goalcheckUT(lazor_path, positions_to_intersect)
solve_grid("mad_1.bff")
