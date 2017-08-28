from gdf_to_dff_new_new import gdf_to_dff
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
from collections import Counter
from itertools import islice
import numpy as np
import powerlaw
from operator import itemgetter
from matplotlib import colors as mcolors
import matplotlib.patches as mpatches




from Cartography import list_of_modules, within_mod_deg_vs_part_coeff
from proj_and_comm import bipartite_generate, to_gephi, edge_weight_distribution, degree_distribution, edge_weight_fit
from Gephi_tables import csv_to_nx_graph



location_TX = '/home/dewigould/Documents/PROJECT/Barcelona/TX/page_157248094325296_2017_07_18_12_45_57.gdf'
location_EL = '/home/dewigould/Documents/PROJECT/Barcelona/EL/page_35735977639_2017_07_18_12_48_07.gdf'
location_BL = '/home/dewigould/Documents/PROJECT/Barcelona/BL/page_242544625792496_2017_07_18_12_49_29.gdf'
location_DP = '/home/dewigould/Documents/PROJECT/Barcelona/DP/page_503830016413462_2017_07_18_12_51_06.gdf'
location_SC = '/home/dewigould/Documents/PROJECT/Barcelona/SC/page_664746190296435_2017_07_18_12_52_46.gdf'
location_EC = '/home/dewigould/Documents/PROJECT/Barcelona/EC/page_179505822093231_2017_07_18_12_53_55.gdf'
location_GO = '/home/dewigould/Documents/PROJECT/Barcelona/GO/page_121869801164675_2017_07_18_12_56_45.gdf'
location_BH = '/home/dewigould/Documents/PROJECT/Barcelona/BH/page_313041785419_2017_07_18_12_58_06.gdf'
location_ML = '/home/dewigould/Documents/PROJECT/Barcelona/ML/page_188755654492247_2017_07_18_13_00_01.gdf'

location_JD = '/home/dewigould/Documents/PROJECT/Barcelona/JD/page_179452158747555_2017_07_18_15_12_21.gdf'
location_LB = '/home/dewigould/Documents/PROJECT/Barcelona/LB/page_34303573494_2017_07_18_15_13_52.gdf'
location_IB = '/home/dewigould/Documents/PROJECT/Barcelona/IB/page_44496660777_2017_07_18_15_15_24.gdf'
location_AF = '/home/dewigould/Documents/PROJECT/Barcelona/AF/page_17566589298_2017_07_18_15_17_57.gdf'
location_LI = '/home/dewigould/Documents/PROJECT/Barcelona/LI/page_133700129986545_2017_07_18_15_19_39.gdf'
location_EP = '/home/dewigould/Documents/PROJECT/Barcelona/EP/page_109565682400416_2017_07_18_15_21_01.gdf'

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
location_DM = '/home/dewigould/Documents/PROJECT/DM/page_158324834220405_2017_07_18_15_03_36.gdf'
location_SK = '/home/dewigould/Documents/PROJECT/SK/page_110840208962563_2017_07_18_15_05_25.gdf'
location_NT = '/home/dewigould/Documents/PROJECT/NT/page_32431721651_2017_07_18_15_07_17.gdf'




Locations = [(location_TX,"TX"),(location_EL,"EL"),(location_BL,"BL"),(location_DP,"DP"),(location_SC,"SC"),(location_EC,"EC"),(location_GO,"GO"),(location_BH,"BH"),(location_ML,"ML"),(location_JD,"JD"),(location_LB,"LB"),(location_IB,"IB"),(location_AF,"AF"),(location_LI,"LI"),(location_EP,"EP"),(location_GB,"GB"),( location_GC,"GC"),( location_TP,"TP"),(location_CH,"CH"),(location_TV,"TV"),(location_FM,"FM"),(location_TA,"TA"),(location_RR,"RR"),(location_QF,"QF"),(location_DB,"DB"),(location_LF,"LF"),(location_DM,"DM"),(location_SK,"SK"),(location_NT,"NT")]


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

to_gephi(G_p,"combination")
