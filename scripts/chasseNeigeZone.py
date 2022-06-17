# Imports

from algopy import graph as gh

def clearTheSnow(graph):
    gh.sortgraph(graph)
    """Passage record (PRecord) is here to record from which node the last movement to a certain node came from"""
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