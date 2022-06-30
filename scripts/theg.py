import math
###################################################################
# Week 1
###################################################################

def odd_vertices(n, edges):
    deg = [0] * n
    for (a,b) in edges:
        deg[a] += 1
        deg[b] += 1
    return [a for a in range(n) if deg[a] % 2]


def is_simple(n, edges):
    mat = [[0] * n for i in range(n)]
    for (a, b) in edges:
        if a == b or mat[a][b]:
            return False
        mat[a][b] = True
        mat[b][a] = True
    return True


def is_connected(n, edges):
    if n == 0:
        return True
    # Convert to adjacency list
    succ = [[] for a in range(n)]
    for (a,b) in edges:
        succ[a].append(b)
        succ[b].append(a)
    # DFS over the graph
    touched = [False] * n
    touched[0] = True
    todo = [0]
    while todo:
        s = todo.pop()
        for d in succ[s]:
            if not touched[d]:
                touched[d] = True
                todo.append(d)
    return sum(touched) == n


def is_edge_connected(n, edges):
    if n == 0 or len(edges) == 0:
        return True
    # Convert to adjacency list
    succ = [[] for a in range(n)]
    for (a,b) in edges:
        succ[a].append(b)
        succ[b].append(a)
    # DFS over the graph, starting from one extremity of the first edge
    touched = [False] * n
    init = edges[0][0]
    touched[init] = True
    todo = [init]
    while todo:
        s = todo.pop()
        for d in succ[s]:
            if not touched[d]:
                touched[d] = True
                todo.append(d)
    return all(touched[a] or not succ[a] for a in range(n))

###################################################################
# Week 2
###################################################################

def odd_vertices(n, edges):
    deg = [0] * n
    for (a,b) in edges:
        deg[a] += 1
        deg[b] += 1
    return [a for a in range(n) if deg[a] % 2]

def is_edge_connected(n, edges):
    if n == 0 or len(edges) == 0:
        return True
    # Convert to adjacency list
    succ = [[] for a in range(n)]
    for (a,b) in edges:
        succ[a].append(b)
        succ[b].append(a)
    # BFS over the graph, starting from one extremity of the first edge
    touched = [False] * n
    init = edges[0][0]
    touched[init] = True
    todo = [init]
    while todo:
        s = todo.pop()
        for d in succ[s]:
            if touched[d]:
                continue
            touched[d] = True
            todo.append(d)
    for a in range(n):
        if succ[a] and not touched[a]:
            return False
    return True

def is_eulerian(n, edges):
    return is_edge_connected(n, edges) and not odd_vertices(n, edges)


def nedge(a, b):
    return (a, b) if a < b else (b, a)

def is_eulerian_cycle(n, edges, cycle):
    if len(edges) != len(cycle):
        return False
    if len(edges) == 0:
        return True
    eset = {}
    for (a, b) in edges:
        s = nedge(a, b)
        if s in eset:
            eset[s] += 1
        else:
            eset[s] = 1
    for (a, b) in zip(cycle, cycle[1:]+cycle[0:1]):
        s = nedge(a, b)
        if s in eset and eset[s] > 0:
            eset[s] -= 1
        else:
            return False
    for val in eset.values():
        if val != 0:
            return False
    return True


def odd_vertices(n, edges):
    deg = [0] * n
    for (a,b) in edges:
        deg[a] += 1
        deg[b] += 1
    return [a for a in range(n) if deg[a] % 2]

def is_edge_connected(n, edges):
    if n == 0 or len(edges) == 0:
        return True
    # Convert to adjacency list
    succ = [[] for a in range(n)]
    for (a,b) in edges:
        succ[a].append(b)
        succ[b].append(a)
    # BFS over the graph, starting from one extremity of the first edge
    touched = [False] * n
    init = edges[0][0]
    touched[init] = True
    todo = [init]
    while todo:
        s = todo.pop()
        for d in succ[s]:
            if touched[d]:
                continue
            touched[d] = True
            todo.append(d)
    for a in range(n):
        if succ[a] and not touched[a]:
            return False
    return True

def is_eulerian(n, edges):
    return is_edge_connected(n, edges) and not odd_vertices(n, edges)

def find_eulerian_cycle(n, edges):
    assert is_eulerian(n, edges)
    if len(edges) == 0:
        return []
    cycle = [edges[0][0]] # start somewhere
    while True:
        rest = []
        for (a, b) in edges:
            if cycle[-1] == a:
                cycle.append(b)
            elif cycle[-1] == b:
                cycle.append(a)
            else:
                rest.append((a,b))
        if not rest:
            assert cycle[0] == cycle[-1]
            return cycle[0:-1]
        edges = rest
        if cycle[0] == cycle[-1]:
            # Rotate the cycle so that the last state
            # has some outgoing edge in EDGES.
            for (a, b) in edges:
                if a in cycle:
                    idx = cycle.index(a)
                    cycle = cycle[idx:-1] + cycle[0:idx+1]
                    break

