'''
Authors: Kunal Dani, Marina Morrow, Shyanne Salen
Last Modified: April 17th, 2019
Lazor Project
Software Carpentry
Unit Tests

This file unit tests the code to solve the Lazors android/apple game. This 
file uses a class called Test_Lazor to test the following files:
Blocks.py, lazors_func.py, Lazor.py, and Read_map.py

***FUNCTIONS***
  read_map_UT
    Tests the type of the outputs for the read_map function in Read_map.py.
    It also tests the output against the known maps if it is a known map to
    make sure it is parsing correctly.
  blocks_UT
    Tests the block_wall function in Blocks.py to make sure vertical_wall and
    horizontal_wall are both True.
  lazor_func_UT
    Tests to see if the lazor is inside the grid.
  solve_grid_UT
     Tests the type of the outputs for the solve grid function in Lazor.py.
     Tests against known solutions if the map is known.

'''
from Lazor import solve_grid
from Read_map import read_map
from lazors_func import lazor
from Blocks import block_wall

class Test_Lazor(object):
  '''
  This is the unit test class to test our files for Lazors game.
  '''
  def read_map_UT(self, read_map):
    '''
    This function unit tests the types for the outputs of the read_map 
    function in Read_map.py. It also tests the output against known outputs
    if the filename is one of the known maps.

    ***Parameters***
      read_map: *list*
        This is a list of the outputs from the read_map function in the 
        Read_map.py file.
    '''
    grid, number_of_reflect_blocks, number_of_refract_blocks, \
    number_of_opaque_blocks, initial_lazor, positions_to_intersect = read_map
    for row in grid:
      for value in row:
        assert (type(grid) == list), "The grid is not a list"
        assert (type(row) == list), 'The rows of the grid are not lists'
        assert (type(value) == str), 'The values in the grid are not strings'
    assert (type(number_of_reflect_blocks) == int), 'number_of_reflect_blocks'\
      ' is not an integer'
    assert (type(number_of_opaque_blocks) == int), 'number_of_opaque_blocks' \
      ' is not an integer'
    assert (type(number_of_refract_blocks) == int), 'number_of_refract_blocks' \
      ' is not an integer'
    assert (type(initial_lazor) == list), 'initial_lazor not a list'
    assert (type(positions_to_intersect) == list), 'positions_to_intersect not' \
    'a list'
    if filename == 'showstopper_4.bff' or 'mad_1.bff' or 'numbered_6.bff' or \
    'mad_4.bff' or 'mad_7.bff' or 'tiny_5.bff' or 'yarn_5.bff' or 'dark_1.bff':
      showstopper_4 = ([['B', 'o', 'o'], ['o', 'o', 'o'], ['o', 'o', 'o']], \
        3, 0, 3, [['3', '6', '-1', '-1']], [(2.0, 3.0)])
      numbered_6 = ([['o', 'o', 'o'], ['o', 'x', 'x'], ['o', 'o', 'o'], \
        ['o', 'x', 'o'], ['o', 'o', 'o']], 3, 0, 3, [['4', '9', '-1', '-1'], \
        ['6', '9', '-1', '-1']], [(2.0, 5.0), (5.0, 0.0)])
      mad_1 = ([['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o'],  \
        ['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o']], 2, 1, 0, \
        [['2', '7', '1', '-1']],\
        [(3.0, 0.0), (4.0, 3.0), (2.0, 5.0), (4.0, 7.0)])
      mad_4 = ([['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o'], \
        ['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o']], \
        5, 0, 0, [['7', '2', '-1', '1']], [(3.0, 4.0), (7.0, 4.0), (5.0, 8.0)])
      mad_7 = ([['o', 'o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o', 'o'], \
        ['o', 'o', 'o', 'o', 'x'], ['o', 'o', 'o', 'o', 'o'], \
        ['o', 'o', 'o', 'o', 'o']], 6, 0, 0, [['2', '1', '1', '1'], \
        ['9', '4', '-1', '1']], [(6.0, 3.0), (6.0, 5.0), (6.0, 7.0), \
        (2.0, 9.0), (9.0, 6.0)])
      tiny_5 = ([['o', 'B', 'o'], ['o', 'o', 'o'], ['o', 'o', 'o']], 3, 1, 0, \
        [['4', '5', '-1', '-1']], [(1.0, 2.0), (6.0, 3.0)])
      yarn_5 = [['o', 'B', 'x', 'o', 'o'], ['o', 'A', 'o', 'o', 'o'], \
        ['A', 'x', 'o', 'o', 'A'], ['o', 'x', 'A', 'o', 'x'], \
        ['A', 'o', 'x', 'x', 'A'], ['B', 'A', 'x', 'A', 'o']]
      dark_1 = ([['x', 'o', 'o'], ['o', 'o', 'o'], ['o', 'o', 'x']], 0, 0, 3, \
        [['3', '0', '-1', '1'], ['1', '6', '1', '-1'], ['3', '6', '-1', '-1'], \
        ['4', '3', '1', '-1']], [(0.0, 3.0), (6.0, 1.0)])
      standard = [showstopper_4, numbered_6, mad_1, mad_4, mad_7, tiny_5,\
      yarn_5, dark_1]
      assert any([read_map == x for x in standard]), 'It seems the levels were\
      not loaded correctly'

  def blocks_UT(x,y,block_position,vx,vy):
    '''
    This function unit tests the function block_wall in Blocks.py. If
    horizontal_wall and vertical_wall are both true then the lazor hit
    two wall simultaneously, which is not possible.

    ***Parameters***
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
    '''
    vertical_wall, horizontal_wall = block_wall(x,y,block_position,vx,vy)
    assert (vertical_wall == True and horizontal_wall == False or 
            vertical_wall == False and horizontal_wall == True or
            vertical_wall == False and horizontal_wall == False),'The lazor' \
            ' should only hit one wall or no walls, here both walls were hit'

  def lazors_func_UT(self, grid, x, y):
    '''
    This function unit tests the lazor position to see if it is inside the
    grid.

    ***Parameters***
      x: *float*
          This is the x coordinate of the lazor position on a grid.
      y: *float*
          This is the y coordinate of the lazor position on a grid.
      grid: *list*
        This is a list of the list of rows of the grid to be solved.
    '''
    InBound = False
    if x >= 0.0 and y >= 0.0:
        if x <= float(2*len(grid)) and y <= float(2*len(grid)):
            InBound = True
    assert InBound, 'The lazor is outside the boundaries of the grid'

  def solve_grid_UT(self, solution, filename):
    '''
    This function unit tests the types for the final grid solution of the 
    solve_grid function in lazors.py. It also tests the solution against known 
    solutions if the filename is one of the known maps.

    ***Parameters***
      solution: *list*
        This is a list of the list of rows of the grid that has been solved.
      filename: *str*
        The name of the file that is being solved.
    '''
    for row in solution:
      for value in row:
        assert (type(row) == list and type(value) == str), 'The final grid' \
        'is not the correct type'
    if filename == 'showstopper_4.bff' or 'mad_1.bff' or 'numbered_6.bff' or \
      'mad_4.bff' or 'mad_7.bff' or 'tiny_5.bff' or 'yarn_5.bff' or 'dark_1.bff':
      showstopper_4 = [['B', 'A', 'B'], ['B', 'o', 'A'], ['A', 'o', 'B']]
      numbered_6 = [['B', 'o', 'o'], ['A', 'x', 'x'], ['B', 'o', 'A'], \
       ['A', 'x', 'o'], ['B', 'o', 'o']]
      mad_1 = [['o', 'o', 'C', 'o'], ['o', 'o', 'o', 'A'], \
       ['A', 'o', 'o', 'o'], ['o', 'o', 'o', 'o']]
      mad_4 = [['o', 'o', 'o', 'o'], ['o', 'A', 'o', 'o'], \
       ['A', 'o', 'o', 'o'], ['o', 'A', 'o', 'A'], ['o', 'o', 'A', 'o']]
      mad_7 = [['o', 'o', 'A', 'o', 'o'], ['o', 'o', 'o', 'A', 'o'], \
       ['A', 'o', 'A', 'o', 'x'], ['o', 'o', 'o', 'A', 'o'], \
       ['o', 'o', 'A', 'o', 'o']]
      tiny_5 = [['A', 'B', 'A'], ['o', 'o', 'o'], ['A', 'C', 'o']]
      yarn_5 = [['o', 'B', 'x', 'o', 'o'], ['o', 'A', 'o', 'o', 'o'],\
       ['A', 'x', 'o', 'o', 'A'], ['o', 'x', 'A', 'o', 'x'],\
       ['A', 'o', 'x', 'x', 'A'], ['B', 'A', 'x', 'A', 'o']]
      dark_1 = [['x', 'o', 'o'], ['o', 'B', 'o'], ['B', 'B', 'x']]
      standard = [showstopper_4, numbered_6, mad_1, mad_4, mad_7, \
      tiny_5, yarn_5, dark_1]
      assert any([solution == x for x in standard]), 'It seems the blocks \
      are not in the right place for any of these levels' 

if __name__ == '__main__':
  filename = 'mad_1.bff'
  grid, number_of_reflect_blocks, number_of_refract_blocks, \
  number_of_opaque_blocks, initial_lazor, positions_to_intersect = \
  read_map(filename)
  read_map = read_map(filename)
  Test_Lazor().read_map_UT(read_map)
  solution = solve_grid("mad_4.bff")
  Test_Lazor().solve_grid_UT(solution, filename)
  Test_Lazor().lazors_func_UT(grid, 1, 1)
