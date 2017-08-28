"""
Take node and edge files from gephi to create Graph file

node_file and edge_file are csv files exported from PROJECTED GRAPH on GEPHI

Just now this code only adds two attributes: 
modularity class of nodes
weight of edges
NAME
TYPE OF POST

Dewi Gould
13-7-2017
"""

def csv_to_nx_graph(node_file,edge_file):
	import pandas as pd
	import networkx as nx

	df_nodes = pd.read_csv(node_file)
	df_edges = pd.read_csv(edge_file)

	df_nodes = df_nodes.rename(columns={'9': 'type_post', '0': 'Name'})

	list_nodes = df_nodes["id"].tolist()
	list_mod_class = df_nodes["modularity_class"].tolist()
	list_type_posts = df_nodes["type_post"].tolist()
	list_names = df_nodes["Name"].tolist()

	list_sources = df_edges["Source"].tolist()
	list_targets = df_edges["Target"].tolist()
	list_weights = df_edges["weight"].tolist()

	#keys are node id, values are modularity class
	node_information = {}
	for i in range(len(list_nodes)):
		node_information[list_nodes[i]] = list_mod_class[i]
	#same for names
	node_information_2 = {}
	for i in range(len(list_nodes)):
		node_information_2[list_nodes[i]] = list_names[i]

	#same for type post
	node_information_3 = {}
	for i in range(len(list_nodes)):
		node_information_3[list_nodes[i]] = list_type_posts[i]

	#Keys are edge number, values are source, target and weight
	edge_information = {}
	edges = []
	for i in range(len(list_sources)):
		edges.append((list_sources[i],list_targets[i]))
	for edge in edges:
		edge_information[edge] = list_weights[edges.index(edge)]


	#NOW CREATE NETWORKX GRAPH

	G=nx.Graph()
	G.add_nodes_from(list_nodes)
	G.add_edges_from(edges)

	nx.set_node_attributes(G,"modularity_class",node_information)
	nx.set_node_attributes(G,"type_post",node_information_3)
	nx.set_node_attributes(G,"Name",node_information_2)
	nx.set_edge_attributes(G,"weight",edge_information)

	return G
	