###################################################################
# Week 3
###################################################################

def single_source_distances(n,edges,src):
    # Classic Bellman-Ford for undirected graphs
    dist = [math.inf] * n
    dist[src] = 0
    for k in range(n - 1):
        for (s, d, w) in edges:
            dist[d] = min(dist[d], dist[s] + w)
            dist[s] = min(dist[s], dist[d] + w)
    # Extra loop to detect negative cycles
    for (s, d, w) in edges:
        if dist[d] > dist[s] + w or dist[s] > dist[d] + w:
            return None
    return dist


def single_source_distances(n,edges,src):
    # Classic Bellman-Ford for directed graphs
    dist = [math.inf] * n
    dist[src] = 0
    for k in range(n - 1):
        for (s, d, w) in edges:
            dist[d] = min(dist[d], dist[s] + w)
    # Extra loop to detect negative cycles
    for (s, d, w) in edges:
        if dist[d] > dist[s] + w:
            return None
    return dist


def adjlist(n,edges):
    succ = [[] for i in range(n)]
    for (a,b) in edges:
        succ[a].append(b)
    return succ

def eccentricity(n,edges,i):
    succ = adjlist(n,edges)
    dist = [math.inf for i in range(n)]
    seen = [False] * n
    dist[i] = 0
    seen[i] = True
    todo = [i]
    while todo:
        s = todo.pop(0)
        dstdist = dist[s] + 1
        for d in succ[s]:
            if not seen[d]:
                dist[d] = dstdist
                seen[d] = True
                todo.append(d)
    return max(dist)

###################################################################
# Week 4
###################################################################

def init_mat(n, edges, op_plus, e_plus, op_times, e_times):
  M = [[e_plus for _ in range(n)] for _ in range(n)]
  for i in range(n):
    M[i][i] = e_times
  for (a,b,w) in edges:
    M[a][b] = w
  return M


def floyd_warshall(n, edges, op_plus, e_plus, op_times, e_times):
  # Generalised Floyd-Warshall algorithm

  M_last = init_mat(n, edges, op_plus, e_plus, op_times, e_times)

  # Floyd-Warshall triple loop
  for k in range(n):
    M_current = [[None for _ in range(n)] for _ in range(n)]
    for i in range(n):
      for j in range(n):
        M_current[i][j] = op_plus(M_last[i][j], op_times(M_last[i][k], M_last[k][j]))
    M_last = M_current

  return M_current


def init_mat(n, edges, op_plus, e_plus, op_times, e_times):
  # Set up the matrix
  M = [[e_plus for _ in range(n)] for _ in range(n)]
  # Matrix for the successors of each vertex
  Succ = [[None for _ in range(n)] for _ in range(n)]

  # Diag elems
  for i in range(n):
    M[i][i] = e_times
    Succ[i][i] = i

  # Add the edges
  for (a,b,w) in edges:
    M[a][b] = w
    Succ[a][b] = b

  return M, Succ

def path(Succ, i, j):
  assert len(Succ) == len(Succ[0])
  assert (0 <= i < len(Succ)) and (0 <= j < len(Succ))

  if Succ[i][j] is None:
    return []

  path = [i]
  while i != j:
    i = Succ[i][j]
    path.append(i)
  return path

def floyd_warshall(n, edges, op_plus, e_plus, op_times, e_times):
  # Generalised Floyd-Warshall algorithm
  # with successor computation

  M_last, Succ = init_mat(n, edges, op_plus, e_plus, op_times, e_times)

  # Floyd-Warshall triple loop
  for k in range(n):
    M_current = [[None for _ in range(n)] for _ in range(n)]
    for i in range(n):
      for j in range(n):
        M_current[i][j] = op_plus(M_last[i][j], op_times(M_last[i][k], M_last[k][j]))
        # Check if changed
        if M_current[i][j] != M_last[i][j]:
          Succ[i][j] = Succ[i][k]
    M_last = M_current

  return M_current, Succ


#### Part 2
def init_mat(n, edges, op_plus, e_plus, op_times, e_times):
  # Set up the matrix
  M = [[e_plus for _ in range(n)] for _ in range(n)]
  # Matrix for the successors of each vertex
  Succ = [[None for _ in range(n)] for _ in range(n)]

  # Diag elems
  for i in range(n):
    M[i][i] = e_times
    Succ[i][i] = i

  # Add the edges
  for (a,b,w) in edges:
    assert M[a][b] == e_plus
    M[a][b] = w
    Succ[a][b] = b

  return M, Succ

def path_i2j(Succ, i, j):
  assert len(Succ) == len(Succ[0])
  assert (0 <= i < len(Succ)) and (0 <= j < len(Succ))

  if Succ[i][j] is None:
    return []

  path = [i]
  while i != j:
    i = Succ[i][j]
    path.append(i)
  return path

