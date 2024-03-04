from time import perf_counter_ns
from collections import deque

class Graph:

    def __init__(self, adjacency_list = {}, h = {}):
        self.h = h      # Dicionário para armazenar o valor das heurísticas do ponto final em relação a todos os outros pontos
        self.adjacency_list = adjacency_list        # Lista de adjacência que representa o grafo propriamente dito
        self.path_start = None      # Ponto inicial
        self.path_end = None        # Ponto final
        self.iterations = 1     # Número de iterações
        self.operations = 0     # Número de operações

    # Retorna os vizinhos de um nó v
    def get_neighbors(self, v):
        return self.adjacency_list[v]

    # Retorna a heurística de um destination
    def get_h(self, destination):
        return self.h[destination]

    # Algoritmo A* propriamente implementado
    def a_star(self):
        self.operations = 0
        print("-------------")

        initial_time = perf_counter_ns()        # Variável auxiliar para calcular o tempo de execução

        # Inicializa as listas de nós a serem explorados (open_list) e que já foram explorados (closed_list)
        open_list = set([self.path_start])  # Operação de atribuição
        closed_list = set([])   # Operação de atribuição

        # Distancia até os outros nós
        current_distance = {}   # Operação de atribuição
        current_distance[self.path_start] = 0   # Operação de atribuição

        # Declara e inicializa o dicionario do pai de cada nó 
        parents = {}    # Operação de atribuição
        parents[self.path_start] = self.path_start  # Operação de atribuição

        # Variaveis para medicao do desempenho
        self.operations += 6
        self.iterations = 1

        # Enquanto existir nó a ser explorado
        while len(open_list) > 0:   # Operação de comparação e iteracao
            node = None     # Operação de atribuição
            self.operations += 2
            for vertex in open_list:    # Operação de iteracao
                self.operations += 1

                # Encontra o melhor nó a ser explorado 
                if node == None or current_distance[vertex] + self.get_h(vertex) < current_distance[node] + self.get_h(node):   # Operação de comparação
                    node = vertex   # Operação de atribuição
                    self.operations += 1

                    if node == None:    # Caso a primeira condicao do if seja verdadeira, adiciona somente uma Operação
                        self.operations += 1
                    else:   # Caso contrario adiciona 3 (Duas somas e uma comparação)
                        self.operations += 3
                    
            if node == None:    # Operação de comparação
                self.operations += 1

                print('Nao existe caminho!')
                return None
            
            print("-------------\n")
            print("Iteracao: %s" % (self.iterations))
            print("Numero de operacoes: %s" % (self.operations))
            self.iterations += 1
            print("No atual: " + str(node))
            print("Vizinhos atuais: " + str(self.get_neighbors(node)))
            

            # Se chegou ao ponto final
            if node == self.path_end:   # Operação de comparação
                # Inicializa uma lista para reconstruir o caminho
                reconst_path = []   # Operação de atribuição
                total_weight = 0    # Operação de atribuição

                self.operations += 2

                # Acumula todos os pontos e pesos do melhor caminho
                while parents[node] != node:    # Operação de comparação
                    # Adiciona o nó atual ao caminho reconstruído
                    reconst_path.append(node)   # Operação de atribuição
                    total_weight += self.get_weight(parents[node], node)    # Operação de atribuição e soma

                    # Move para o nó pai
                    node = parents[node]    # Operação de atribuição
                    self.operations += 5
                # Adiciona o nó inicial ao final da lista de reconstituição
                reconst_path.append(self.path_start)    # Operação de atribuição
                # Inverte o caminho reconstruído para obtê-lo do início ao fim
                reconst_path.reverse()      # Operação de atribuição

                self.operations += 2
                print("\n-------------\n")
                
                i = 0
                print('Caminho encontrado: [', end='')
                while i < len(reconst_path) - 1:
                    print(reconst_path[i] + " - ", end='')
                    i += 1
                print(reconst_path[i], end=']   ')
                print('Peso total: {}'.format(total_weight))

                final_time = perf_counter_ns()      # Variável auxiliar para calcular o tempo de execução
                print("--- Tempo total de execucao: %s nanosegundos ---" % (final_time-initial_time))
                print("--- Numero total de iteracoes: %s ---" % (self.iterations))
                print("--- Numero total de operacoes: %s ---" % (self.operations))

                return reconst_path

            # Para todos os vizinhos do nó atual
            for (neighbor, weight) in self.get_neighbors(node):     # Operação de comparação e duas atribuicoes
                self.operations += 3

                # Se o vizinho ainda não foi explorado
                if neighbor not in open_list and neighbor not in closed_list:   # M + N comparacoes considerando o pior caso
                    self.operations += len(open_list) + len(closed_list)

                    # Adiciona o vizinho à lista de nós a serem explorados e coloca o nó atual como seu pai
                    open_list.add(neighbor)     # Operação de atribuição
                    parents[neighbor] = node    # Operação de atribuição
                    current_distance[neighbor] = current_distance[node] + weight    # Operação de atribuição e soma

                    self.operations += 4

                else:
                    # Verifica se é melhor visitar o nó atual antes de visitar o vizinho, se sim, atualiza as listas de exploração
                    if current_distance[neighbor] > current_distance[node] + weight:    # Operação de comparação e soma
                        current_distance[neighbor] = current_distance[node] + weight    # Operação de atribuição e soma
                        parents[neighbor] = node    # Operação de atribuição

                        self.operations += 5
                        if neighbor in closed_list:     # Operação de iteracao
                            self.operations += 1

                            closed_list.remove(neighbor)    # Operação de atribuição
                            open_list.add(neighbor)     # Operação de atribuição

                            self.operations += 2

            # Terminou de explorar o nó
            open_list.remove(node)      # Operação de atribuição
            closed_list.add(node)       # Operação de atribuição

            self.operations += 2
            
            print("Nos ja explorados: %s" % (closed_list))
            print("Proximos nos a serem explorados: %s" % (open_list))
            print("\n-------------\n")

            self.operations += 1

        print('Nao existe caminho!')
        return None

    # Método auxiliar recursiva que executa o algoritmo DFS
    def dfs_visit(self, v, end, visited, path, total_weight):
        print("-------------\n")
        print("Iteracao: %s" % (self.iterations))
        print("Numero de operacoes: %s" % (self.operations))
        self.iterations += 1
        print("No atual: " + str(v))
        print("Vizinhos atuais: " + str(self.get_neighbors(v)))
        print("Nos ja explorados: " + str(visited))
        print("\n-------------\n")

        visited.add(v)      # Operação de atribuição
        path.append(v)      # Operação de atribuição

        self.operations += 2

        # Se o nó atual é o final então caminho encontrado
        if v == end:        # Operação de comparação
            self.operations += 1

            return path, total_weight

        # Explora os vizinhos do nó atual
        for (neighbour, weight) in self.get_neighbors(v):       # Duas operacoes de atribuição mais a de iteracao
            self.operations += 2

            if neighbour not in visited:        # Operação de comparação N vezes considerando o pior caso
                self.operations += len(visited)

                new_path, new_weight = self.dfs_visit(neighbour, end, visited, path, total_weight + weight)     # Duas operacoes de atribuição e uma de soma

                self.operations += 3

                if new_path:        # Operação de comparação
                    self.operations += 1

                    return new_path, new_weight
        
            self.operations += 1

        # Caso não tenha um caminho no nó atual, remove o último nó da pilha do caminho
        path.pop()  # Operação de atribuição

        self.operations += 1
        return None, None

    # Método principal para executar o algoritmo DFS
    def dfs(self):
        self.iterations = 1
        self.operations = 0

        visited = set()     # Operação de atribuição
        path = []       # Operação de atribuição
        total_weight = 0        # Operação de atribuição

        self.operations += 3

        initial_time = perf_counter_ns()        # Variável auxiliar para calcular o tempo de execução
        path, final_weight = self.dfs_visit(self.path_start, self.path_end, visited, path, total_weight)
        final_time = perf_counter_ns()      # Variável auxiliar para calcular o tempo de execução

        i = 0
        print('Caminho encontrado: [', end='')
        while i < len(path) - 1:
            print(path[i] + " - ", end='')
            i += 1
        print(path[i], end=']   ')
        print('Peso total: {}'.format(final_weight))

        print("--- Tempo total de execucao: %s nanosegundos ---" % (final_time-initial_time))
        print("--- Numero total de iteracoes: %s ---" % (self.iterations))
        print("--- Numero total de operacoes: %s ---" % (self.operations))

    # Método que retorna o peso da aresta entre dois nos
    def get_weight(self, node1, node2):
        for neighbor, weight in self.get_neighbors(node1):
            if neighbor == node2:
                return weight
        return float('inf')  # Assumindo infinito se nao existir a aresta

    # Método para adicionar uma aresta ao grafo
    def add_edge(self, source, destination, weight):
        items = self.adjacency_list.get(source)
        if items:
            items.append((destination, weight))
        else:
            items = [(destination, weight)]

        self.adjacency_list.update({source: items})

    # Método para adicionar um valor da funcao heuristica do grafo
    def add_h(self, destination, h):
        self.h.update({destination: h})

    def bfs(self):
        self.operations = 0
        self.iterations = 0

        initial_time = perf_counter_ns()        # Variável auxiliar para calcular o tempo de execução
        visited = set()     # Operação de atribuição

        # Inicializa uma fila com o nó inicial
        queue = deque([self.path_start])        # Duas operações de atribuição

        parents = {}        # Operação de atribuição
        parents[self.path_start] = None     # Operação de atribuição

        total_weight = 0
        self.operations += 5

        while queue:    # Operação de comparação
            self.iterations += 1
            current_node = queue.popleft()      # Operação de atribuição
            visited.add(current_node)       # Operação de atribuição

            self.operations += 3


            print("-------------\n")
            print("Iteracao: %s" % (self.iterations))
            print("Numero de operacoes: %s" % (self.operations))
            print("No atual: " + str(current_node))
            print("Vizinhos atuais: " + str(self.get_neighbors(current_node)))
            print("Nos ja explorados: " + str(visited))
            print("\n-------------\n")

            # Se o nó atual for o nó final, caminho encontrado
            if current_node == self.path_end:       # Operação de comparação
                # Inicializa uma lista para reconstruir o caminho
                reconst_path = []       # Operação de atribuição  

                self.operations += 2
                while current_node is not None:     # Operação de comparação
                    # Adiciona o nó atual ao caminho reconstruído
                    reconst_path.append(current_node)   # Operação de atribuição

                    # Move para o nó pai
                    current_node = parents[current_node]    # Operação de atribuição

                    self.operations += 3
                # Inverte o caminho reconstruído para obtê-lo do início ao fim
                reconst_path.reverse()      # Operação de atribuição

                self.operations += 1

                # Calcula o peso total do caminho
                for i in range(len(reconst_path) - 1):
                    total_weight += self.get_weight(reconst_path[i], reconst_path[i+1])    # Soma o peso das arestas do caminho
                    self.operations += 1


                print('Caminho encontrado: [', end='')
                i = 0
                while i < len(reconst_path) - 1:
                    print(reconst_path[i] + " - ", end='')
                    i += 1
                print(reconst_path[i], end=']   ')
                print('Peso total: {}'.format(total_weight))

                final_time = perf_counter_ns()      # Variável auxiliar para calcular o tempo de execução

                print("--- Tempo total de execucao: %s nanosegundos ---" % (final_time-initial_time))
                print("--- Numero total de iteracoes: %s ---" % (self.iterations))
                print("--- Numero total de operacoes: %s ---" % (self.operations))

                return reconst_path

            # Explora os vizinhos do nó atual
            for neighbor, _ in self.get_neighbors(current_node):
                if neighbor not in visited:
                    # Adiciona o vizinho à fila para exploração posterior
                    queue.append(neighbor)

                    # Define o nó atual como o pai do vizinho
                    parents[neighbor] = current_node
        