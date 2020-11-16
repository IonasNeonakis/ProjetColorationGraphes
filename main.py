RES_DIR = "res/"
AVAILABLE_COLORS = set(['blue', 'red', 'green', 'white', 'black'])

def clean_string(s):
    return s.strip().replace('\n', '')

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
        for c in splitted[1].strip():
            if(c.isalnum()):
                edges.append(c)
        graph[vertex] = edges

    f.close()

    if graphLength != len(graph):
        raise BaseException('La taille entrée en début de fichier ne correspond pas au graphe donné.')

    return graph

def degree(graph, vertex):
    return len(graph[vertex])

def neighbourhood_colors(neighbours, coloring):
    used_colors = set()
   
    for v in neighbours:
       used_colors.add(coloring[v])

    return used_colors

# Initie la couleur de chaque sommet à une couleur au 'hasard'
def init_colors(graph):
    coloring = {}
    for v in graph.keys():
        coloring[v] = next(iter(AVAILABLE_COLORS))
    return coloring

def coloring_rec(graph, coloring):

    if graph:
        for vertex in graph:
            if degree(graph, vertex) <= 5:
                x = vertex
                break

        deg_x = degree(graph, x)
        neighbours = graph.pop(x, None)
        coloring_res = coloring_rec(graph, coloring)

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
                coloring[x] = next(iter(remaining_colors))
            else:
                # On applique la brique 6
                alpha   = coloring[graph[x][0]]
                beta    = coloring[graph[x][1]]
                gamma   = coloring[graph[x][2]]
                delta   = coloring[graph[x][3]]
                epsilon = coloring[graph[x][4]]

                return coloring


    return coloring


def check_coloring(graph, coloring):
    for v,e in graph.items():
        self_color = coloring[v]
        for v1 in e:
            if coloring[v1] == self_color:
                return False
    return True

def main():
    graph = parse_graph('JoliGraphe10.graphe')
    print(coloring_rec(graph, init_colors(graph)))
    print(check_coloring(graph, coloring_rec(graph, init_colors(graph))))


if __name__ == "__main__":
    main()