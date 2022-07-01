import sys
import drone
import chasseNeigeZone as cnz
import chasseNeige as cn
import osmnx as ox
from algopy import graph as gf
from theg import path

def osnxgraphToNormalGraph(G):
    data = G.edges(data=True)
    tmp = []
    for node in data:
        tmp.append((node[0], node[1], node["length"]))
    edges = drone.to_soft_id_graph(tmp)
    ng = gf.Graph(len(data.nodes))
    for e in edges:
        ng.addedge(e)
    return ng
            
def main(arg):
    if len(arg) != 1:
        print("Use only 1 argument, 1 for demonstratrion, 2 for Montreal application")
    else:
        if arg[0] == "1":
            print("[*]Demonstration start")
            normalGraph = gf.load_weightedgraph("./graphs/complex.wgra")
            (graphlist, zoneref) = cn.do_the_work(normalGraph, 500)
            print("[-]Determining area done")
            print()
            print("[+]Starting cleaning")
            (paths, costs) = cnz.cleanArea(graphlist)
            print("[-]Cleaning done")
            print("[*]Results:")
            print("Total cost: " + "{:.2f}".format(sum(costs)))
            for i in range(0, len(paths)):
                print("    cost:" + "{:.2f}".format(costs[i]))
                print(paths[i])
        elif arg[0] == "2":
            place = "Montreal, Canada"
            osmnxGraph = ox.graph_from_place(place, network_type="drive")
            x = osmnxGraph.edges(data=True)
            snowGraph = drone.color_graph(osmnxGraph) # zone with wheight indicating if they are snowy
            normalGraph = osnxgraphToNormalGraph(osmnxGraph)
            # Zone shit #
            (graphlist, zoneref) = cn.do_the_work(normalGraph, 500, snowGraph)
            ##
            paths = cnz.cleanArea(graphlist, snowGraph)
            print(paths)
if __name__ == "__main__":
   main(sys.argv[1:])