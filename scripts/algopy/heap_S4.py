# -*- coding: utf-8 -*-
"""
Heap for graphs: contains (val, elt) / elts are integers in [0, sizeMax[ (vertices)
@author: Nathalie
"""

class Heap:
    def __init__(self, sizeMax):
        self.heap = [None]
        self.index = [-1]*sizeMax        
    
    def is_empty(self):
        return len(self.heap) == 1

    def _moveUp(self, pos):
        (val, elt) = self.heap[pos]
        while (pos > 1) and (val < self.heap[pos//2][0]):
            self.heap[pos] = self.heap[pos//2]
            self.index[self.heap[pos][1]] = pos
            pos = pos // 2
        self.heap[pos] = (val, elt)
        self.index[elt] = pos
        
        
    def push(self, elt, val):
        '''
        add (val, elt) to heap
        '''
        self.heap.append((val, elt))
        self.index[elt] = len(self.heap)-1
        self._moveUp(len(self.heap)-1)
    
    def update(self, elt, newVal):
        '''
        if elt not in heap: same as self.push(elt, newVal)
        else: updates the heap after minimization of elt's value with newVal
        '''
        pos = self.index[elt]
        if pos == -1:
            self.heap.append((newVal, elt))
            pos = len(self.heap)-1
            self.index[elt] = pos
        else:
            self.heap[pos] = (newVal, elt)
        self._moveUp(pos)
    
        
    def pop(self):
        """ 
        returns and deletes the element of smallest value in heap
        returns the pair (value, elt)    
        """
        e = self.heap[1]
        self.index[e[1]] = -1
        (val, elt) = self.heap[len(self.heap)-1]
        self.heap.pop()
        if not self.is_empty():
            n = len(self.heap)-1
            ok = False
            i = 1    
            while (i <= n // 2) and not ok:
                j = 2 * i
                if (j + 1 <= n) and (self.heap[j+1][0] < self.heap[j][0]):
                    j = j + 1
                if val > self.heap[j][0]:
                    self.heap[i] = self.heap[j]
                    self.index[self.heap[i][1]] = i
                    i = j
                else:
                    ok = True
            self.heap[i] = (val, elt)
            self.index[self.heap[i][1]] = i
            
        return e


