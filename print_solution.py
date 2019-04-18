'''
Authors: Kunal Dani, Marina Morrow, Shyanne Salen
Last Modified: April 17th, 2019
Lazor Project
Software Carpentry
print_solution

This file makes the grid readable and saves the grid as an image.

***Functions***
    gridmaker
        This functions joins the grid as a string to make it look nice 
        in a txt file.

    get_colors
        This function assigns a r, g, and b value to a number to be able
        to access certain colors quickly.

    save_grid
        This function uses a grid to save an image of the solved grid as 
        a png file.
'''

from PIL import Image

def gridmaker(new_grid):
    '''
    This function takes a grid which is in a list of lists form and
    makes it a string for easier exporting.

    ***Parameters***
        new_grid: *list*
            This is a list of list of each row of the solved grid.

    ***Returns***
        ng: *str*
            This is a string of the values in new grid.
    '''
    ng = '\n'.join([' '.join(i) for i in new_grid])
    return ng

def get_colors():
    '''
    This function assigns a value to set colors to easily be able to
    assign colors to a block.

    Colors that the grid will use:
        0 - Black - An opaque block
        1 - White - A reflect block
        2 - Gray - The background
        3 - Light blue - A refract block

    **Returns**

        color_map: *dict, int, tuple*
            A dictionary that will correlate the integer key to
            a color.
    '''
    return {
        0: (169,169,169),
        1: (255, 255, 255),
        2: (0, 0, 0),
        3: (153, 204, 255)
    }

def save_grid(grid, name, blockSize=50):
    '''
    This function saves the solved grid as a png image file.

    ***Parameters***
        grid: *list*
            This is a list of lists of the rows in the solved grid.
        name: *str*
            This is the name of the level to save the image as this name.
        blockSize: *int* **Optional**
            This is the size of the blocks in pixels.
    '''
    nBlocks = len(grid)
    height = len(grid)
    width = len(grid[0])
    new_height = height * blockSize
    new_width = width * blockSize
    colors = get_colors()
    img = Image.new("RGB", (new_width, new_height), color=0)
    for jx in range(width):
        for jy in range(height):
            x = jx * blockSize
            y = jy * blockSize
            for i in range(1, blockSize):
                for j in range(1, blockSize):
                    img.putpixel((x + i, y + j), colors[grid[jy][jx]])
    for a in range(new_width):
        b = new_height-1
        img.putpixel((a,b), (0, 0, 0))
    for b in range(new_height):
        a = new_width-1
        img.putpixel((a,b), (0, 0, 0))
    if not name.endswith(".png"):
        name += ".png"
    img.save("%s" % name)
