
import community
import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd

def randomcolor():
    colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0,14)]
    return "#"+color


# 根据DFS的社交网络区分，分出了27组
# 默认同一片文章的作者是相互认识的
def DFSAuthorSociety():

    # construct a graph
    G = nx.Graph()

    # get edges
    with open('./graph/edges.txt', 'r') as f:
        list1 = f.readlines()

        for line in list1:
            [source, target] = line.strip('\n').split(' ')
            G.add_edge(int(source), int(target))

    AuthorSocietyCnt = 1
    Society = {}
    LeftNodeNum = len(list(G.nodes))
    while LeftNodeNum > 0:
        res = nx.dfs_successors(G, source=list(G.nodes)[0])
        nodes = [list(G.nodes)[0]]
        for key in res:
            nodes = nodes + res[key]
        LeftNodeNum = LeftNodeNum - len(nodes)
        for node in nodes:
            G.remove_node(node)

        Society[AuthorSocietyCnt] = nodes
        AuthorSocietyCnt = AuthorSocietyCnt + 1
        # print(AuthorSocietyCnt, LeftNodeNum)

    print('----- Society -----')
    print(Society)
    SocietyMap = {}
    for SocietyType in Society.keys():
        nodes = Society[SocietyType]
        for node in nodes:
            SocietyMap[node] = SocietyType

    return SocietyMap



def GetAuthorsId():
    points = pd.read_csv('./graph/points.csv')
    AuthorIdMap = {}
    AuthorIdZipMap = zip(points['Label'].values.tolist(), points['Id'].values.tolist())
    print('----- GetAuthorsId -----')
    for mapitem in AuthorIdZipMap:
        AuthorIdMap[mapitem[0]] = mapitem[1]
    return AuthorIdMap

    # print(points)

def ConStructSocietyFeaturesByDFSAuthorSociety(papers):
    AuthorIdMap = GetAuthorsId()

    SocietyMap = DFSAuthorSociety()


    for paper in papers:
        authors = paper['authors']
        AuthorSocialIds = []
        for author in authors:
            try:
                authorid = SocietyMap[AuthorIdMap[author]]
                AuthorSocialIds.append(authorid)
            except:
                pass
        paper['AuthorSocialIds'] = AuthorSocialIds
        if len(AuthorSocialIds) == 0:
            paper['SocialType'] = -1
        else:
            paper['SocialType'] = AuthorSocialIds[0]
    return papers




def ConstructAuthorSociety():

    # construct a graph
    G = nx.Graph()

    # get edges
    with open('./graph/edges.txt', 'r') as f:
        list1 = f.readlines()

        for line in list1:
            [source, target] = line.strip('\n').split(' ')
            G.add_edge(int(source), int(target))

    print('----- nx.clustering(G) -----')
    # print(nx.clustering(G))

    # first compute the best partition
    partition = community.best_partition(G)

    # drawing
    size = float(len(set(partition.values())))

    pos = nx.spring_layout(G)
    print('------- partition level -------')
    print(set(partition.values()))

    print('number of partitions: ')
    print(len(partition.keys()))

    # 硬编码，已知有11个社交分组
    PartitionersGrouph = {}
    for com in set(partition.values()):
        partitioners = [nodes for nodes in partition.keys() if partition[nodes] == com]
        PartitionersGrouph[com] = partitioners

    return PartitionersGrouph
    # ColorSet = {}
    # count = 0.
    # for com in set(partition.values()) :
    #     count = count + 1.
    #     list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
    #
    #     PointColor = randomcolor()
    #     while PointColor in ColorSet:
    #         PointColor = randomcolor()
    #     ColorSet[PointColor] = True
    #
    #     nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 30 , node_color = PointColor)
    #
    #
    # nx.draw_networkx_edges(G, pos, alpha=0.5)
    #
    # plt.show()

    #


def test():
    # better with karate_graph() as defined in networkx example.
    # erdos renyi don't have true communityFeature structure
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
    # ConstructAuthorSociety()
    DFSAuthorSociety()

# Com is :  0
# ['1', '', '2', '5', '3', '24', '25', '26', '28', '55', '56', '238', '240', '239', '242', '243', '246', '248', '250', '251', '252', '255', '249', '259', '241', '256', '261', '258', '266', '262', '268', '27', '245', '272', '273', '274', '276', '277', '278', '279', '282', '283', '284', '285', '287', '275']
# Com is :  1
# ['9', '10', '11', '14', '15', '8', '12', '7', '66', '67', '68', '70', '71', '72', '69', '74', '75', '76', '78', '80', '81', '83', '79', '84', '85', '86', '88', '89', '91', '92', '93', '94', '95', '96', '98', '97', '99', '100', '90', '102', '103', '73', '104', '110', '113', '77', '118', '116', '120', '114', '126', '128', '13', '131', '106', '119', '138', '141', '144', '148', '150', '153', '154', '107']
# Com is :  2
# ['17', '18', '23', '133', '149', '156', '142', '159', '16', '161', '162', '151', '164', '117', '168', '169', '171', '134', '178', '179', '180', '160', '186', '187', '170', '19', '194', '196', '155', '20', '129', '177', '192', '205', '21', '212', '198', '214', '215', '216', '22', '221', '224', '223', '227', '230', '231', '232', '233', '209', '235', '236']
# Com is :  3
# ['29', '31', '264', '292', '295', '30', '296', '297', '298', '299', '300', '301', '302', '304', '303', '305', '306', '310', '311', '312', '314']
# Com is :  4
# ['33', '308', '318', '32', '319', '320', '322', '323', '324', '326', '321', '327', '328', '331', '333', '334', '335', '337', '338', '34', '339', '341', '346', '347', '348']
# Com is :  5
# ['37', '342', '344', '35', '352', '353', '355', '356', '357', '358', '36', '360', '362', '365', '364', '361', '368', '369', '354', '372', '377']
# Com is :  6
# ['40', '4', '42', '41', '375', '378', '38', '379', '382', '383', '384', '387', '390', '39', '376', '391', '392', '393', '397', '398', '395', '401', '380', '386', '403', '405', '406', '407', '410', '417', '420', '409', '413', '414', '428']
# Com is :  7
# ['46', '48', '51', '52', '451', '45', '452', '453', '454', '456', '457', '458', '459', '461', '460', '462', '464', '466', '467', '469', '47', '470', '472', '473', '474', '475', '477', '476', '478', '479', '480', '482', '485', '486', '484', '488', '487', '49', '491', '489', '496', '497', '50', '501', '503', '504', '506', '510', '514', '509', '519', '520', '521', '522', '523']
# Com is :  8
# ['58', '57', '6', '59', '62', '64', '65']
# Com is :  9
# ['426', '43', '430', '433', '434', '435', '438']
# Com is :  10
# ['443', '44', '446', '447', '448']

























