from algopy import graph as gh
from algopy import queue
from theg import * 


def convert_to_edges(graph):
    """
    Converts a graph to a list of edges.
    """
    edges = []
    for node in range(len(graph.adjlists)):
        for neighbor in graph.adjlists[node]:
            if (node < neighbor):
                edges.append((node, neighbor))
    return edges

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
    mark = [(None, None)] * len(edges)
    int_nodes = get_interesting_nodes(graph)
    for node in int_nodes:
        for neigbors in graph.adjlists[node]:
            if (neigbors in int_nodes):
                if (node, neigbors) in edges:
                    mark[edges.index((node, neigbors))] = (node, neigbors)
                else:
                    mark[edges.index((neigbors, node))] = (node, neigbors)
            else:
                mark[edges.index((node, neigbors))] = (node, None)
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
                tmp = edge[0] if edge[0] != None else edge[1]
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
            mark[i] = (None, mark[i][1])
        elif (node == mark[i][1]):
            mark[i] = (mark[i][0], None)

def compute_distance(graph, node_a, node_b):
    # TODO:
    return 42;

def find_best_path(int_nodes, graph):
    """
    find the best path for the drone between all interesting nodes
    int_nodes represent a list of all interesting nodes 
    return a list ordered by closest interesting nodes
    """
    M = [ False ] * len(int_nodes)   
    M[0] = True
    nodes = [i for i in int_nodes]
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


x = gh.load_weightedgraph("./graphs/test2.wgra")
y = get_interesting_nodes(x)
print(y)
z = cleaning_graph(x)
print(z)









