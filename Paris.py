from gdf_to_dff_new_new import gdf_to_dff
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
from collections import Counter
from itertools import islice
import numpy as np
import powerlaw
from operator import itemgetter


from Cartography import list_of_modules, within_mod_deg_vs_part_coeff
from proj_and_comm import bipartite_generate, to_gephi, edge_weight_distribution, degree_distribution
from Gephi_tables import csv_to_nx_graph


location_LP = '/home/dewigould/Documents/PROJECT/Paris/LP/page_308379402539315_2017_07_26_10_55_35.gdf'
location_DJ = '/home/dewigould/Documents/PROJECT/Paris/DJ/page_229070590543503_2017_07_26_10_59_11.gdf'
location_LO = '/home/dewigould/Documents/PROJECT/Paris/LO/page_389137947828306_2017_07_26_11_05_56.gdf'
location_AK = '/home/dewigould/Documents/PROJECT/Paris/AK/page_344785365587962_2017_07_26_11_08_55.gdf'
location_DM = '/home/dewigould/Documents/PROJECT/Paris/DM/page_589526841202283_2017_07_26_11_12_24.gdf'
location_LA = '/home/dewigould/Documents/PROJECT/Paris/LA/page_1793523060930716_2017_07_26_11_16_11.gdf'
location_EL = '/home/dewigould/Documents/PROJECT/Paris/EL/page_47694533087_2017_07_26_11_17_59.gdf'
location_NS = '/home/dewigould/Documents/PROJECT/Paris/NS/page_402902943208746_2017_07_26_11_19_21.gdf'
location_SI = '/home/dewigould/Documents/PROJECT/Paris/SI/page_142936679210390_2017_07_26_11_28_35.gdf'
location_BA = '/home/dewigould/Documents/PROJECT/Paris/BA/page_322660004588402_2017_07_26_11_30_51.gdf'

Locations=[(location_LP, "Lomepal"),(location_DJ, "Dadju"),(location_LO,"Louane"),(location_AK,"Ash Kidd"),(location_DM,"Dehmo"),(location_LA,"Leah Paci"), (location_EL,"Elephanz"),(location_NS,"Niska"),(location_SI,"Siboy"),(location_BA,"Basada")]

def combine_graphs_and_project(Locations,top_or_bottom):
	# top_or_bottom, which nodes to project upon "top", "bottom"
	#Locations is list of file locations of netvizz data to combine
	G_raw=[]
	for location in Locations:
		G_raw.append(gdf_to_dff(location[0],netvizz=True,node_attr=True,isolated_nodes=True)[0])
		print "done_1"
	#add attributes "name" and "type of page (band or venue)"
	counter = 0
	for graph in G_raw:
		nx.set_node_attributes(graph,"Name",Locations[counter][1])
		counter += 1
		print counter
	#add all individual graphs into one connected graph
	G_complete = nx.Graph()
	for graph in G_raw:
		G_complete = nx.compose(G_complete,graph)
		print "done_2"
	G_complete_p,top_nodes,bottom_nodes = bipartite_generate(G_complete, Which_nodes = top_or_bottom)
	return G_complete,G_complete_p,top_nodes,bottom_nodes



#produce graph from data above (RAW) ie. unprojected, and PROJECTED graph
G_raw,G_p,top_nodes,bottom_nodes = combine_graphs_and_project(Locations,"top")
print "first bit done"
to_gephi(G_p,"PAR_10")
print "done"

"""
node_file ='
edge_file ='
G_gephi_par = csv_to_nx_graph(node_file,edge_file)
to_gephi(G_gephi_par,'par_with_mod')
"""

#degree_distribution(G_p,top_nodes,weight=True)












