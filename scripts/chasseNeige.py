# Imports
import random

from algopy.graph import load_weightedgraph, todot, Graph
from algopy import queue

# Def infinite
inf = float('inf')

# Def graphs
multizone = load_weightedgraph("graphs/multizone.wgra", int)
zone = load_weightedgraph("graphs/zone.wgra", int)

# Print graphs dot files
#print(todot(zone))
#print(todot(multizone))

# Function
def eccentricity(G, src):
    """Return the eccentricity of each vertice of the graph from a given vertice

    Args:
        src: vertice from which the eccentricity is calculated

    Returns:
        array: array in which the eccentricity of a summit x is array[x]
    """
    D = [-1] * G.order
    q = queue.Queue()
    q.enqueue(src)
    D[src] = 0

    while not q.isempty():
        s = q.dequeue()
        for adj in G.adjlists[s]:
            if D[adj] == -1:
                D[adj] = D[s] + G.costs[s, adj]
                q.enqueue(adj)
    return D

def random_numbers(maximum, nb):
    """Gives an array of nb random numbers between 0 and maximum included

    Args:
        maximum (int): Max value of random included
        nb (int): number random values to get

    Returns:
        array: the array of random numbers
    """
    res = []
    for _ in range(nb):
        res.append(random.randint(0, maximum - 1))
    return res

def ite1(G, n):
    """Implementation of the Iteration1. Take random zone bases and associate
    each vertices with a zone according to the eccentricities of the zone bases

    Args:
        n (int): Number of zones to create 

    Returns:
        matrix: each list correspond to a zone with vertices number in it
    """
    # Take random zone bases
    rand = [0, 8] # TODO: Should be random in a real situation
    # rand = random_numbers(G.order, n)

    # Returned matrix, contain a vertices list for each zones
    res = [[] for _ in range(n)]

    # Create a matrix of eccentricities
    eccentricities = []
    for i in range(n):
        eccentricities.append(eccentricity(G, rand[i]))

    # Associate each vertice to a zone
    for i in range(G.order):
        mini = inf, inf
        # Go accross all eccentricity matrix and choose the nearest zone base according to eccentricity (NOT SHORTEST PATH)
        for j in range(n):
            if eccentricities[j][i] < mini[1]:
                mini = (j, eccentricities[j][i])
        res[mini[0]].append(i)

    return res

#print(ite1(multizone, 2))    

def ite2(G, n):
    """Implementation of the Iteration2. Take random zone bases and associate
    each vertices with a zone according to the eccentricities of the zone bases

    Args:
        n (int): Number of zones to create 

    Returns:
        matrix: each list correspond to a zone with vertices number in it
    """
    # If there is more engines than vertex, assign one engine for each
    if (n > G.order):
        n = G.order

    # Take random base point
    rand = random_numbers(G.order, 1)

    # Returned matrix, contain a vertices list for each zones
    res = [[] for _ in range(n)]

    # Create a matrix of eccentricities
    eccentricities = []
    # For all zones that needs to be created
    for i in range(n):
        eccentricities.append(eccentricity(G, rand[i]))

        # Create a new zone based on eccentricities,
        # The further the point is from other points, the higher the chance to be picked
        eccentricitiesSum = [0] * G.order
        for j in range(len(eccentricities)):
            for k in range(len(eccentricities[j])):
                eccentricitiesSum[k] = eccentricities[j][k]

        pickList = []
        for j in range(len(eccentricities)):
            for _ in range(len(eccentricities[j])):
                pickList.append(j)
        rand.append(random.choice(pickList))

    # Associate each vertice to a zone
    for i in range(G.order):
        mini = inf, inf
        # Go accross all eccentricity matrix and choose the nearest zone base according to eccentricity (NOT SHORTEST PATH)
        for j in range(n):
            if eccentricities[j][i] < mini[1]:
                mini = (j, eccentricities[j][i])
        res[mini[0]].append(i)

    return res

def extract_sub_graphs(G, M):
    graphList = []

    for i in range(len(M)):
        g = Graph(len(M[i]), False, True, None)
        for j in range(len(M[i])):
            for k in range(j + 1, len(M[i])):
                if M[i][k] in G.adjlists[M[i][j]]:
                    g.addedge(j, k, G.costs[M[i][j], M[i][k]])
        print(todot(g))
        graphList.append(g)
    return graphList

def print_all_graphs(graphList):
    for elt in graphList:
        print(todot(elt))

def do_the_work(G, nbZones, is_snow=None):
    print("GRAPH")
    print(todot(G))
    zones = ite2(G, nbZones)
    print("ZONES")
    print(zones)
    graphList = extract_sub_graphs(G, zones)
    print("PRINT")
    print_all_graphs(graphList)

do_the_work(zone, 2)


