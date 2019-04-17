from PIL import Image

def gridmaker(new_grid):
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
        0: (169,169,169),
        1: (255, 255, 255),
        2: (0, 0, 0),
        3: (153, 204, 255)
    }

def save_grid(grid, name, blockSize=50):
    nBlocks = len(grid)
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
        b = height-1
        img.putpixel((a,b), (0, 0, 0))
    for b in range(height):
        a = width-1
        img.putpixel((a,b), (0, 0, 0))
    if not name.endswith(".png"):
        name += ".png"
    img.save("%s" % name)
