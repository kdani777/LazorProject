'''
Authors: Kunal Dani, Marina Morrow, Shyanne Salen
Last Modified: April 7th, 2019
'''
from collections import Counter
import random
import copy

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

#i think all the defs have to be within class
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

def goalcheck(lazor_path, positions_to_intersect):
    goal_met = False
    if set(positions_to_intersect).issubset(lazor_path):
        goal_met = True
    return goal_met

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
    lvl = filename.replace('.bff','')
    f = open('LazorSolutions.txt', 'w+')
    f.write('This is the solution for Lazor level: ')
    f.write(lvl)
    f.write('\n\nLegend \nx = No Block Allowed Here \no = Block Allowed Here \nA = Reflect Block \nB = Opaque Block \nC = Refract Block\n\n')
    f.write('Using the above legend, place the blocks according to the solution below\n\n')
    f.write(gridmaker(new_grid))
    f.close()
    return(new_grid)

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
    assert (solution == showstopper_4), 'It seems the blocks are not in the right place for any of these levels' 

solve_gridUT(solve_grid('showstopper_4.bff'))

# if __name__ == '__main__':
solve_grid("mad_1.bff")
