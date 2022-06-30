from algopy import graph as gh
from algopy import queue
from theg import * 

import multiprocessing as mp
import numpy as np
import osmnx as ox

def convert_to_edges(graph):
    """
    Converts a graph to a list of edges.
    """
    edges = []
    cost = {}
    for node in range(len(graph.adjlists)):
        for neighbor in graph.adjlists[node]:
            if (node < neighbor):
                edges.append((node, neighbor, graph.costs[node, neighbor]))
    return edges

def convert_to_adjlists(n, edges):
    adjlist = [ [] for _ in range(n) ]
    G = graph(n, False, True);
    for (x, y, _) in edges:
        adjlist[x].append(y)
        G.costs.update({(x, y): 0})
    G.adjlists = adjlist
    return G

def get_interesting_nodes(graph):
    """
    Returns a list of nodes that are interesting to the drone.
    """
    res = []
    P = find_maximum_matching(graph.order, convert_to_edges(graph))
    for (src,dst) in P:
        res.append(src)
        res.append(dst)
    return res

def find_node_edges(node, edges):
    res = []
    for x in edges:
        if (node in x):
            res.append(x)
    return res

def cleaning_graph(graph):
    """
    Returns an optimal version of the interesting nodes.
    """
    edges = convert_to_edges(graph)
    mark = [(None, None, 0)] * len(edges)
    int_nodes = get_interesting_nodes(graph)
    for node in int_nodes:
        for neigbors in graph.adjlists[node]:
            if (neigbors in int_nodes):
                if (node, neigbors, 0) in edges:
                    mark[edges.index((node, neigbors, 0))] = (node, neigbors, 0)
                else:
                    mark[edges.index((neigbors, node, 0))] = (node, neigbors, 0)
            else:
                mark[edges.index((node, neigbors, 0))] = (node, None, 0)
    return supress_nodes(int_nodes, edges, mark)
    
def supress_nodes(int_nodes, edges, mark):
    """
    supress the useless nodes in the interesting nodes
    """
    to_keep = []
    for node in int_nodes:
        node_edges = find_node_edges(node, edges)
        flag = True # node will be unmarked if set to true
        for edge in node_edges:
            if None in mark[edges.index(edge)]: # if a node is single colored and not already in tokeep, we add it
                tmp = mark[edges.index(edge)][0] if mark[edges.index(edge)][0] != None else mark[edges.index(edge)][1]
                if not tmp in to_keep:
                    to_keep.append(tmp)
                flag = False
        if (flag):
            update_mark(node, mark)
    return to_keep

def update_mark(node, mark):
    """
    update the marked vertices list by replacing node by None
    """
    for i in range(len(mark)):
        if (node == mark[i][0]):
            mark[i] = (None, mark[i][1], 0)
        elif (node == mark[i][1], 0):
            mark[i] = (mark[i][0], None, 0)

def compute_distance(graph, node_a, node_b):
    return node_a + node_b;


def find_best_path(int_nodes, graph):
    """
    find the best path for the drone between all interesting nodes
    int_nodes represent a list of all interesting nodes 
    return a list ordered by closest interesting nodes
    """
    M = [ False ] * len(int_nodes)   
    M[0] = True
    nodes = [i for i in range(len(int_nodes))]
    curr_node = 0
    path = [0]
    miniind = 1
    for _ in range(len(nodes) - 1):
        mini = float('inf')
        for node in nodes:
            distance = compute_distance(graph, int_nodes[curr_node], int_nodes[node])
            if (mini > distance and not M[node]):
                mini = distance 
                miniind = node 
        path.append(int_nodes[miniind])
        M[miniind] = True;
        curr_node = miniind
    return path

def color_graph(osmgraph):
    edges = osmgraph.edges
    # using the third value of edges as boolean for snow
    for i in range(len(edges)):
        if edges[i] == (_, _, 1):
            edges[i] = (edges[i][0], edges[i][1], 0)
    g = convert_to_adjlists(len(osmgraph.nodes), edges);
    cleaned = cleaning_graph(g)
    int_nodes = find_best_path(cleaned, g)
    for node in int_nodes:
        for neigbors in g.adjlists[node]:
            color = randint(0,1) # coloring the graph randomly
            g.costs.update({(node, neigbors): color})
    return g

place = "Montreal, Canada"
G = ox.graph_from_place(place, network_type="drive")
print(G.edges[125])
# G3 = ox.truncate.truncate_graph_dist(G,17,max_dist=1000)
# g = color_graph(G)
# print(g.adjlists)

