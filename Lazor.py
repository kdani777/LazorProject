'''
Authors: Kunal Dani, Marina Morrow, Shyanne Salen
Last Modified: April 7th, 2019
'''
import copy
import numpy as np
from Blocks import block, block_wall, place_block, stationary_blocks
from lazors import lazor, overlap, lazors_in_grid
from Read_map import read_map
from print_solution import gridmaker, get_colors, save_grid

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

    save_grid(grid_colors, lvl) 
    return new_grid

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

# solve_gridUT(solve_grid('showstopper_4.bff'))

# if __name__ == '__main__':
solve_grid("mad_1.bff")
