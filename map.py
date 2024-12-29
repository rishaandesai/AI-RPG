import numpy as np
import opensimplex
import time

class Tile:
    def __init__(self, char, color_code):
        self.char = char
        self.color_code = color_code

class Tilemap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.heightmap = np.zeros((height, width), dtype=np.single)
        self.tiles = []

    def map_tiles(self):
        char_map = [
            (0.9, 'M', "37"),  # White - Mountains
            (0.8, 'F', "32"),  # Green - Forest
            (0.7, 'f', "32"),  # Light Green - Fields
            (0.6, 'd', "33"),  # Yellow - Desert
            (0.5, 'g', "32"),  # Green - Grass
            (0.4, 's', "31"),  # Red - Sand
            (0.3, 'w', "34"),  # Blue - Shallow Water
            (0.0, 'W', "34"),  # Blue - Deep Water
        ]

        def set_tile(z):
            for threshold, char, color_code in char_map:
                if z >= threshold:
                    return Tile(char, color_code)
            return Tile('W', "34")  # Default to deep water

        self.tiles = [[set_tile(z) for z in row] for row in self.heightmap]

    def gen_heightmap(self, seed=None):
        if seed is None:
            seed = time.time_ns()
        opensimplex.seed(seed)

        def noise(nx, ny, scale, offset_x=0, offset_y=0):
            return opensimplex.noise2(scale * (nx + offset_x), scale * (ny + offset_y)) / 2 + 0.5

        def ridge_noise(nx, ny):
            return 2 * (0.5 - abs(0.5 - noise(nx, ny, scale=1)))

        def island_height(nx, ny):
            base = ridge_noise(nx, ny)
            detail = noise(nx, ny, scale=4)
            return base * 0.6 + detail * 0.4

        def generate_landmass_choice():
            choice = np.random.choice(["islands", "mainland", "mixed"])
            return choice

        def calculate_height(nx, ny, landmass_type):
            height = ridge_noise(nx, ny) if landmass_type == "islands" else noise(nx, ny, scale=3)
            if landmass_type == "mixed" and noise(nx, ny, scale=0.3) > 0.5:
                height = ridge_noise(nx, ny)
            edge_falloff = 1 - (nx ** 2 + ny ** 2) ** 0.5
            edge_falloff = max(0, edge_falloff + (np.random.rand() - 0.5) * 0.2)
            return height * edge_falloff

        def add_rivers_and_lakes(heightmap):
            for _ in range(5):  # Add a few rivers
                start_x, start_y = np.random.randint(0, self.width), np.random.randint(0, self.height)
                for _ in range(100):
                    heightmap[start_y, start_x] = 0.3  # Water height
                    direction = np.random.choice(["up", "down", "left", "right"])
                    if direction == "up" and start_y > 0:
                        start_y -= 1
                    elif direction == "down" and start_y < self.height - 1:
                        start_y += 1
                    elif direction == "left" and start_x > 0:
                        start_x -= 1
                    elif direction == "right" and start_x < self.width - 1:
                        start_x += 1
            return heightmap

        landmass_type = generate_landmass_choice()
        for y in range(self.height):
            for x in range(self.width):
                nx, ny = (x / self.width - 0.5) * 2, (y / self.height - 0.5) * 2
                self.heightmap[y, x] = calculate_height(nx, ny, landmass_type)

        self.heightmap = add_rivers_and_lakes(self.heightmap)

    def render(self):
        for row in self.tiles:
            print(''.join(f"\033[{tile.color_code}m{tile.char}\033[0m" for tile in row))

def generate_map():
    width, height = 200, 100
    tilemap = Tilemap(width, height)
    tilemap.gen_heightmap()
    tilemap.map_tiles()
    tilemap.render()

for i in range(12):
    generate_map()
    print()