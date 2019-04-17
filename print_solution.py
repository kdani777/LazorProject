'''
Author: Kunal Dani, Shyanne Salen, Marina Morrow
Last Modified: April 17th, 2019

File containts ancillary functions used to reformat output from solve_grid
function into more convenient easily readable text and png files. Corresponding
image is then saved into separate file.

Functions:
    gridmaker(new_grid)

    get_colors()

    save_grid()
'''
from PIL import Image


def gridmaker(new_grid):
    '''
    Function will reformat grid from a list of list of strings
    into an array of combined elements in the form of a grid

    **Parameters**

        new_grid: *list, list, str*
            Contains solved grid for corresponding level

    **Returns**

        ng: *str*
            Reformatted array of joined list elements
    '''

    ng = '\n'.join([' '.join(i) for i in new_grid])
    return(ng)


def get_colors():
    '''
    Colors map that the maze will use:
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
        0: (169, 169, 169),
        1: (255, 255, 255),
        2: (0, 0, 0),
        3: (153, 204, 255)
    }


def save_grid(grid, name, blockSize=50):
    '''
    Function saves the grid into a new png file containing block
    images corresponding to the the type of element within the grid
    (reflect, refract, opaque blocks and open and closed grid spaces)

    **Parameters**

        grid: *list, list, int*
            Contains a list of list of integers that represent
            the block type and its corresponding color

        name: *str*
            Corresponds to the name of the level
    **Returns**

        A png will be saved with the illustrated grid
        containing the solution

    '''
    height_1 = len(grid)
    width_1 = len(grid[0])
    height = height_1 * blockSize
    width = width_1 * blockSize
    colors = get_colors()
    img = Image.new("RGB", (width, height), color=0)
    for jx in range(width_1):
        for jy in range(height_1):
            x = jx * blockSize
            y = jy * blockSize
            for i in range(1, blockSize):
                for j in range(1, blockSize):
                    img.putpixel((x + i, y + j), colors[grid[jy][jx]])
    for a in range(width):
        b = height - 1
        img.putpixel((a, b), (0, 0, 0))
    for b in range(height):
        a = width - 1
        img.putpixel((a, b), (0, 0, 0))
    if not name.endswith(".png"):
        name += ".png"
    img.save("%s" % name)
