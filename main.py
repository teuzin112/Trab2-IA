import Graph

# Função auxiliar para ler um arquivo texto e inicializar o grafo corretamente
def read_file(file_path):
    graph = Graph.Graph()

    with open(file_path, 'r') as file:
        lines = file.readlines()

        if len(lines) < 2:
            print('Invalid file')
            return

        graph.path_start = lines[0][lines[0].find('(') + 1 : lines[0].find(')')]
        graph.path_end = lines[1][lines[1].find('(') + 1 : lines[1].find(')')]

        i = 2
        while 'pode_ir' in lines[i]:
            aux = lines[i][lines[i].find('(') + 1 : lines[i].find(')')]
            aux = aux.split(',')
            vertex_1 = aux[0]
            vertex_2 = aux[1]
            weight = int(aux[2])

            graph.add_edge(vertex_1, vertex_2, weight)
            graph.add_edge(vertex_2, vertex_1, weight)

            i += 1

        # Ordena a lista de adjacencia depois que todas as arestas foram inseridas
        for vertex, neighbours in graph.adjacency_list.items():
            graph.adjacency_list[vertex] = sorted(neighbours, key=lambda x: x[0])

        while i < len(lines) and lines[i].startswith('h('):
            aux = lines[i][lines[i].find('(') + 1 : lines[i].find(')')]
            aux = aux.split(',')
            vertex_1 = aux[0]
            vertex_2 = aux[1]
            h = int(aux[2])

            if vertex_1 == graph.path_end:
                graph.add_h(vertex_2, h)
            if vertex_2 == graph.path_end:
                graph.add_h(vertex_1, h)
            
            graph.add_h(graph.path_end, 0)

            i += 1
        
    return graph

if __name__ == '__main__':
    entry = -1
    graph_obj = None
    while entry:

        print('-'*50 + ' MENU ' + '-'*50)
        print('[1] Carregar Grafo')
        if graph_obj:
            print('[2] Executar algoritmo DFS')
            print('[3] Executar algoritmo A*')
            print('[4] Executar algoritmo BFS')
        print('[0] Fechar programa')
        entry = int(input('>>> '))
        print()

        if entry == 1:
            graph_obj = None
            file_path = input('Entre com o caminho do arquivo\n>>> ')
            print()

            graph_obj = read_file(file_path)
            
        elif entry == 2 and graph_obj:
            graph_obj.dfs()
            
        elif entry == 3 and graph_obj:
            graph_obj.a_star()
        
        elif entry == 4 and graph_obj:
            graph_obj.bfs()
