import numpy as np
import opensimplex
import time
from biome import biome, map_legend


class Tilemap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.heightmap = np.zeros((height, width), dtype=np.single)
        self.tiles = []

    def map_tiles(self):
        # Map the height values to biomes based on thresholds defined in map_legend
        def get_biome(z):
            if z >= 0.9:
                return "Snowy Mountain"
            elif z >= 0.8:
                return "Mountain"
            elif z >= 0.7:
                return "Dense Forest"
            elif z >= 0.6:
                return "Light Forest"
            elif z >= 0.5:
                return "Plains"
            elif z >= 0.4:
                return "Swamp"
            elif z >= 0.3:
                return "River"
            elif z >= 0.0:
                return "Deep Ocean"
            return "Deep Ocean"

        self.tiles = [[get_biome(z) for z in row] for row in self.heightmap]

    def gen_heightmap(self, seed=None):
        if seed is None:
            seed = time.time_ns()
        opensimplex.seed(seed)

        def noise(nx, ny, scale, offset_x=0, offset_y=0):
            return opensimplex.noise2(scale * (nx + offset_x), scale * (ny + offset_y)) / 2 + 0.5

        def ridge_noise(nx, ny):
            return 2 * (0.5 - abs(0.5 - noise(nx, ny, scale=1)))

        def calculate_height(nx, ny):
            base = ridge_noise(nx, ny)
            detail = noise(nx, ny, scale=4)
            edge_falloff = 1 - (nx ** 2 + ny ** 2) ** 0.5
            edge_falloff = max(0, edge_falloff + (np.random.rand() - 0.5) * 0.2)
            return (base * 0.6 + detail * 0.4) * edge_falloff

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

        for y in range(self.height):
            for x in range(self.width):
                nx, ny = (x / self.width - 0.5) * 2, (y / self.height - 0.5) * 2
                self.heightmap[y, x] = calculate_height(nx, ny)

        self.heightmap = add_rivers_and_lakes(self.heightmap)

    def render(self):
        for row in self.tiles:
            print(''.join(biome(tile) for tile in row))


def generate_map(width=100, height=30):
    tilemap = Tilemap(width, height)
    tilemap.gen_heightmap()
    tilemap.map_tiles()
    tilemap.render()


for i in range(3):  # Generate and display 3 maps as an example
    generate_map()
    print()