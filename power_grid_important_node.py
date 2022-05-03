import copy
import numpy as np
from pypower.case39 import case39
import networkx as nx


# 输入为原始状态下的网络图，输出节点收缩后的图的集合
def node_shrink(Graph):  # 节点收缩法
    Graphs = []
    # subGraph = nx.Graph()
    for i in list(Graph.nodes):  # 计算每个节点收缩后的图
        subGraph = nx.Graph()
        neighboor_nodes = [n for n in Graph.neighbors(i)]  # i节点的邻居节点
        Graph_int = copy.deepcopy(Graph)  # 深拷贝Graph
        Graph_int.remove_node(i)  # 删除节点i
        remove_edge = list([list(i) for i in Graph_int.edges])  # 删除节点i后，图中的边
        for j in range(len(remove_edge)):  # 将节点i的邻居节点都改成节点i实现节点收缩
            for k in range(len(neighboor_nodes)):
                if remove_edge[j][0] == neighboor_nodes[k]:
                    remove_edge[j][0] = i
                elif remove_edge[j][1] == neighboor_nodes[k]:
                    remove_edge[j][1] = i
                else:
                    continue
        subGraph.add_edges_from(remove_edge)
        subGraph.name = str(i)  # 给图赋属性，排序用
        Graphs.append(subGraph)

    # 冒泡排序
    for i in range(len(Graphs)):
        # Last i elements are already in place
        for j in range(0, len(Graphs) - i - 1):
            if int(Graphs[j].name) > int(Graphs[j + 1].name):
                Graphs[j], Graphs[j + 1] = Graphs[j + 1], Graphs[j]
    return Graphs  # 返回排序后节点收缩图的集合


def IMCs(graph_int, Graphs):  # 计算重要度
    njd_int = 1 / (len(list(graph_int.nodes)) * nx.average_shortest_path_length(graph_int))  # 原始网络凝聚度
    IMCs = []
    for graph in Graphs:
        njd = 1 / (len(list(graph)) * nx.average_shortest_path_length(graph))
        IMC = 1 - njd_int / njd
        IMCs.append(IMC)
    return IMCs


if __name__ == '__main__':
    # 论文测试算例
    edges = [(1, 3), (2, 3), (3, 4), (4, 5), (4, 7), (5, 6), (6, 7), (7, 8), (8, 9), (8, 10)]
    Graph = nx.Graph()
    for i in range(len(edges)):
        Graph.add_edge(edges[i][0], edges[i][1])
    Graph.add_edges_from(edges)
    shrink_Graphs = node_shrink(Graph)  # 节点收缩后的图
    IMC = IMCs(Graph, shrink_Graphs)  # 节点重要度
    IMC = np.array(IMC)
    IMC = IMC.reshape(IMC.shape[0], 1)
    print(IMCs)
    # zyd_line0 = []
    #
    # x = 0
    # for i in range(len(zyd0)):  # 线性归一化
    #     value = (1 - x) * (
    #             (zyd0[i] - min(zyd0)) / (max(zyd0) - min(zyd0))) + x
    #     zyd_line0.append(value)
    # zyd_line0 = np.array(zyd_line0)

    # case = case39()
    # branch = case["branch"]
    # branch_X = []

    # edges = []
    # for i in range(len(branch)):
    #     edges.append((int(branch[i][0]), int(branch[i][1])))
    #     branch_X.append(branch[i][3])
    # test_Graph = nx.Graph()
    # for i in range(len(edges)):
    #     test_Graph.add_edge(edges[i][0], edges[i][1], weight=branch_X[i])
    # test_Graph.add_edges_from(edges)
    # njds = node_shrink(test_Graph)
    # zyd = njd(test_Graph, njds)
    # zyd_line = []
    #
    # x = 0
    # for i in range(len(zyd)):
    #     value = (1 - x) * (
    #             (zyd[i] - min(zyd)) / (max(zyd) - min(zyd))) + x
    #     zyd_line.append(value)
    # zyd_line = np.array(zyd_line)

    # case = CaseDataHN500.TestCase()
    # branch1 = case["branch"]
    # branch_X1 = []
    #
    # edges1 = []
    # for i in range(len(branch1)):
    #     edges1.append((int(branch1[i][0]), int(branch1[i][1])))
    #     branch_X1.append(branch1[i][3])
    # test_Graph1 = nx.Graph()
    # for i in range(len(edges1)):
    #     test_Graph1.add_edge(edges1[i][0], edges1[i][1], weight=branch_X1[i])
    # test_Graph1.add_edges_from(edges1)
    # # test_Graph.add_edges_from()
    # njds1 = node_shrink(test_Graph1)
    # zyd1 = njd(test_Graph1, njds1)
    # zyd_line1 = []
    #
    # x = 0
    # for i in range(len(zyd1)):
    #     value = (1 - x) * (
    #             (zyd1[i] - min(zyd1)) / (max(zyd1) - min(zyd1))) + x
    #     zyd_line1.append(value)
    # zyd_line1 = np.array(zyd_line1)
