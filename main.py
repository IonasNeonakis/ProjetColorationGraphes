from collections import deque

RES_DIR = "res/"
OUT_DIR = "out/"
AVAILABLE_COLORS = {'blue', 'red', 'green', 'white', 'black'}


# Supprime les espaces inutiles et les sauts de ligne
def clean_string(s):
    return s.strip().replace('\n', '')


# Retourne un graphe à partir d'un fichier .graphe qui se trouve dans RES_DIR
def parse_graph(filename):
    graph = {}
    graphLength = -1
    f = open(RES_DIR + filename, 'r')
    lines = f.readlines()

    if clean_string(lines[0]).isdigit():
        graphLength = int(clean_string(lines[0]))
    else:
        raise BaseException('Le fichier doit commencer par la longueur du graphe.')

    for i in range(1, len(lines)):
        splitted = clean_string(lines[i]).split(':')
        vertex = splitted[0]
        edges = []
        for s in splitted[1].strip()[1:-1].split(','):
            if s.strip().isalnum():
                edges.append(s.strip())
        graph[vertex] = edges

    f.close()

    if graphLength != len(graph):
        raise BaseException('La taille entrée en début de fichier ne correspond pas au graphe donné.')

    return graph


# Calcule le degré d'un sommet vertex dans un graphe
def degree(graph, vertex):
    return len(graph[vertex])


# Retourne les couleurs de tous les sommets neighbours
def neighbourhood_colors(neighbours, coloring):
    used_colors = set()

    for v in neighbours:
        used_colors.add(coloring[v])

    return used_colors


# Supprime un sommet d'un graphe en se supprimant des liste d'adjacence des autres sommets
def remove_vertex(graph, vertex):
    for v in graph:
        if vertex in graph[v]:
            graph[v].remove(vertex)

    return graph.pop(vertex)


# Initie la couleur de chaque sommet à une couleur au 'hasard'. Chaque sommet aura la même couleur
def init_colors(graph):
    coloring = {}
    for v in graph.keys():
        coloring[v] = next(iter(AVAILABLE_COLORS))
    return coloring


# Trouve un chemin d'un graphe, à partir de starting_vertex jusqu'à vertex_to_find
def get_path(graph, starting_vertex, vertex_to_find):
    visited = []
    queue = deque()
    queue.append(starting_vertex)

    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            if vertex == vertex_to_find:
                return True
            else:
                visited.append(vertex)
                unvisited = [v1 for v1 in graph[vertex] if v1 not in visited]
                queue.extend(unvisited)

    return False


# Parcours en profondeur à partir de starting_vertex
def breadth_first_search(graph, starting_vertex):
    visited = []
    queue = deque()
    queue.append(starting_vertex)

    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.append(vertex)
            unvisited = [v1 for v1 in graph[vertex] if v1 not in visited]
            queue.extend(unvisited)

    return visited


# Inverse les couleurs a et b d'un graphe. Coloring est les couleurs acctuelle du graphe
def inverse_color(graph, coloring, color_a, color_b):
    for vertex in graph:
        if coloring[vertex] == color_a:
            coloring[vertex] = color_b
        else:
            coloring[vertex] = color_a
    return coloring


# Retourne une 5 coloration d'un graphe
def coloring_rec(graph, coloring):
    if graph:
        for vertex in graph:
            if degree(graph, vertex) <= 5:
                x = vertex  # on trouve un sommet de degré <= 5
                break

        deg_x = degree(graph, x)
        neighbours = remove_vertex(graph, x)  # on supprime le sommet x et récupère son sommet
        coloring_res = coloring_rec(graph, coloring)  # appel récursif

        if deg_x < 5:
            # On applique la brique 4
            if coloring_res:
                # On aura au minimum une couleur dans l'ensemble remaining_colors car il y a 5 couleurs et x a 4 voisins.
                remaining_colors = AVAILABLE_COLORS - neighbourhood_colors(neighbours, coloring_res)
                coloring[x] = next(iter(remaining_colors))
        elif deg_x == 5:
            # On applique la brique 5 ou la brique 6
            used_colors = neighbourhood_colors(neighbours, coloring_res)
            # On a seulement 5 couleurs différentes, donc si le nombre de couleur utilisées n'est pas < à 5, il est forcément égal.
            if len(used_colors) < 5:
                # On applique la brique 5
                remaining_colors = AVAILABLE_COLORS - neighbourhood_colors(neighbours, coloring_res)
                coloring[x] = next(iter(remaining_colors))  # x prend la première couleur disponible
            else:
                # On applique la brique 6
                a = neighbours[0]
                b = neighbours[1]
                c = neighbours[2]
                d = neighbours[3]
                e = neighbours[4]

                alpha = coloring[a]
                beta = coloring[b]
                gamma = coloring[c]
                delta = coloring[d]
                epsilon = coloring[e]

                induced_subgraph_ag = {}  # graphe induit de alpha gamma
                induced_subgraph_bd = {}  # graphe induit de beta delta

                for k, v in graph.items():  # on trouves les deux graphes induits
                    if coloring_res[k] == alpha or coloring_res[k] == gamma:
                        induced_subgraph_ag[k] = v
                    if coloring_res[k] == beta or coloring_res[k] == delta:
                        induced_subgraph_bd[k] = v

                if get_path(induced_subgraph_ag, a, c):  # s'il y a un chemin de a vers c
                    connected_component = breadth_first_search(induced_subgraph_bd,
                                                               b)  # on prend la composante connexe G'(beta, delta) qui contient b
                    new_coloring = inverse_color(connected_component, coloring_res, beta,
                                                 delta)  # on inverse les couleurs de G'(beta, delta)
                else:  # S'il y a un chemin de b à d ou qu'il n'y a pas de chemin de a à c et de b à d
                    connected_component = breadth_first_search(induced_subgraph_ag,
                                                               a)  # on prend la composante connexe G'(alpha, gamma) qui contient a
                    new_coloring = inverse_color(connected_component, coloring_res, alpha,
                                                 gamma)  # on inverse les couleurs de G'(alpha, gamma)

                remaining_colors = AVAILABLE_COLORS - neighbourhood_colors(neighbours,
                                                                           new_coloring)  # on récupère la couleur restante
                coloring[x] = next(iter(remaining_colors))  # on la donne à x

    return coloring


# Vérifie que la coloration d'un graphe est correcte
def check_coloring(graph, coloring):
    for v, e in graph.items():
        self_color = coloring[v]
        for v1 in e:
            if coloring[v1] == self_color:
                return False
    return True


# méthode qui prend une coloration d'un graphe et qui l'écrit dans un fichier .colors dans OUT_DIR
def write_file(file_name, colors):
    f = open(OUT_DIR + file_name + '.colors', 'w+')
    f.write(str(len(colors)) + '\n')
    for k, v in colors.items():
        f.write(k + ': ' + v + '\n')
    f.close()


def main():
    graph = parse_graph('JoliGraphe100.graphe')
    colors = coloring_rec(graph, init_colors(graph))

    if check_coloring(graph, colors):
        write_file('JoliGraphe100', colors)
        print('Voici la coloration trouvée : \n\n', colors)
    else:
        print('Pas de coloration trouvée !')


if __name__ == "__main__":
    main()
