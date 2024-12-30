from utils.map import Graph
from utils.terrain import assign_terrain_types_to_graph

g = Graph(N=250, iterations=2)
assign_terrain_types_to_graph(graph=g, min_water_ratio=0.25)
g.assign_corner_elevations()
g.redistribute_elevations()
g.assign_center_elevations()
g.create_rivers(n=30, min_height=0.6)
g.assign_moisture()
g.assign_biomes()
g.plot_full_map(
    plot_type='biome',
    debug_height=False, 
    debug_moisture=False, 
    downslope_arrows=False, 
    rivers=True)