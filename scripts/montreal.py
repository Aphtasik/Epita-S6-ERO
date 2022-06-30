import multiprocessing as mp

import numpy as np
import osmnx as ox

place = "Montreal, Canada" 
G = ox.graph_from_place(place, network_type="walk")

print(G.edges)
