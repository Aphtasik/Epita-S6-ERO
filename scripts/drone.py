from algopy import graph as gh
from algopy import queue
from theg import * 

import multiprocessing as mp
import numpy as np
import osmnx as ox
import random

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
    G = gh.Graph(n, False, True)
    for (x, y, _) in edges:
        adjlist[x].append(y)
        G.costs.update({(x, y): 0})
    G.adjlists = adjlist
    return G

def get_interesting_nodes(graph, edges):
    """
    Returns a list of nodes that are interesting to the drone.
    """
    res = []
    P = find_maximum_matching(graph.order, edges)
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

def cleaning_graph(graph, edges):
    """
    Returns an optimal version of the interesting nodes.
    """
    # edges = convert_to_edges(graph)
    mark = [(None, None, 0)] * len(edges)
    int_nodes = get_interesting_nodes(graph, edges)
    for node in int_nodes:
        for neigbors in graph.adjlists[node]:
            if (neigbors in int_nodes):
                if (node, neigbors, 0) in edges:
                    mark[edges.index((node, neigbors, 0))] = (node, neigbors, 0)
                else:
                    mark[edges.index((neigbors, node, 0))] = (neigbors, node, 0)
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
                tmp = 0 # mark[edges.index(edge)][0] if mark[edges.index(edge)][0] != None else mark[edges.index(edge)][1]
                if mark[edges.index(edge)][0] != None:
                    tmp = mark[edges.index(edge)][0]
                elif mark[edges.index(edge)][1] != None:
                    mark[edges.index(edge)][1]
                else:
                    continue # in order to skip the (None, None) case
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
    return node_a + node_b


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
    data = osmgraph.edges(data=True)
    # using the third value of edges as boolean for snow
    tmp = []
    for node in data:
        tmp.append((node[0], node[1], 0))
    edges = to_soft_id_graph(tmp)
    g = convert_to_adjlists(len(osmgraph.nodes), edges)
    cleaned = cleaning_graph(g)
    int_nodes = find_best_path(cleaned, g)
    for node in int_nodes:
        for neigbors in g.adjlists[node]:
            color = random.randint(0,1) # coloring the graph randomly
            g.costs.update({(node, neigbors): color})
    return g

############################################

CORRESPONDENCE_TABLE = {}
CORRESPONDENCE_TABLE_PRIME = {}

def get_true_node(soft_id):
    if soft_id in CORRESPONDENCE_TABLE_PRIME:
        return CORRESPONDENCE_TABLE_PRIME[soft_id]
    return -1

def to_soft_id_graph(graph_city):
    global CORRESPONDENCE_TABLE_PRIME
    global CORRESPONDENCE_TABLE
    
    CORRESPONDENCE_TABLE_PRIME = {}
    CORRESPONDENCE_TABLE = {}
    
    graph_city_soft_id = []
    soft_id = 0
    
    len_g = len(graph_city)
    index = 0
    
    old_percentage = -1
    for (node1,node2,dist) in graph_city:
        if node1 not in  CORRESPONDENCE_TABLE:
            CORRESPONDENCE_TABLE[node1] = soft_id
            CORRESPONDENCE_TABLE_PRIME[soft_id] = node1
            soft_id += 1
            
        if node2 not in  CORRESPONDENCE_TABLE:
            CORRESPONDENCE_TABLE[node2] = soft_id
            CORRESPONDENCE_TABLE_PRIME[soft_id] = node2
            
            soft_id += 1
        s_id1 = CORRESPONDENCE_TABLE[node1]
        s_id2 = CORRESPONDENCE_TABLE[node2]
        graph_city_soft_id.append((s_id1,s_id2, dist))
    return graph_city_soft_id

def to_real_id_graph(graph_city_soft_id):
    graph_city = []
    soft_id = 0
    for (node1,node2,dist) in graph_city_soft_id:
        n_id1 = get_true_node(node1)
        n_id2 = get_true_node(node2)
    
        graph_city.append((n_id1,n_id2, dist))
    return graph_city

def to_real_id_path(path_soft_id):
    path = []
    soft_id = 0
    for (node1,node2) in path_soft_id:
        n_id1 = get_true_node(node1)
        n_id2 = get_true_node(node2)
    
        path.append(n_id1)
    return path

#######################################################

def cut_city(place, n):
    """
    cut the city in small parts
    """
    G = ox.graph_from_place(place, network_type="drive")
    nodes = G.nodes(data=True)
    counter = len(G.nodes) // n
    i = counter
    res = []
    for node in nodes:
        if (len(res) >= n):
            break
        i-=1 
        if (i <= 0):
            tmp = ox.truncate.truncate_graph_dist(G,node[0],max_dist=1500)
            res.append(tmp)
            print(len(tmp.nodes))
            i = counter
    return res

def Process_drone():
    place = "Montreal, Canada"
    part = cut_city(place, 1)
    res = color_graph(part[0])
    return gh.todot(res) 

# print(Process_drone())
