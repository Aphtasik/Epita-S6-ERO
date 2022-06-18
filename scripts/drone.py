from algopy import graph as gh
from algopy import queue
from theg import * as theg

def convert_to_edges(graph):
    """
    Converts a graph to a list of edges.
    """
    edges = []
    for node in graph.adjlists:
        for neighbor in graph.adjlists[node]):
            if (node < neighbor):
                edges.append((node, neighbor))
    return edges

def get_interesting_nodes(graph):
    """
    Returns a list of nodes that are interesting to the drone.
    """
    res = []
    P = theg.find_maximum_matching(graph.order, convert_to_edges(graph))
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
    mark = [(None, None)] * len(edges)
    int_nodes = get_interesting_nodes(graph)
    for node in int_nodes:
        for neigbors in graph.adjlists[node]:
            if (neighbor in int_nodes):
                mark[edges.index((node, neigbors))] = (node, neigbors)
            else:
                mark[edges.index((node, neigbors))] = (node, None)
    to_keep = []
    for node in int_nodes:
        node_edges = find_node_edges(node, edges)
        for edge in node_edges:
            if None in mark[edges.index(edge)]:
                    to_keep.append(edge[0])
    return to_keep



