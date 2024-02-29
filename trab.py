from collections import deque
import time
    
class Graph:

    def __init__(self, is_directed, adjacency_list = {}):
        self.adjacency_list = adjacency_list
        self.is_directed = is_directed

    def get_neighbors(self, v):
        return self.adjacency_list[v]

    def h(self, n):
        H = {
            'A': 10,
            'B': 8,
            'C': 5,
            'D': 7,
            'E': 3,
            'F': 6,
            'G': 5,
            'H': 3,
            'I': 3,
            'J': 1
        }
        return H[n]

    def a_star(self, start_node, stop_node):
        open_list = set([start_node])
        closed_list = set([])
        g = {}
        g[start_node] = 0
        parents = {}
        parents[start_node] = start_node

        while len(open_list) > 0:
            n = None
            for v in open_list:
                if n == None or g[v] + self.h(v) < g[n] + self.h(n):
                    n = v

            if n == None:
                print('Path does not exist!')
                return None
                
            if n == stop_node:
                reconst_path = []
                total_weight = 0
                while parents[n] != n:
                    reconst_path.append(n)
                    total_weight += self.get_weight(parents[n], n)
                    n = parents[n]
                reconst_path.append(start_node)
                reconst_path.reverse()
                total_weight += self.get_weight(start_node, reconst_path[1])
                print('Path found: {}, Total Weight: {}'.format(reconst_path, total_weight))
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

    def dfs(self, start, end):
        stack = [(start, [start], 0)]  # Added total_weight to the stack
        all_paths = []
        while stack:
            (vertex, path, total_weight) = stack.pop()
            for (neighbor, weight) in self.get_neighbors(vertex):
                if neighbor not in path:
                    if neighbor == end:
                        all_paths.append((path + [neighbor], total_weight + weight))
                    else:
                        stack.append((neighbor, path + [neighbor], total_weight + weight))
        return sorted(all_paths, key=lambda x: x[1])  # Sorting by total_weight in descending order

    def get_weight(self, node1, node2):
        for neighbor, weight in self.get_neighbors(node1):
            if neighbor == node2:
                return weight
        return float('inf')  # Assuming infinity if there's no direct edge

    def add_edge(self, source, destination, weight):
        # if source not in self.adjacency_list:
        #     self.adjacency_list.update({source: [(destination, weight)]})

        #     if not self.is_directed:
        #         self.adjacency_list.update({destination: [(source, weight)]})
                
        # else:
        #     items = self.adjacency_list.get(source)
        #     items.append((destination, weight))
        #     self.adjacency_list.update({source: items})

        #     if not self.is_directed:
        #         items = self.adjacency_list.get(destination)
        #         items.append((source, weight))
        #         self.adjacency_list.update({source: items})

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


def read_file(file_path, graph):
    with open(file_path, 'r') as file:
        lines = file.readlines()

        if len(lines) < 2:
            print('Invalid file')
            return

        source = lines[0][lines[0].find('(') + 1]
        destination = lines[1][lines[1].find('(') + 1]

        adjacency_list = {}
        i = 2
        while 'pode_ir' in lines[i]:
            aux = lines[i][lines[i].find('(') + 1 : lines[i].find(')')]
            aux = aux.split(',')
            vertex_1 = aux[0]
            vertex_2 = aux[1]
            weight = int(aux[2])

            graph.add_edge(vertex_1, vertex_2, weight)

            i += 1
        
        while lines[i].startswith('h('):
            aux = lines[i][lines[i].find('(') + 1 : lines[i].find(')')]
            aux = aux.split(',')

            i += 1



graph1 = Graph(is_directed=False)

read_file('teste.txt', graph1)


print('asdasd')
# adjacency_list = {
#     'A': [('B', 6), ('F', 3)],
#     'B': [('C', 3),('D', 2)],
#     'C': [('D', 1),('E', 5)],
#     'D': [('B', 2),('C', 1),('E', 8)],
#     'E': [('C', 5),('D', 8),('I', 5),('J', 5)],
#     'F': [('A', 3),('G', 1),('H', 7)],
#     'G': [('F', 1),('I', 3)],
#     'H': [('F', 7),('I', 2)],
#     'I': [('E', 5),('G', 3),('H', 2),('J', 3)],
#     'J': [('E', 5),('I', 3)]
# }

# graph1 = Graph(adjacency_list)
# # start_time = time.time() 
# graph1.a_star('A', 'J')
# # print("--- %s seconds ---" % (time.time() - start_time))

# print("\n")
# print("All possible paths from A to J using DFS:")
# all_paths = graph1.dfs('A', 'J')
# for path, total_weight in all_paths:
#     print("Path:", path, "Total Weight:", total_weight)
