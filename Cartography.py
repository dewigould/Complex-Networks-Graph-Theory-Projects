"""
Generate Plots of within module degree vs participation coefficient
G is graph object of Networkx
feature is the name of the Networkx attribute that defines the modules

Dewi Gould
13-7-2017
"""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def list_of_modules(G,feature):
#feature is what you are basing the modules on. eg: "Name", "Modularity"
	list_modules =[]
	name = nx.get_node_attributes(G,feature)
	for nodes in G.nodes():
		if name[nodes] not in list_modules:
			list_modules.append(name[nodes])
	return list_modules, feature
	

def within_mod_deg_vs_part_coeff(G,names_modules,feature):

	#number of nodes in each module
	number_in_modules = {}
	#Keys are nodes, values are number of links to nodes in same module
	nodes_and_links_inmod ={}
	#Keys are nodes, value are links to each module (list)
	nodes_and_links_allmods ={}
	#Keys are nodes, values are number of links to all other nodes
	nodes_and_links_total = {}
	#Keys are nodes, values are sum of weights to nodes within same module above
	nodes_and_weighted_inmod ={}
	#Keys are nodes, values are sum of weights to nodes in each module (list entry for each module)
	nodes_and_weighted_allmods={}
	#Keys are nodes, values are sum total sum of weights to all other nodes
	nodes_and_weighted_total={}

	name = nx.get_node_attributes(G, feature)
	#GET DATA

	for names in names_modules:
		number_in_modules[names] = 0
	for sources in G.nodes():
		nodes_and_links_allmods[sources] = [0]*len(names_modules)
		nodes_and_links_inmod[sources] = 0
		nodes_and_links_total[sources] = 0
		nodes_and_weighted_inmod[sources]=0
		nodes_and_weighted_allmods[sources]=[0]*len(names_modules)
		nodes_and_weighted_total[sources]=0

		if name[sources] in names_modules == True :
			number_in_modules[name[sources]] +=1
		for targets in G.nodes():
			nodes_and_links_total[sources] += G.number_of_edges(sources,targets)
			if G.has_edge(sources,targets) == True:
				nodes_and_weighted_total[sources] += G[sources][targets]["weight"]
				nodes_and_weighted_allmods[sources][names_modules.index(name[targets])] += G[sources][targets]["weight"]
			if name[sources] == name[targets]:
				nodes_and_links_inmod[sources] += G.number_of_edges(sources,targets)
				if G.has_edge(sources,targets) == True:
					nodes_and_weighted_inmod[sources] += G[sources][targets]["weight"]

			nodes_and_links_allmods[sources][names_modules.index(name[targets])] += G.number_of_edges(sources,targets)






	#print "Number of nodes in each module", number_in_modules
	#print "Nodes and total number of links to all other nodes within same module", nodes_and_links_inmod
	#print "Nodes and number of links to all nodes within each module", nodes_and_links_allmods
	#print "Nodes and total number of links to all other nodes", nodes_and_links_total
	#print "Combined weights of all links to all other nodes in same module", nodes_and_weighted_inmod
	#print "Combined weights of all links to all nodes in each individual module", nodes_and_weighted_allmods
	#print "Combined weights of all links to all other nodes", nodes_and_weighted_total			
	
	nodes_R1 = []
	nodes_R2 = []
	nodes_R3 = []
	nodes_R4 = []
	nodes_R5 = []
	nodes_R6 = []
	nodes_R7 = []
	nodes_R1l = []
	nodes_R2l = []
	nodes_R3l = []
	nodes_R4l = []
	nodes_R5l = []
	nodes_R6l = []
	nodes_R7l = []

	#GET WITHIN MODULE DEGREE AND PARTICIPATION COEFFICIENT
	within_module_degree_links={}
	within_module_degree_weights={}
	participation_coefficient_links={}
	participation_coefficient_weights={}
	for nodes in G.nodes():
		within_module_degree_links[nodes]=0
		within_module_degree_weights[nodes]=0
		participation_coefficient_links[nodes]=0
		participation_coefficient_weights[nodes]=0

		name = nx.get_node_attributes(G,feature)

		total_links_inmod=[]
		total_weights_inmod=[]

		total_links = nodes_and_links_total[nodes]
		total_weights = nodes_and_weighted_total[nodes]

		for other_nodes in G.nodes():
			if name[nodes] == name[other_nodes]:
				total_links_inmod.append(nodes_and_links_inmod[other_nodes])
				total_weights_inmod.append(nodes_and_weighted_inmod[other_nodes])
		#the within module degree z-score measures how 'well connected' a node is to other nodes in the module


		#WHAT TO DO IF STANDARD DEVIATION IS 0
		if np.std(total_links_inmod) == 0:
			err_a = 1
		else:
			err_a = np.std(total_links_inmod)	

		if np.std(total_weights_inmod) == 0:
			err_b = 1
		else: 
			err_b = np.std(total_weights_inmod)	
		z_links =  abs((nodes_and_links_inmod[nodes] - np.mean(total_links_inmod))/err_a)
		z_weights = abs((nodes_and_weighted_inmod[nodes] - np.mean(total_weights_inmod))/err_b)

		within_module_degree_links[nodes] += z_links
		within_module_degree_weights[nodes] += z_weights
		
		links_squared = [i**2 for i in nodes_and_links_allmods[nodes]]
		weights_squared = [i**2 for i in nodes_and_weighted_allmods[nodes]]

		P_i_links = 1 - (sum(links_squared)/((float(total_links))**2))

		#FOR WEIGHTED, GET RID OF THE 1-??? SO VERY MODULAR NODES HAVE VALUE TENDING TO 0 AS EXPECTED

		P_i_weights =1 - (sum(weights_squared)/(total_weights**2))
					

		#The participation coefficient of a node is therefore close to one if its links are
		#uniformly distributed among all the modules and zero if all its links are within its own
		#module.

		participation_coefficient_links[nodes] += P_i_links
		participation_coefficient_weights[nodes] += P_i_weights


		if z_weights <2.5:	
			if nodes_and_weighted_allmods[nodes][names_modules.index(name[nodes])] == nodes_and_weighted_total[nodes]:
				nodes_R1.append(nodes)
			elif nodes_and_weighted_allmods[nodes][names_modules.index(name[nodes])] >= 0.6*nodes_and_weighted_total[nodes]:
				nodes_R2.append(nodes)
			if nodes_and_weighted_allmods[nodes][names_modules.index(name[nodes])] < 0.6*nodes_and_weighted_total[nodes]:
				if nodes_and_weighted_allmods[nodes][names_modules.index(name[nodes])] >= 0.35*nodes_and_weighted_total[nodes]:
					nodes_R3.append(nodes)
			if nodes_and_weighted_allmods[nodes][names_modules.index(name[nodes])] <0.35*nodes_and_weighted_total[nodes]:
				nodes_R4.append(nodes)
		if z_weights >=2.5:
			if nodes_and_weighted_allmods[nodes][names_modules.index(name[nodes])] >= 0.6*nodes_and_weighted_total[nodes]:
				nodes_R5.append(nodes)
			if nodes_and_weighted_allmods[nodes][names_modules.index(name[nodes])] >= 0.5*nodes_and_weighted_total[nodes]:
				nodes_R6.append(nodes)
			if nodes_and_weighted_allmods[nodes][names_modules.index(name[nodes])] < 0.5*nodes_and_weighted_total[nodes]:
				nodes_R7.append(nodes)
				
		if z_links <2.5:	
			if nodes_and_links_allmods[nodes][names_modules.index(name[nodes])] >= nodes_and_links_total[nodes]:
				nodes_R1l.append(nodes)
			elif nodes_and_links_allmods[nodes][names_modules.index(name[nodes])] >= 0.6*nodes_and_links_total[nodes]:
				nodes_R2l.append(nodes)
			if nodes_and_links_allmods[nodes][names_modules.index(name[nodes])] < 0.6*nodes_and_links_total[nodes]:
				if nodes_and_links_allmods[nodes][names_modules.index(name[nodes])] >= 0.35*nodes_and_links_total[nodes]:
					nodes_R3l.append(nodes)
			if nodes_and_links_allmods[nodes][names_modules.index(name[nodes])] <0.35*nodes_and_links_total[nodes]:
				nodes_R4l.append(nodes)
		if z_links >=2.5:
			if nodes_and_links_allmods[nodes][names_modules.index(name[nodes])] >= 0.6*nodes_and_links_total[nodes]:
				nodes_R5l.append(nodes)
			if nodes_and_links_allmods[nodes][names_modules.index(name[nodes])] >= 0.5*nodes_and_links_total[nodes]:
				nodes_R6l.append(nodes)
			if nodes_and_links_allmods[nodes][names_modules.index(name[nodes])] < 0.5*nodes_and_links_total[nodes]:
				nodes_R7l.append(nodes)
			
		regions_links = [nodes_R1l, nodes_R2l, nodes_R3l, nodes_R4l, nodes_R5l, nodes_R6l, nodes_R7l]
		regions_weights = [nodes_R1, nodes_R2, nodes_R3, nodes_R4, nodes_R5, nodes_R6, nodes_R7]

		








	#print "Within Module Degree", within_module_degree_links
	#print "Within Module Degree, weighted", within_module_degree_weights

	#print "Participation Coefficient", participation_coefficient_links
	#print "Weighted Participation Coefficient", participation_coefficient_weights
	

#Normalise the participation coefficients so that they sum to 1, just for ease of visualization
	#participation_coefficient_weights_norm = [i/sum(participation_coefficient_weights.values()) for i in participation_coefficient_weights.values()]

	return within_module_degree_links, within_module_degree_weights, participation_coefficient_links,participation_coefficient_weights,regions_links,regions_weights