def floyd_warshall(n, edges, op_plus, e_plus, op_times, e_times):
  # Generalised Floyd-Warshall algorithm
  # with successor computation

  M_last, Succ = init_mat(n, edges, op_plus, e_plus, op_times, e_times)

  # Floyd-Warshall triple loop
  for k in range(n):
    M_current = [[None for _ in range(n)] for _ in range(n)]
    for i in range(n):
      for j in range(n):
        M_current[i][j] = op_plus(M_last[i][j], op_times(M_last[i][k], M_last[k][j]))
        # Check if changed
        if M_current[i][j] != M_last[i][j]:
          Succ[i][j] = Succ[i][k]
    M_last = M_current

  return M_current, Succ



########## Part 3
## In addition to part 2
def safest_path(n, edges, i, j):
  M,S = floyd_warshall(n,edges, op_max, 0., op_mul, 1.)
  return path_i2j(S, i, j)


###################################################################
# Week 5
###################################################################

def edgeset(edges):
    "Convert a list of undirected edges to a set of directed edges."
    alledges = set()
    for (a,b) in edges:
        alledges.add((a,b))
        alledges.add((b,a))
    return alledges

def is_matching(n, edges, matching):
    alledges = edgeset(edges)
    matched = [False] * n
    for (a,b) in matching:
        if (a,b) not in alledges or matched[a] or matched[b]:
            return False
        matched[a] = True
        matched[b] = True
    return True

def edgeset(edges):
    "Convert a list of undirected edges to a set of directed edges."
    alledges = set()
    for (a,b) in edges:
        alledges.add((a,b))
        alledges.add((b,a))
    return alledges
    
def is_maximal_matching(n, edges, matching):
    alledges = edgeset(edges)
    matched = [False] * n
    for (a,b) in matching:
        if (a,b) not in alledges or matched[a] or matched[b]:
            return False
        matched[a] = True
        matched[b] = True
    return all(matched[a] or matched[b] for (a,b) in edges)


def is_matching(n,edges,pairs):
    # Note: This is a quadratic implementation of is_matching().  Can you see why?
    # Can you guess the complexity of the implementation given in the solution for the first question?
    seen = [False] * n
    for (a,b) in pairs:
        if ((a,b) not in edges) and ((b,a) not in edges):
            return False
        if seen[a] or seen[b]:
            return False
        seen[a] = seen[b] = True 
    return True

def is_perfect_matching(n,edges,matching):
    if (n % 2) or (n/2 != len(matching)):
        return False
    return is_matching(n,edges,matching)


def edgeset(edges):
    "build a set of edges with both directions"
    alledges = set()
    for (a,b) in edges:
        alledges.add((a,b))
        alledges.add((b,a))
    return alledges

def adjlists(n, edges, matchingedges):
    succ_matching = [[] for i in range(n)]
    succ_nonmatching = [[] for i in range(n)]
    for (a,b, _) in edges:
        s = succ_matching if (a,b) in matchingedges else succ_nonmatching
        s[a].append(b)
        s[b].append(a)
    return succ_matching, succ_nonmatching

def find_augmenting_path(n, edges, matching):
    freevertices = [True] * n
    for (a,b) in matching:
        freevertices[a] = freevertices[b] = False
    succ_matching, succ_nonmatching = adjlists(n, edges, edgeset(matching))

    # DFS-based exploration of all possible alternating paths starting from start.
    seen = [False] * n    
    def rec(start):
        seen[start] = True
        # start should be followed by a non-matching edge
        for y in succ_nonmatching[start]:
            if seen[y]:
                continue
            if freevertices[y]:
                return [start, y]
            seen[y] = True
            # and then a matching edge
            for z in succ_matching[y]:
                if seen[z]:
                    continue
                # and then again non-matching edge...
                res = rec(z)
                if res is not None:
                    return [start, y] + res
            # Erase "seen" on backtrack
            # This unfortunately causes the algorithm to become exponential 
            # in the worst case since it explores all possibles alternating paths.
            # For a polynomial implementation lookup Edmonds' Blossom algorithm.
            seen[y] = False
        seen[start] = False
        return None
        
    for start,isfree in enumerate(freevertices):
        if isfree:
            res = rec(start)
            if res:
                return res;
    return None

# Normalize edges so that vertices are increasing    
def normedge(e):
    return e if e[0] < e[1] else (e[1], e[0])

def update_matching(matching, augpath):
    m = { normedge(e) for e in matching }
    p = { normedge(e) for e in zip(augpath, augpath[1:])}
    return list(m ^ p)
    
def find_maximum_matching(n, edges):
    matching = []
    p = find_augmenting_path(n, edges, matching)
    while p is not None:
        matching = update_matching(matching, p)
        p = find_augmenting_path(n, edges, matching)
    return matching


###################################################################
# Week 6
###################################################################
