from Lazor import solve_grid
from Read_map import read_map

class Test_Lazor(object):

  def read_map_UT(self, grid, read_map):
    for row in grid:
      for value in row:
        assert (type(grid) == list), "The grid is not a list"
        assert (type(row) == list), 'The rows of the grid are not lists'
        assert (type(value) == str), 'The values in the grid are not strings'
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

  def solve_grid_UT(self, solution, filename):
    for row in solution:
      for value in row:
        assert (type(row) == list and type(value) == str), 'The final grid' \
        'is not the correct type'
    if filename == 'showstopper_4.bff' or 'mad_1.bff' or 'numbered_6.bff' or \
      'mad_4.bff' or 'mad_7.bff' or 'tiny_5.bff' or 'yarn_5.bff' or 'dark_1.bff':
      showstopper_4 = [['B', 'A', 'B'], ['B', 'o', 'A'], ['A', 'o', 'B']]
      numbered_6 = [['B', 'o', 'o'], ['A', 'x', 'x'], ['B', 'o', 'A'], \
        ['A', 'x', 'o'], ['B', 'o', 'o']]
      mad_1 = [['o', 'o', 'C', 'o'], ['o', 'o', 'o', 'A'],\
        ['A', 'o', 'o', 'o'], ['o', 'o', 'o', 'o']]
      mad_4 = [['o', 'o', 'o', 'o'], ['o', 'A', 'o', 'o'], \
        ['A', 'o', 'o', 'o'], ['o', 'A', 'o', 'A'], ['o', 'o', 'A', 'o']]
      mad_7 = [['o', 'o', 'A', 'o', 'o'], ['o', 'o', 'o', 'A', 'o'], \
        ['A', 'o', 'A', 'o', 'x'], ['o', 'o', 'o', 'A', 'o'], \
        ['o', 'o', 'A', 'o', 'o']]
      tiny_5 = [['A', 'B', 'A'], ['o', 'o', 'o'], ['A', 'C', 'o']]
      yarn_5 = [['o', 'B', 'x', 'o', 'o'], ['o', 'A', 'o', 'o', 'o'], \
         ['A', 'x', 'o', 'o', 'A'], ['o', 'x', 'A', 'o', 'x'], \
         ['A', 'o', 'x', 'x', 'A'], ['B', 'A', 'x', 'A', 'o']]
      dark_1 = [['x', 'o', 'o'], ['o', 'B', 'o'], ['B', 'B', 'x']]
      standard = [showstopper_4, numbered_6, mad_1, mad_4, mad_7, tiny_5,\
      yarn_5, dark_1]
      assert any([read_map == x for x in standard]), 'It seems the blocks ' \
        'are not in the right place for any of these levels' 

if __name__ == '__main__':
  filename = 'mad_1.bff'
  grid, number_of_reflect_blocks, number_of_refract_blocks, \
  number_of_opaque_blocks, initial_lazor, positions_to_intersect = \
  read_map(filename)
  read_map = read_map(filename)
  Test_Lazor().read_map_UT(grid, read_map)
  solution = solve_grid("mad_1.bff")
  print solution
  Test_Lazor().solve_grid_UT(solution, filename)
