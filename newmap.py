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
            (0.6, 'f', "32"),  # Light Green - Fields
            (0.5, 'd', "33"),  # Yellow - Desert
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

        def landmass_type(nx, ny, choice):
            if choice == "islands":
                return ridge_noise(nx, ny)
            elif choice == "mainland":
                return noise(nx, ny, scale=3)
            elif choice == "mixed":
                return ridge_noise(nx, ny) if noise(nx, ny, scale=0.3) > 0.5 else noise(nx, ny, scale=3)

        def calculate_height(nx, ny, choice):
            base_height = landmass_type(nx, ny, choice)
            detail = noise(nx, ny, scale=6)
            edge_falloff = 1 - (nx ** 2 + ny ** 2) ** 0.5
            edge_falloff = max(0, edge_falloff + (np.random.rand() - 0.5) * 0.2)
            return (base_height * 0.7 + detail * 0.3) * edge_falloff

        def add_rivers_and_lakes(heightmap):
            num_rivers = np.random.randint(3, 6)
            for _ in range(num_rivers):
                start_x, start_y = np.random.randint(0, self.width), np.random.randint(0, self.height)
                for _ in range(150):  # Simulate a river
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

        def add_mountain_ranges(heightmap):
            num_ranges = np.random.randint(2, 5)
            for _ in range(num_ranges):
                start_x, start_y = np.random.randint(0, self.width), np.random.randint(0, self.height)
                for _ in range(100):  # Simulate a mountain range
                    heightmap[start_y, start_x] = max(heightmap[start_y, start_x], 0.9)
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

        landmass_choice = np.random.choice(["islands", "mainland", "mixed"])
        for y in range(self.height):
            for x in range(self.width):
                nx, ny = (x / self.width - 0.5) * 2, (y / self.height - 0.5) * 2
                self.heightmap[y, x] = calculate_height(nx, ny, landmass_choice)

        self.heightmap = add_rivers_and_lakes(self.heightmap)
        self.heightmap = add_mountain_ranges(self.heightmap)

    def render(self):
        for row in self.tiles:
            print(''.join(f"\033[{tile.color_code}m{tile.char}\033[0m" for tile in row))

width, height = 200, 100
tilemap = Tilemap(width, height)
tilemap.gen_heightmap()
tilemap.map_tiles()
tilemap.render()