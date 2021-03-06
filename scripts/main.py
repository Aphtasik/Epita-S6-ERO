import sys
import drone
import chasseNeigeZone as cnz
import chasseNeige as cn
from algopy import graph as gf
from theg import path

def osnxgraphToNormalGraph(G):
    data = G.edges(data=True)
    tmp = []
    l = 0
    for node in data:
        tmp.append((node[0], node[1], node[2]["length"]))
        l+=1
    edges = drone.to_soft_id_graph(tmp)
    ng = gf.Graph(l)
    for (a, b, e) in edges:
        ng.addedge(a, b, e)
    return ng

def translateNode(path, zoneref):
    n = len(zoneref)
    resPath = [[] * n for i in range(n)]
    for i in range(0, len(zoneref)):
        for (a,b) in path[i]:
            resPath[i].append((zoneref[i][a], zoneref[i][b]))
    return resPath


def main(arg):
    if len(arg) != 1:
        print("Use only one argument, 1 for Montreal application, 2 for demonstration")
    else:            
        if arg[0] == "1":
            try:
                import osmnx as ox
            except:
                print("osmnx not installed, use pip3 install osmnx")
            print("Start Montreal application")
            print("- Downloading Montreal map, this can take some time")
            place = "Montreal, Canada"
            osmnxGraph = ox.graph_from_place(place, network_type="drive")
            print("- Montreal downloaded")
            x = osmnxGraph.edges(data=True)
            # snowGraph = drone.color_graph(osmnxGraph) # zone with wheight indicating if they are snowy
            print("- Snow road located")
            normalGraph = osnxgraphToNormalGraph(osmnxGraph) # nique
        else:
            normalGraph = gf.load_weightedgraph("./graphs/complex.wgra")
        print("[*]Demonstration start")
        print("[+]Determination of areas")
        (graphlist, zoneref) = cn.do_the_work(normalGraph, 500)
        print("[-]Determining area done")
        print("    Number of areas:", len(graphlist))
        print("[+]Starting cleaning")
        print(graphlist)
        print(zoneref)
        (paths, costs) = cnz.cleanArea(graphlist)
        print("[-]Cleaning done")
        print("[*]Results:")
        print("Total cost: " + "{:.2f}".format(sum(costs)), "\n")
        paths = translateNode(paths, zoneref)
        for i in range(0, len(paths)):
            print("path", i, ": cost:" + "{:.2f}".format(costs[i]))
            print(paths[i])
        print("[*]End demonstration")
if __name__ == "__main__":
   main(sys.argv[1:])