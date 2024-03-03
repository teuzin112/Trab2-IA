from time import perf_counter_ns

class Graph:

    def __init__(self, is_directed, adjacency_list = {}, h = {}):
        self.h = h
        self.adjacency_list = adjacency_list
        self.is_directed = is_directed
        self.path_start = None
        self.path_end = None
        self.iterations = 1
        self.operations = 0

    def get_neighbors(self, v):
        return self.adjacency_list[v]

    def get_h(self, destination):
        return self.h[destination]

    def a_star(self):
        self.operations = 0
        print("-------------")

        # Inicia o contador de tempo
        initial_time = perf_counter_ns()

        # Inicializa as listas de nós a serem explorados (open_list) e que já foram explorados (closed_list)
        open_list = set([self.path_start])  # Operacao de atribuicao
        closed_list = set([])   # Operacao de atribuicao

        # Distancia até os outros nós
        current_distance = {}   # Operacao de atribuicao
        current_distance[self.path_start] = 0   # Operacao de atribuicao

        # Declara e inicializa o dicionario do pai de cada nó 
        parents = {}    # Operacao de atribuicao
        parents[self.path_start] = self.path_start  # Operacao de atribuicao

        # Variaveis para medicao do desempenho
        self.operations += 6
        self.iterations = 1

        # Enquanto existir nó a ser explorado
        while len(open_list) > 0:   # Operacao de comparacao e iteracao
            node = None     # Operacao de atribuicao
            self.operations += 2
            for vertex in open_list:    # Operacao de iteracao
                self.operations += 1

                # Encontra o melhor nó a ser explorado 
                if node == None or current_distance[vertex] + self.get_h(vertex) < current_distance[node] + self.get_h(node):   # Operacao de comparacao
                    node = vertex   # Operacao de atribuicao
                    self.operations += 1

                    if node == None:    # Caso a primeira condicao do if seja verdadeira, adiciona somente uma operacao
                        self.operations += 1
                    else:   # Caso contrario adiciona 3 (Duas somas e uma comparacao)
                        self.operations += 3
                    
            if node == None:    # Operacao de comparacao
                self.operations += 1

                print('Nao existe caminho!')
                return None
            
            print("-------------\n")
            print("Iteracao: %s" % (self.iterations))
            print("Numero de operacoes: %s" % (self.operations))
            self.iterations += 1
            print("No atual: " + str(node))
            print("Vizinhos atuais:" + str(self.get_neighbors(node)))
            

            # Se chegou ao ponto final
            if node == self.path_end:   # Operacao de comparacao
                reconst_path = []   # Operacao de atribuicao
                total_weight = 0    # Operacao de atribuicao

                self.operations += 2

                # Acumula todos os pontos e pesos do melhor caminho
                while parents[node] != node:    # Operacao de comparacao
                    reconst_path.append(node)   # Operacao de atribuicao
                    total_weight += self.get_weight(parents[node], node)    # Operacao de atribuicao e soma
                    node = parents[node]    # Operacao de atribuicao
                    self.operations += 5
                reconst_path.append(self.path_start)    # Operacao de atribuicao
                reconst_path.reverse()      # Operacao de atribuicao

                self.operations += 2
                print("\n-------------\n")
                print('Caminho encontrado: {}, Peso total: {}'.format(reconst_path, total_weight))
                final_time = perf_counter_ns()
                print("--- Tempo total de execucao: %s nanosegundos ---" % (final_time-initial_time))

                # f = open("aestrela_resultados.txt", "a")
                # f.write("%s\n" % (final_time-initial_time))
                # f.close()
                return reconst_path

            # Para todos os vizinhos do nó atual
            for (neighbor, weight) in self.get_neighbors(node):     # Operacao de comparacao e duas atribuicoes
                self.operations += 3

                # Se o vizinho ainda não foi explorado
                if neighbor not in open_list and neighbor not in closed_list:   # M + N comparacoes considerando o pior caso
                    self.operations += len(open_list) + len(closed_list)

                    # Adiciona o vizinho à lista de nós a serem explorados e coloca o nó atual como seu pai
                    open_list.add(neighbor)     # Operacao de atribuicao
                    parents[neighbor] = node    # Operacao de atribuicao
                    current_distance[neighbor] = current_distance[node] + weight    # Operacao de atribuicao e soma

                    self.operations += 4

                else:
                    # Verifica se é melhor visitar o nó atual antes de visitar o vizinho, se sim, atualiza as listas de exploração
                    if current_distance[neighbor] > current_distance[node] + weight:    # Operacao de comparacao e soma
                        current_distance[neighbor] = current_distance[node] + weight    # Operacao de atribuicao e soma
                        parents[neighbor] = node    # Operacao de atribuicao

                        self.operations += 5
                        if neighbor in closed_list:     # Operacao de iteracao
                            self.operations += 1

                            closed_list.remove(neighbor)    # Operacao de atribuicao
                            open_list.add(neighbor)     # Operacao de atribuicao

                            self.operations += 2

            # Terminou de explorar o nó
            open_list.remove(node)      # Operacao de atribuicao
            closed_list.add(node)       # Operacao de atribuicao

            self.operations += 2
            
            print("Nos ja explorados: %s" % (closed_list))
            print("Proximos nos a serem explorados: %s" % (open_list))
            print("\n-------------\n")

            self.operations += 1

        print('Nao existe caminho!')
        return None

    def dfs_visit(self, v, end, visited, path, total_weight):
        # print("-------------\n")
        # print("Iteracao: %s" % (self.iterations))
        # print("Numero de operacoes: %s" % (self.operations))
        # self.iterations += 1
        # print("No atual: " + str(v))
        # print("Vizinhos atuais:" + str(self.get_neighbors(v)))
        # print("\n-------------\n")

        visited.add(v)      # Operacao de atribuicao
        path.append(v)      # Operacao de atribuicao

        # self.operations += 2

        if v == end:        # Operacao de comparacao
            # self.operations += 1

            return path, total_weight

        for (neighbour, weight) in self.get_neighbors(v):       # Duas operacoes de atribuicao mais a de iteracao
            # self.operations += 2

            if neighbour not in visited:        # Operacao de comparacao N vezes considerando o pior caso
                # self.operations += len(visited)

                new_path, new_weight = self.dfs_visit(neighbour, end, visited, path, total_weight + weight)     # Duas operacoes de atribuicao e uma de soma

                # self.operations += 3

                if new_path:        # Operacao de comparacao
                    # self.operations += 1

                    return new_path, new_weight
        
            # self.operations += 1

        path.pop()  # Operacao de atribuicao

        # self.operations += 1
        return None

    def dfs(self):
        # self.iterations = 1
        # self.operations = 0

        visited = set()     # Operacao de atribuicao
        path = []       # Operacao de atribuicao
        total_weight = 0        # Operacao de atribuicao

        # self.operations += 3


        initial_time = perf_counter_ns()

        # print(self.dfs_visit(self.path_start, self.path_end, visited, path, total_weight))

        final_time = perf_counter_ns()
        # print("--- Tempo total de execucao: %s nanosegundos ---" % (final_time-initial_time))
        print(final_time-initial_time)
        f = open("dfs_resultados.txt", "a")
        f.write("%s\n" % (final_time-initial_time))
        f.close()

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
