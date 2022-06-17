# Imports

from algopy import graph as gh

def clearTheSnow(graph):
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
G = gh.load_weightedgraph("/home/adrie/Epita-S6-ERO/scripts/graphs/zone.wgra")
gh.display(G)
print(clearTheSnow(G))