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

def read_mapUT(filename): # Unit Test for readmap function
    solution = read_map(filename)
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