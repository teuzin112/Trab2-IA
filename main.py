import Graph

def read_file(file_path, is_directed):
    graph = Graph.Graph(is_directed)

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

            i += 1

        while i < len(lines) and lines[i].startswith('h('):
            aux = lines[i][lines[i].find('(') + 1 : lines[i].find(')')]
            aux = aux.split(',')
            vertex_1 = aux[0]
            vertex_2 = aux[1]
            h = int(aux[2])

            graph.add_h(vertex_1, vertex_2, h)

            i += 1
        
    return graph

if __name__ == '__main__':
    entry = -1
    graph_obj = None
    while entry:

        print('-'*50 + ' MENU ' + '-'*50)
        print('[1] Carregar Grafo')
        if graph_obj:
            print('[2] Executar algoritmo DFS com retrocesso')
            print('[3] Executar algoritmo A*')
        print('[0] Fechar programa')
        entry = int(input('>>> '))
        print()

        if entry == 1:
            file_path = input('Entre com o caminho do arquivo\n>>> ')
            print()

            is_directed = input('O grafo é orientado ? [S/N]\n>>> ')
            print()

            if is_directed in ('S', 's', 'sim'):
                is_directed = True
            else:
                is_directed = False
            graph_obj = read_file(file_path, is_directed)
            
        elif entry == 2 and graph_obj:
            graph_obj.dfs()
        
        elif entry == 3 and graph_obj:
            graph_obj.a_star()

