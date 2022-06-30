# Imports

from cmath import inf
from webbrowser import Galeon
from algopy import graph as gh

G = gh.load_weightedgraph("/home/adrie/Epita-S6-ERO/scripts/graphs/zone.wgra")
gh.display(G)

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

# Tests
# G = gh.load_weightedgraph("/home/adrie/Epita-S6-ERO/scripts/graphs/zone.wgra")
# gh.display(G)
# print(clearTheSnow1(G))
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
def dijkstra(graph, src, dest):
    ind = src
    if src == dest:
        return 0
    inf = float('inf')
    min = inf
    shortest = [inf for _ in range(graph.order)]
    for i in graph.adjlists[src]:
        shortest[i] = graph.costs[(src, i)]
        if min < graph.costs[(src, i)]:
            min = graph.costs[(src, i)]
            ind = i
    shortest[src] = 0
    selected = [src]
    # Dijkstra
    while(ind!=dest):
        for i in range(graph.order):
            if i not in selected:
                if i in graph.adjlists[ind]:
                    #Check if distance needs to be updated
                    if((graph.costs[(ind, i)] + min) < shortest[i]):
                        shortest[i] = graph.costs[(ind, i)] + min
        temp_min = inf
        
        for j in range(graph.order):
            if j not in selected:
                if(shortest[j] < temp_min):
                    temp_min = shortest[j]
                    ind = j
        min = temp_min
        selected.append(ind)
    
    return shortest[dest]
 
def get_odd(graph):
    degrees = [0 for i in range(graph.order)]
    for i in range(graph.order):
            degrees[i]=len(graph.adjlists[i])
                
    odds = [i for i in range(len(degrees)) if degrees[i]%2!=0]
    print('odds are:',odds)
    return odds

def gen_pairs(odds):
    pairs = []
    for i in range(len(odds)-1):
        pairs.append([])
        for j in range(i+1,len(odds)):
            pairs[i].append([odds[i],odds[j]])
        
    print('pairs are:',pairs)
    return pairs

def DFSCount(graph, v, visited):
        count = 1
        visited[v] = True
        for i in graph.adjlists[v]:
            if visited[i] == False:
                count = count + DFSCount(graph, i, visited)        
        return count

def isValidNextEdge(graph, u, v):
        # The edge u-v is valid in one of the following two cases:
  
          #  1) If v is the only adjacent vertex of u
        if len(graph.adjlists[u]) == 1:
            return True
        else:
            '''
             2) If there are multiple adjacents, then u-v is not a bridge
                 Do following steps to check if u-v is a bridge
  
            2.a) count of vertices reachable from u'''   
            visited =[False]*(graph.order)
            count1 = DFSCount(graph, u, visited)
 
            '''2.b) Remove edge (u, v) and after removing the edge, count
                vertices reachable from u'''
            graph.removeedge(u, v)
            graph.removeedge(v, u)
            visited =[False]*(graph.order)
            count2 = DFSCount(graph, u, visited)
 
            #2.c) Add the edge back to the graph
            graph.addedge(u,v)
 
            # 2.d) If count1 is greater, then edge (u, v) is a bridge
            return False if count1 > count2 else True

def printEulerUtil(graph, u):
        #Recur for all the vertices adjacent to this vertex
        for v in graph.adjlists[u]:
            #If edge u-v is not removed and it's a a valid next edge
            if isValidNextEdge(graph, u, v):
                print("%d-%d " %(u,v)),
                graph.removeedge(u, v)
                printEulerUtil(graph, v)

def Chinese_Postman(graph):
    odds = get_odd(graph)
    if(len(odds)==0):
        printEulerUtil(graph, 0)

    pairs = gen_pairs(odds)
    l = (len(pairs)+1)//2
    pairings_sum = []
    
    def get_pairs(pairs, done = [], final = []):
        if(pairs[0][0][0] not in done):
            done.append(pairs[0][0][0])
            
            for i in pairs[0]:
                f = final[:]
                val = done[:]
                if(i[1] not in val):
                    f.append(i)
                else:
                    continue
                
                if(len(f)==l):
                    pairings_sum.append(f)
                    return 
                else:
                    val.append(i[1])
                    get_pairs(pairs[1:],val, f)
                    
        else:
            get_pairs(pairs[1:], done, final)
            
    get_pairs(pairs)
    min_sums = []
    
    for i in pairings_sum:
        s = 0
        for j in range(len(i)):
            s += dijkstra(graph, i[j][0], i[j][1])
        min_sums.append(s)
    
    added_dis = float(inf)
    min_index = 0
    for i in range(0, len(min_sums)):
        if (min_sums[i] < added_dis):
            added_dis = min_sums[i]
            min_index = i
    
    for i in pairings_sum[min_index]:
        graph.addedge(i[0], i[1])
    
    notLoadedG = gh.Graph(graph.order)
    for a in range(0, graph.order):
        for b in graph.adjlists[a]:
            notLoadedG.addedge(a, b)
    printEulerUtil(notLoadedG, 0)

G = gh.load_weightedgraph("/home/adrie/Epita-S6-ERO/scripts/graphs/zone.wgra")
Chinese_Postman(G)

####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################

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

heck = transform_and_find_eulerian_path(gh.load_weightedgraph("/home/adrie/Epita-S6-ERO/scripts/graphs/zone.wgra"))
print(heck)