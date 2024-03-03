from collections import deque
from time import perf_counter_ns
    
class Graph:

    def __init__(self, is_directed, adjacency_list = {}, h = {}):
        self.h = h
        self.adjacency_list = adjacency_list
        self.is_directed = is_directed
        self.path_start = None
        self.path_end = None

    def get_neighbors(self, v):
        return self.adjacency_list[v]

    def get_h(self, destination):
       
        return self.h[destination]

    def a_star(self):
        t = perf_counter_ns()
        open_list = set([self.path_start])
        closed_list = set([])
        g = {}
        g[self.path_start] = 0
        parents = {}
        parents[self.path_start] = self.path_start

        while len(open_list) > 0:
            n = None
            for v in open_list:
                if n == None or g[v] + self.get_h(v) < g[n] + self.get_h(n):
                    n = v

            if n == None:
                print('Path does not exist!')
                return None
                
            if n == self.path_end:
                reconst_path = []
                total_weight = 0
                while parents[n] != n:
                    reconst_path.append(n)
                    total_weight += self.get_weight(parents[n], n)
                    n = parents[n]
                #reconst_path.append(self.path_start)
                #reconst_path.reverse()
                #print('Path found: {}, Total Weight: {}'.format(reconst_path, total_weight))
                e = perf_counter_ns()
                print("--- %s nanoseconds ---" % (e-t))
                return reconst_path

            for (m, weight) in self.get_neighbors(n):
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n
                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None

    def dfs(self):
        t = perf_counter_ns()
        stack = [(self.path_start, [self.path_start], 0)]  # Added total_weight to the stack
        all_paths = []
        while stack:
            (vertex, path, total_weight) = stack.pop()
            for (neighbor, weight) in self.get_neighbors(vertex):
                if neighbor not in path:
                    if neighbor == self.path_end:
                        all_paths.append((path + [neighbor], total_weight + weight))
                    else:
                        stack.append((neighbor, path + [neighbor], total_weight + weight))
        e = perf_counter_ns()
        print("--- %s nanoseconds ---" % (e-t))
        #all_paths = sorted(all_paths, key=lambda x: x[1])  # Sorting by total_weight in descending order

       # for path, total_weight in all_paths:
        #    print("Path:", path, "Total Weight:", total_weight)

    def get_weight(self, node1, node2):
        for neighbor, weight in self.get_neighbors(node1):
            if neighbor == node2:
                return weight
        return float('inf')  # Assuming infinity if there's no direct edge

    def add_edge(self, source, destination, weight):
        items = self.adjacency_list.get(source)
        if items:
            items.append((destination, weight))
        else:
            items = [(destination, weight)]

        self.adjacency_list.update({source: items})

        if not self.is_directed:
            items = self.adjacency_list.get(destination)
            if items:
                items.append((source, weight))
            else:
                items = [(source, weight)]

            self.adjacency_list.update({destination: items})

    def add_h(self, destination, h):
        self.h.update({destination: h})