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

node_file_glasgow = '/home/dewigould/Documents/PROJECT/Barcelona/fifteen_nodes.csv'
edge_file_glasgow = '/home/dewigould/Documents/PROJECT/Barcelona/fifteen_edges.csv'

G_gephi_gla = csv_to_nx_graph(node_file_glasgow,edge_file_glasgow)

print "1"
names_modules_gephi_gla = list_of_modules(G_gephi_gla,"modularity_class")[0]
print "2"
feature_gephi_gla=list_of_modules(G_gephi_gla,"modularity_class")[1]
print "3"
z_links_gephi_gla,z_weights_gephi_gla,P_links_gephi_gla, P_weights_gephi_gla,regions_GEPHIl_gla,regions_GEPHIw_gla = within_mod_deg_vs_part_coeff(G_gephi_gla,names_modules_gephi_gla,feature_gephi_gla)

name = nx.get_node_attributes(G_gephi_gla,"modularity_class")
type_post = nx.get_node_attributes(G_gephi_gla, "type_post")



colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
list_colors = colors.keys()

#Glasgow
color={}
for names in names_modules_gephi_gla:
	color[names] = list_colors[names_modules_gephi_gla.index(names)]
	
markers_dict = {"photo": "o", "link": "D", "video":"*", "status": "<", "event": "s","music": ">"}

print "4"
coloring = {}
markers = {}
for node in P_weights_gephi_gla.keys():

	coloring[node] = color[name[node]]
	markers[node] = markers_dict[type_post[node]]
	
print "5"
plt.figure(1)
plt.subplot(311)
plt.title("Glasgow")

R_dict = {}
for node in P_weights_gephi_gla.keys():
	plt.scatter(P_weights_gephi_gla[node],z_weights_gephi_gla[node],c=coloring[node],marker = markers[node])
for region in regions_GEPHIw_gla:
	z_values = []
	P_values = []
	for node in region:
		z_values.append(z_weights_gephi_gla[node])
		P_values.append(P_weights_gephi_gla[node])
	if z_values != [] or P_values != []:
		R = regions_GEPHIw_gla.index(region) + 1
		print "REGION: R",R, len(region)
		nx.set_node_attributes(G_gephi_gla,"Region",R)
		names = []
		types = []
		for node in region:
			names.append(name[node])
			types.append(type_post[node])
			R_dict[node] = R
		print Counter(names)
		print Counter(types)
			
		plt.plot((min(P_values),max(P_values)),(max(z_values),max(z_values)),'r')
		plt.plot((min(P_values),max(P_values)),(min(z_values),min(z_values)),'r')
		plt.plot((min(P_values),min(P_values)),(min(z_values),max(z_values)),'r')
		plt.plot((max(P_values),max(P_values)),(min(z_values),max(z_values)),'r')

plt.xlabel("Participation Coefficient, P")
plt.ylabel("Within Module Degree, z")

patches = []
for i in names_modules_gephi_gla:
	patches.append(mpatches.Patch( color=list_colors[names_modules_gephi_gla.index(i)],label =i ) )
plt.legend(handles = patches)

plt.show()
#nx.set_node_attributes(G_gephi_gla,"Region",R_dict)
#to_gephi(G_gephi_gla,"barcelona_updated")
print "done"



