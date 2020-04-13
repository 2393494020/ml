#!/usr/bin/env python
# -*- coding: utf-8 -*-

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D', 'E'],
    'D': ['B', 'C', 'E', 'F'],
    'E': ['C', 'D'],
    'F': ['D'],
}

# Breadth First Search
def BFS(graph, s):
    queue = []
    queue.append(s)
    
    seen = set()
    seen.add(s)

    parent = {}
    parent[s] = None

    while len(queue) > 0:
        vertex = queue.pop(0)
        nodes = graph[vertex]
        for node in nodes:
            if node not in seen:
                queue.append(node)
                seen.add(node)
                parent[node] = vertex
        
        # print(vertex)
    return parent

if __name__ == '__main__':
    parent = BFS(graph, 'E')
    node = 'A'
    while node != None:
        print(node)
        node = parent[node]