#%%
import networkx as nx
import matplotlib.pyplot as plt

def create_dummy_data():

	dict_author_citer = {'author_1': ['citer_1','citer_2'],
						 'author_2': ['citer_3','citer_4'],
						 'author_3': ['citer_2','citer_3']}
	
	return dict_author_citer

def create_network(dict_author_citer):
	
	authors = list(dict_author_citer)

	flatten = lambda l: [item for sublist in l for item in sublist]
	citers = [dict_author_citer[authors] for authors in dict_author_citer]
	citers = flatten(citers)

	nodes = set(authors +citers)

	edges = []
	for author in dict_author_citer:
		for citer in dict_author_citer[author]:
			edges.append([author,citer])

	G = nx.DiGraph()
	G.add_nodes_from(nodes)
	G.add_edges_from(edges)

	return G


def draw_graph(G):
	
	pos = nx.circular_layout(G)

	# --- PLOTTING ---
	plt.figure()
	plt.subplot(111)
	# draws nodes
	nx.draw(G, pos,node_size=2000, node_color='pink',
			labels={node:node for node in G.nodes()},
			arrowsize=20)

	plt.show()

