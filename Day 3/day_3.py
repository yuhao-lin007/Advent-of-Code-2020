from math import prod

class Toboggan:
    def __init__(self, map_grid, velocity_hor, velocity_ver):
        """
        Args:
            map_grid: A 1D string list containing each row of
                the map
            velocity_hor: How many squares right the toboggan
                moves at a time
            velocity_ver: How many squares down the toboggan
                moves at a time
        """
        self.map_grid = map_grid
        self.velocity_hor = velocity_hor
        self.velocity_ver = velocity_ver
        
        self.position_x = 0
        self.position_y = 0

        self.map_height = len(self.map_grid)
        self.map_width = len(self.map_grid[0])

    def move(self):
        self.position_x += self.velocity_hor
        self.position_y += self.velocity_ver

    def is_colliding(self):
        return self.map_grid[self.position_y][self.position_x % self.map_width] == "#"

    def is_out_of_map(self):
        return self.position_y >= self.map_height

with open("input.txt", "r") as file:
    grid = [row.rstrip() for row in file]

total_trees = []
# Slope (3, 1) is for Part 1
slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
for slope in slopes:
    toboggan = Toboggan(grid, *slope)

    num_trees = 0
    while not toboggan.is_out_of_map():
        if toboggan.is_colliding():
            num_trees += 1
        toboggan.move()
    total_trees.append(num_trees)

    print(f"Slope: {slope}, Num Trees: {num_trees}")

print("Total Num Trees Product:", prod(total_trees))
