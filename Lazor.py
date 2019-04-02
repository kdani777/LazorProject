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

if __name__ == '__main__':
	maps = read_map("mad_1.bff")
	print(maps)