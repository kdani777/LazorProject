'''
This file is our first attempt at the lazor project. 

**Functions**
	
	read_map:
		This function reads the map .bff file and parses the grid, what blocks are available, 
		what way the lazor is pointing, and the positions the lazor has to hit
'''

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
	for line in split_strings:
		if not in_grid:
			if line.startswith('GRID START'):
				in_grid = True
		elif line.startswith('GRID STOP'):
				in_grid = False
		else:
			grid.append(line.strip().split())

	positions_to_intersect = []
	number_of_opaque_blocks = 0
	number_of_reflect_blocks = 0
	number_of_refract_blocks = 0

	for line in split_strings:
		if line.startswith("A"): 
			number_of_reflect_blocks = line.strip().split()[1]
		elif line.startswith("B"):
			number_of_opaque_blocks = line.strip().split()[1]
		elif line.startswith("C"):
			number_of_refract_blocks = line.strip().split()[1]
		elif line.startswith("L"):
			initial_lazor = line.strip().split()[1:]
		elif line.startswith("P"):
			positions_to_intersect.append(line.strip().split()[1:])
		else:
			continue
	return grid, number_of_refract_blocks, number_of_refract_blocks, number_of_opaque_blocks, initial_lazor, positions_to_intersect

class blocks(object):
	def __init__(self):
		self.size = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
		self.grid_value = "A"

def create_refract_block():
	refract_block = blocks()
	refract_block.grid_value = "C"
	return refract_block

def create_opaque_block():
	opaque_block = blocks()
	opaque_block.grid_value = "B"
	return opaque_block

def solve_grid(filename):
	grid, number_of_refract_blocks, number_of_refract_blocks, number_of_opaque_blocks, initial_lazor, positions_to_intersect = read_map(filename)
	print grid
	new = []
	new_grid = []
	for i in range(0, 9):
		new_grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
	for i in grid:
		for j in i:
			if j != "o":
				print 0+3*i.index(j)
				for k in range(0, 3):
					for h in range(0, 3):
						new_grid[k+3*i.index(j)][h+3*i.index(j)] = 1
			else:
				continue
	

if __name__ == '__main__':
	# maps = read_map("showstopper_4.bff")
	solve_grid("showstopper_4.bff")