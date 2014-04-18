import sys
import whrandom as rand

def readGraph(cur, text):
    n = int(text[cur].strip())
    g = []
    cur += 1

    for i in range(cur, cur+n):
        g.append(map(int, text[i].strip().split(' ')))

    return i+1, g

def parse_input_file(filename):
    f = open(filename, "r")
    file_txt = f.readlines()
    f.close()
    len_file_txt = len(file_txt)
    cur = 0

    # Parse G1 and G2
    cur, g1 = readGraph(cur, file_txt)
    cur, g2 = readGraph(cur, file_txt)

    # Parse the subgraph inducer
    edges_to_delete = [map(int, edge.split(',')) for edge in file_txt[cur].strip().split(' ')[1: ]]
    vertices_to_delete = map(int, file_txt[cur+1].strip().split(' ')[1: ])
    cur += 2

    # Parse the isomorphism
    pi_original = {}
    range_list = file_txt[cur].strip().split(' ')
    for i in range(len(range_list)):
        pi_original[i] = int(range_list[i])

    return g1, g2, {"ER": edges_to_delete, "VD": vertices_to_delete}, pi_original

def get_random_isomorphism(n):
    s = range(n)
    isomorphism = {}
    for i in range(n):
        element = rand.choice(s)
        isomorphism[i] = element
        s.remove(element)

    return isomorphism

def get_isomorphic_graph(g, iso):
    n = len(g)
    gP = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            gP[iso[i]][iso[j]] = g[i][j]
    return gP

def apply_iso_on_subgph_indc(si, iso):
    return {
        "VD": [iso[vertex] for vertex in si["VD"]],
        "ER": [[iso[edge[0]], iso[edge[1]]] for edge in si["ER"]]
    }

def get_subgraph(si, g):
    er = si["ER"]
    for edge in er:
        g[edge[0]][edge[1]] = g[edge[1]][edge[0]] = 0

    si["VD"].sort(reverse=True)
    for vertex in si["VD"]:
        g.pop(vertex)
        for elements in g:
            elements.pop(vertex)

    return g

def get_iso_and_iso_subgraph(g1, g2, si, pi_original, alpha, q):
    qP = get_subgraph(apply_iso_on_subgph_indc(si, alpha), q)

    range_list = []
    for i in range(len(g1)):
        range_list.append(alpha[pi_original[i]])

    pi = {} 
    range_list_sorted = sorted(range_list)
    for i in range(len(range_list)):
        pi[i] = range_list_sorted.index(range_list[i])

    return pi, qP

def get_boolean_matrix(g, si):
    n = len(g)
    bool_matrix = [[True] * n for i in range(n)]
    for edge in si["ER"]:
        bool_matrix[edge[0]][edge[1]] = False
    for vertex in si["VD"]:
        for i in range(n):
           bool_matrix[vertex][i] = False
           bool_matrix[i][vertex] = False

def main():
    g1, g2, subgraphInducer, pi_original = parse_input_file("input1.txt") # change to sys.argv[1]

    while True:
        alpha = get_random_isomorphism(len(g2))
    
        q = get_isomorphic_graph(g2, alpha)
        # @rbhatia COMMIT TO 'q' and print commitment

        coin_toss = raw_input("Say H(ead)/T(tail)/Q(uit): ").strip()[0].lower()
        if coin_toss == 'q':
            break
        elif coin_toss == 'h':
            pass
            # @rbhatia (1) print alpha (2) Open the commitment to 'q' (3) Print "passed" iff get_isomorphic_graph(g2, alpha) == q
        else:
            pi, qP = get_iso_and_iso_subgraph(g1, g2, subgraphInducer, pi_original, alpha, q)
            subgraph_bool_matrix = get_boolean_matrix(g2, subgraphInducer)
            # @rbhatia (1) reveal only part of subgraph_bool_matrix part of Q and reveal pi (2) print "passed" iff get_isomorphic_graph(g1, pi) == qP
    
if __name__ == "__main__":
    main()
