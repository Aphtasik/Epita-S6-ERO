# Imports

from algopy import graph as gh

def clearTheSnow1(graph):
    """Pass by all edges to clear the snow
    As we do not have to bother with one ways we can directly pass by all edges in order of apparition
    still, we must be warry of returning to a node where all the edges have already been cleared just because it come first,
    to do that the algorithm must remember which nodes reached which node, so that it does not goes on the way back too early
    """
    gh.sortgraph(graph)
    PRecord = []
    for _ in range(graph.order):
        PRecord.append([])
    currentNode = 0
    nextNode = 0
    path = []
    while (1):
        if (not graph.adjlists[currentNode]):
            return path
        for i in graph.adjlists[currentNode]:
            nextNode = i
            if (not i in PRecord[currentNode]):
                PRecord[i].append(currentNode)
                break
        graph.removeedge(currentNode, nextNode)
        path.append((currentNode, nextNode))
        currentNode = nextNode
    return PRecord

#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
######################################################################################################################################

import numpy as np
import importlib as iplib
import fleury as fleury
iplib.reload(fleury)

# transformation du graph vers un graph eulerien
def odd_vertices(n, edges):
    deg = [0] * n
    for (a,b,c) in edges:
        deg[a] += 1
        deg[b] += 1

    return [a for a in range(n) if deg[a] % 2]

def is_edges(n, edges, node1, node2):
    for (a, b, c) in edges:
        if (a == node1 and b == node2) or (a == node2 and b == node1):
            return (a,b,c)
    return None

def list_edges(n, edges, l_vodd):
    res = []
    index = 1
    for a in l_vodd:
        index+=1
        for b in l_vodd:
            if (a == b):
                continue
            tmp = is_edges(n, edges, a, b)
            if (tmp and tmp not in res) :
                #print("MATCH:", a, b)
                res.append(tmp)
    return res

def shortest_edge_idx(l_edges):
    if (len(l_edges) == 0):
        return None
    shortest = l_edges[0][2]
    shortest_index = 0

    index = 1
    for (a,b,c) in l_edges[1:]:
        if (c < shortest):
            shortest = c
            shortest_index = index
        index+=1
    return l_edges[shortest_index]

def transform_to_eulerian(n, edges):
    list_vodd = odd_vertices(n, edges)
    l_edges = list_edges(n, edges, list_vodd)

    len_vodd = len(list_vodd)
    if (len_vodd == 2 or len_vodd == 0): #case is already eulerian
        return edges
    #print(list_vodd)
    #print(l_edges)
    while(len(list_vodd) != 2):
        list_vodd = odd_vertices(n, edges)
        l_edges = list_edges(n, edges, list_vodd)

        shortest_edge = shortest_edge_idx(l_edges)
        #add edge between two
        (a,b,c) = shortest_edge
        new_edge = (b,a,c)
        edges.append(new_edge)

        #delete from vodd
        if (a in list_vodd):
            list_vodd.remove(a)
        if (b in list_vodd):
            list_vodd.remove(b)

        #delete from list_edges
        l_edges.remove(shortest_edge)
    return edges

#adapter le format de notre graph au format dictionnaire de l'algo "fleury"
def to_dict(G):
    dict_graph = {}
    for (a,b) in G:
        dict_graph[a] = []
        dict_graph[b] = []
    for (a,b) in G:
        dict_graph[a].append(b)
        dict_graph[b].append(a)
    return dict_graph


#On utlise toutes les fonctions précedement définies:
def converttoedgelist(graph):
    edgelist = []
    for i in range(0, graph.order):
        for j in graph.adjlists[i]:
            edgelist.append((i, j, graph.costs[(i, j)]))
    return edgelist

def transform_and_find_eulerian_path(graph):
    graph = converttoedgelist(graph)
    graph = transform_to_eulerian(len(graph), graph)
    graph2 = []
    for (a,b,c) in graph:
        graph2.append((a,b))

    dict_graph2 = to_dict(graph2)
    E_path = fleury.fleury(dict_graph2)
    return E_path


# Tests
# G = gh.load_weightedgraph("/home/adrie/Epita-S6-ERO/scripts/graphs/zone.wgra")
# gh.display(G)
# print(clearTheSnow1(G))

def cleanArea(listGraph, snowedPaths=None):
    listPath = []
    costs = []
    for i in range(0, len(listGraph)):
        listPath.append(transform_and_find_eulerian_path(listGraph[i]))
        costs.append(getWeightFromPath(listGraph[i], listPath[i]))
    return listPath, costs

# There was an intermediate function
# def cleanArea2Medium(listGraph):
#     listPath = []
#     for i in listGraph:
#         listPath.append(Chinese_Postman(i))

def cleanAreaBad(listGraph):
    listPath = []
    for i in listGraph:
        listPath.append(clearTheSnow1(i))

def getWeightFromPath(G, path):
    acu = 0
    for i in path:
        acu += G.costs[(i[0], i[1])]
    return acu

# G = gh.load_weightedgraph("/home/adrie/Epita-S6-ERO/scripts/graphs/zone.wgra")

# heck = transform_and_find_eulerian_path(G)
# print(getWeightFromPath(G, heck))
# chineseParty = Chinese_Postman(G)
# print(getWeightFromPath(G, chineseParty))