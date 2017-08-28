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


location_GB = '/home/dewigould/Documents/PROJECT/GB/page_140123476092919_2017_07_18_11_21_03.gdf'
location_GC = '/home/dewigould/Documents/PROJECT/GC/page_552083274809379_2017_07_18_11_24_00.gdf'
location_TP = '/home/dewigould/Documents/PROJECT/TP/page_46727363062_2017_07_18_11_26_57.gdf'
location_CH = '/home/dewigould/Documents/PROJECT/CH/page_119206691440652_2017_07_18_11_29_59.gdf'
location_TV = '/home/dewigould/Documents/PROJECT/TV/page_141122205916194_2017_07_18_11_31_48.gdf'
location_FM = '/home/dewigould/Documents/PROJECT/FM/page_163350180344489_2017_07_18_11_35_40.gdf'
location_TA = '/home/dewigould/Documents/PROJECT/TA/page_57270980350_2017_07_18_11_36_53.gdf'
location_RR = '/home/dewigould/Documents/PROJECT/RR/page_106182642885533_2017_07_18_11_49_19.gdf'
location_QF = '/home/dewigould/Documents/PROJECT/QF/page_145674882144187_2017_07_18_11_54_22.gdf'

location_DB = '/home/dewigould/Documents/PROJECT/DB/page_65742456210_2017_07_18_14_53_45.gdf'
location_LF = '/home/dewigould/Documents/PROJECT/LF/page_23617180546_2017_07_18_14_55_39.gdf'
#location_CF = '/home/dewigould/Documents/PROJECT/CF/page_165173797505_2017_07_18_14_57_07.gdf'
location_DM = '/home/dewigould/Documents/PROJECT/DM/page_158324834220405_2017_07_18_15_03_36.gdf'
location_SK = '/home/dewigould/Documents/PROJECT/SK/page_110840208962563_2017_07_18_15_05_25.gdf'
location_NT = '/home/dewigould/Documents/PROJECT/NT/page_32431721651_2017_07_18_15_07_17.gdf'

Locations=[(location_GB,"GB"),( location_GC,"GC"),( location_TP,"TP"),(location_CH,"CH"),(location_TV,"TV"),(location_FM,"FM"),(location_TA,"TA"),(location_RR,"RR"),(location_QF,"QF"),(location_DB,"DB"),(location_LF,"LF"),(location_DM,"DM"),(location_SK,"SK"),(location_NT,"NT")]

def combine_graphs_and_project(Locations,top_or_bottom):
	# top_or_bottom, which nodes to project upon "top", "bottom"
	#Locations is list of file locations of netvizz data to combine
	G_raw=[]
	for location in Locations:
		G_raw.append(gdf_to_dff(location[0],netvizz=True,node_attr=True,isolated_nodes=True)[0])
	#add attributes "name" and "type of page (band or venue)"
	counter = 0
	for graph in G_raw:
		nx.set_node_attributes(graph,"Name",Locations[counter][1])
		counter += 1
	#add all individual graphs into one connected graph
	G_complete = nx.Graph()
	for graph in G_raw:
		G_complete = nx.compose(G_complete,graph)
	G_complete_p,top_nodes,bottom_nodes = bipartite_generate(G_complete, Which_nodes = top_or_bottom)
	return G_complete,G_complete_p,top_nodes,bottom_nodes



#produce graph from data above (RAW) ie. unprojected, and PROJECTED graph
G_raw,G_p,top_nodes,bottom_nodes = combine_graphs_and_project(Locations,"top")

#to_gephi(G_p,"glasgow_15")

degree_distribution(G_p,top_nodes,weight=True)
















