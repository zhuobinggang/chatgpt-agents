# from game import init_env, update_actor, back


# 1.尝试使用NetworkX建立并显示图
# 2.遍历zork所有的节点以建立图
# 3.将结果存储为networkx的格式

import networkx as nx
G = nx.MultiDiGraph()
G.add_node(81, label = 'north house')
G.add_node(180, label = 'west house')
G.add_edge(81, 180, label = 'W')
G.add_edge(180, 81, label = 'N')

# # draw
# import matplotlib.pyplot as plt
# pos = nx.spring_layout(G)
# nx.draw(G, pos, font_weight='bold')
# # labels
# node_labels = nx.get_node_attributes(G,'desc')
# nx.draw_networkx_labels(G, pos, labels = node_labels)
# edge_labels = nx.get_edge_attributes(G,'way')
# nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels)
# plt.savefig('dd.png')

# to dot
DOTFILE = 'dd.dot'
PNGFILE = 'dd.png'
nx.drawing.nx_pydot.write_dot(G, DOTFILE)

# from dot to png by pydot
import pydot
(graph,) = pydot.graph_from_dot_file(DOTFILE)
graph.write_png(PNGFILE)


# import pydot
# graph = pydot.Dot('zork_map', graph_type='digraph')
# # Add nodes
# a = pydot.Node(81, label='north house')
# b = pydot.Node(180, label='west house')
# graph.add_node(a)
# graph.add_node(b)
# graph.add_edge(a, b, label='W')
# graph.add_edge(b, a, label='N')
# graph.write_png(PNGFILE)



