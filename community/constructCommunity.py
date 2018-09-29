
import community
import networkx as nx
import matplotlib.pyplot as plt
import random

def randomcolor():
    colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0,14)]
    return "#"+color


# 先构建一个邻接矩阵吧
# 以后再实现
def DFSAuthorSociety():

    # construct a graph
    G = nx.Graph()

    # get edges
    with open('../graph/edges.txt', 'r') as f:
        list1 = f.readlines()

        for line in list1:
            [source, target] = line.split(' ')
            G.add_edge(source, target)

    pass


def ConstructAuthorSociety():

    # construct a graph
    G = nx.Graph()

    # get edges
    with open('../graph/edges.txt', 'r') as f:
        list1 = f.readlines()

        for line in list1:
            [source, target] = (line[:-2]).split(' ')
            G.add_edge(source, target)

    print('----- nx.clustering(G) -----')
    # print(nx.clustering(G))

    # first compute the best partition
    partition = community.best_partition(G)

    # drawing
    size = float(len(set(partition.values())))

    pos = nx.spring_layout(G)
    print('------- partition level -------')
    print(set(partition.values()))

    print('number of partition members: ')

    ColorSet = {}
    count = 0.
    for com in set(partition.values()) :
        count = count + 1.
        list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]

        # 每次画20个？
        PointColor = randomcolor()
        while PointColor in ColorSet:
            PointColor = randomcolor()
        ColorSet[PointColor] = True

        nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 30 , node_color = PointColor)


    nx.draw_networkx_edges(G, pos, alpha=0.5)

    plt.show()

    #


def test():
    # better with karate_graph() as defined in networkx example.
    # erdos renyi don't have true community structure
    G = nx.erdos_renyi_graph(30, 0.05)

    # first compute the best partition
    partition = community.best_partition(G)

    # drawing
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(G)
    count = 0.
    for com in set(partition.values()) :
        count = count + 1.
        list_nodes = [nodes for nodes in partition.keys()
                                    if partition[nodes] == com]
        nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20, node_color = str(count / size))


    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.show()


if __name__ == "__main__":
    ConstructAuthorSociety()

























