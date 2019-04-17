class lazor:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    def move(self):
        self.x += self.vx
        self.y += self.vy

def overlap(lazor_path, blocks, first_pass): 
    overlap = False
    if first_pass == False:
        if lazor_path[-2] == lazor_path[0]:
            if lazor_path[-1] == lazor_path[1]:
                x = lazor_path[-1][0]
                y = lazor_path[-1][1]
                overlap = True
    return overlap

def lazors_in_grid(grid, lazors, a):
    if lazors[a].x >= 0.0 and lazors[a].y >= 0.0:
        if lazors[a].x <= float(2*len(grid)) and lazors[a].y <= float(2*len(grid)):
            return True

def lazor_bounds_UT(grid, x, y):
    InBound = False
    if x >= 0.0 and y >= 0.0:
        if x <= float(2*len(grid)) and y <= float(2*len(grid)):
            InBound = True
    assert InBound, 'The lazor is outside the boundaries of the grid'