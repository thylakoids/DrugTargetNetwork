import nxviz as nv 
import networkx as nx 
import matplotlib.pyplot as plt



G = nx.Graph()
G.add_nodes_from([1,2,3])
G.add_edge(1,2)
G.add_edge(1,3)
G.add_edges_from([(2,3)])
nx.draw(G)

m = nv.MatrixPlot(G)
m.draw()

c = nv.CircosPlot(G,node_size=1,edge_width = 10,node_labels=True)
c.draw()

a = nv.ArcPlot(G)
a.draw()


plt.show()