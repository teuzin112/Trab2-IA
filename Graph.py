from time import perf_counter_ns

class Graph:

    def __init__(self, is_directed, adjacency_list = {}, h = {}):
        self.h = h
        self.adjacency_list = adjacency_list
        self.is_directed = is_directed
        self.path_start = None
        self.path_end = None
        self.iterations = 1

    def get_neighbors(self, v):
        return self.adjacency_list[v]

    def get_h(self, destination):
        return self.h[destination]

    def a_star(self):
        print("-------------")

        # Inicia o contador de tempo
        initial_time = perf_counter_ns()

        # Inicializa as listas de nós a serem explorados (open_list) e que já foram explorados (closed_list)
        open_list = set([self.path_start])
        closed_list = set([])

        # Distancia até os outros nós
        current_distance = {}
        current_distance[self.path_start] = 0

        # Declara e inicializa o dicionario do pai de cada nó 
        parents = {}
        parents[self.path_start] = self.path_start

        self.iterations = 1
        # Enquanto existir nó a ser explorado
        while len(open_list) > 0:
            node = None
            for vertex in open_list:

                # Encontra o melhor nó a ser explorado 
                if node == None or current_distance[vertex] + self.get_h(vertex) < current_distance[node] + self.get_h(node):
                    node = vertex

            if node == None:
                print('Nao existe caminho!')
                return None
            
            print("-------------\n")
            print("Iteracao: %s" % (self.iterations))
            self.iterations += 1
            print("No atual: " + str(node))
            print("Vizinhos atuais:" + str(self.get_neighbors(node)))
            

            # Se chegou ao ponto final
            if node == self.path_end:
                reconst_path = []
                total_weight = 0

                # Acumula todos os pontos e pesos do melhor caminho
                while parents[node] != node:
                    reconst_path.append(node)
                    total_weight += self.get_weight(parents[node], node)
                    node = parents[node]
                reconst_path.append(self.path_start)
                reconst_path.reverse()
                print("\n-------------\n")
                print('Caminho encontrado: {}, Peso total: {}'.format(reconst_path, total_weight))
                final_time = perf_counter_ns()
                print("--- Tempo total de execucao: %s nanosegundos ---" % (final_time-initial_time))

                f = open("aestrela_resultados.txt", "a")
                f.write("%s\n" % (final_time-initial_time))
                f.close()
                return reconst_path

            # Para todos os vizinhos do nó atual
            for (neighbor, weight) in self.get_neighbors(node):

                # Se o vizinho ainda não foi explorado
                if neighbor not in open_list and neighbor not in closed_list:

                    # Adiciona o vizinho à lista de nós a serem explorados e coloca o nó atual como seu pai
                    open_list.add(neighbor)
                    parents[neighbor] = node
                    current_distance[neighbor] = current_distance[node] + weight

                else:
                    # Verifica se é melhor visitar o nó atual antes de visitar o vizinho, se sim, atualiza as listas de exploração
                    if current_distance[neighbor] > current_distance[node] + weight:
                        current_distance[neighbor] = current_distance[node] + weight
                        parents[neighbor] = node
                        if neighbor in closed_list:
                            closed_list.remove(neighbor)
                            open_list.add(neighbor)

            # Terminou de explorar o nó
            open_list.remove(node)
            closed_list.add(node)
            print("Nos ja explorados: %s" % (closed_list))
            print("Proximos nos a serem explorados: %s" % (open_list))
            print("\n-------------\n")

        print('Nao existe caminho!')
        return None

    def dfs_visit(self, v, end, visited, path, total_weight):
        print("-------------\n")
        print("Iteracao: %s" % (self.iterations))
        self.iterations += 1
        print("No atual: " + str(v))
        print("Vizinhos atuais:" + str(self.get_neighbors(v)))
        print("\n-------------\n")

        visited.add(v)
        path.append(v)

        if v == end:
            return path, total_weight

        for (neighbour, weight) in self.get_neighbors(v):
            if neighbour not in visited:
                new_path, new_weight = self.dfs_visit(neighbour, end, visited, path, total_weight + weight)
                if new_path:
                    return new_path, new_weight

        path.pop()  # Backtrack if no path is found
        return None

    def dfs(self):
        self.iterations = 1

        visited = set()
        path = []
        total_weight = 0

        print(self.dfs_visit(self.path_start, self.path_end, visited, path, total_weight))

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
