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


#first nine
#node_file_glasgow = '/home/dewigould/Documents/PROJECT/first_nine_nodes.csv'
#edge_file_glasgow = '/home/dewigould/Documents/PROJECT/first_nine_edges.csv'

#node_file_barcelona = '/home/dewigould/Documents/PROJECT/Barcelona/firstnine_nodes.csv'
#edge_file_barcelona = '/home/dewigould/Documents/PROJECT/Barcelona/firstnine_edges.csv'

#node_file_glasgow = '/home/dewigould/Documents/PROJECT/fourteen_nodes.csv'
#edge_file_glasgow = '/home/dewigould/Documents/PROJECT/fourteen_edges.csv'

#node_file_barcelona = '/home/dewigould/Documents/PROJECT/Barcelona/fifteen_nodes.csv'
#edge_file_barcelona = '/home/dewigould/Documents/PROJECT/Barcelona/fifteen_edges.csv'

#G_gephi_gla = csv_to_nx_graph(node_file_glasgow,edge_file_glasgow)

#G_gephi_bar = csv_to_nx_graph(node_file_barcelona,edge_file_barcelona)

G_gephi_gla = nx.read_gexf('/home/dewigould/Documents/PROJECT/gla_with_mod.gexf')

print "1"
#to_gephi(G_gephi_gla,"gla_with_mod")
#to_gephi(G_gephi_bar,"bar_with_mod")
G_gephi_bar = nx.read_gexf('/home/dewigould/Documents/PROJECT/Barcelona/bar_with_mod.gexf')

print "2"

module_defining_property = 'modularity_class'
names_modules_gephi_gla = list_of_modules(G_gephi_gla,module_defining_property)[0]
feature_gephi_gla=list_of_modules(G_gephi_gla,module_defining_property)[1]
z_links_gephi_gla,z_weights_gephi_gla,P_links_gephi_gla, P_weights_gephi_gla,regions_GEPHIl_gla,regions_GEPHIw_gla = within_mod_deg_vs_part_coeff(G_gephi_gla,names_modules_gephi_gla,feature_gephi_gla)
print "3"
names_modules_gephi_bar = list_of_modules(G_gephi_bar,module_defining_property)[0]
feature_gephi_bar=list_of_modules(G_gephi_bar,module_defining_property)[1]
z_links_gephi_bar,z_weights_gephi_bar,P_links_gephi_bar, P_weights_gephi_bar,regions_GEPHIl_bar,regions_GEPHIw_bar = within_mod_deg_vs_part_coeff(G_gephi_bar,names_modules_gephi_bar,feature_gephi_bar)

print "4"


#P_weights_combined = P_weights_gephi_gla.values()
#for i in P_weights_gephi_bar.values():
#	P_weights_combined.append(i)

#z_weights_combined = z_weights_gephi_gla.values()
#for j in z_weights_gephi_bar.values():
#	z_weights_combined.append(j)




name = nx.get_node_attributes(G_gephi_gla,module_defining_property)
name_band = nx.get_node_attributes(G_gephi_gla,"Name")
type_post = nx.get_node_attributes(G_gephi_gla, "type_post")
name_b = nx.get_node_attributes(G_gephi_bar,module_defining_property)
name_band_b = nx.get_node_attributes(G_gephi_bar,"Name")
type_post_b = nx.get_node_attributes(G_gephi_bar, "type_post")

colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
list_colors = colors.keys()

#Glasgow
color={}
#for names in names_modules_gephi_gla:
#	color[names] = list_colors[names_modules_gephi_gla.index(names)]

#add region as attribute and set colors from region
R_dict = {}
R_occupancy_gla = {}
for i in np.arange(1,8):
	R_occupancy_gla[i] = 0
for regions in regions_GEPHIw_gla:
	R_occupancy_gla[regions_GEPHIw_gla.index(regions) +1] += (len(regions))/(float(nx.number_of_nodes(G_gephi_bar)))

	
	for node in regions:
		
		R = regions_GEPHIw_gla.index(regions) + 1
		R_dict[node] = R
		color[R] = list_colors[regions_GEPHIw_gla.index(regions)]
nx.set_node_attributes(G_gephi_gla,"Region",R_dict)
	
markers_dict = {"photo": "o", "link": "D", "video":"*", "status": "<", "event": "s","music": ">"}

region_node = nx.get_node_attributes(G_gephi_gla,"Region")

coloring = {}
markers = {}
for node in P_weights_gephi_gla.keys():

	#coloring[node] = color[name[node]]
	coloring[node] = color[region_node[node]]
	markers[node] = markers_dict[type_post[node]]
	
	
plt.figure(1)
plt.subplot(311)
plt.title("Glasgow")
for node in P_weights_gephi_gla.keys():
	plt.scatter(P_weights_gephi_gla[node],z_weights_gephi_gla[node],c=coloring[node],marker = markers[node])
for region in regions_GEPHIw_gla:
	z_values = []
	P_values = []
	for node in region:
		z_values.append(z_weights_gephi_gla[node])
		P_values.append(P_weights_gephi_gla[node])
	if z_values != [] or P_values != []:
		print "REGION: R",regions_GEPHIw_gla.index(region)+1
		#plt.plot((min(P_values),max(P_values)),(max(z_values),max(z_values)),'r')
		#plt.plot((min(P_values),max(P_values)),(min(z_values),min(z_values)),'r')
		#plt.plot((min(P_values),min(P_values)),(min(z_values),max(z_values)),'r')
		#plt.plot((max(P_values),max(P_values)),(min(z_values),max(z_values)),'r')

plt.xlabel("Participation Coefficient, P")
plt.ylabel("Within Module Degree, z")

patches = []
#for i in names_modules_gephi_gla:
#	patches.append(mpatches.Patch( color=list_colors[names_modules_gephi_gla.index(i)],label =i ) )
for region in regions_GEPHIw_gla:
	patches.append(mpatches.Patch( color =list_colors[regions_GEPHIw_gla.index(region)],label =regions_GEPHIw_gla.index(region)+1))
plt.legend(handles = patches)

#Barcelona

color_b={}
#for names in names_modules_gephi_bar:
#	color_b[names] = list_colors[names_modules_gephi_bar.index(names)]

R_dict_b= {}
R_occupancy_bar = {}
for i in np.arange(1,8):
	R_occupancy_bar[i] = 0
for regions in regions_GEPHIw_bar:
	R_occupancy_bar[regions_GEPHIw_bar.index(regions)+1] += (len(regions))/(float(nx.number_of_nodes(G_gephi_bar)))

	for node in regions:
		
		R = regions_GEPHIw_bar.index(regions) + 1
		R_dict_b[node] = R
		color_b[R] = list_colors[regions_GEPHIw_bar.index(regions)]
nx.set_node_attributes(G_gephi_bar,"Region",R_dict_b)
region_node_b = nx.get_node_attributes(G_gephi_bar,"Region")
coloring_b = {}
markers_b = {}
for node in P_weights_gephi_bar.keys():
	coloring_b[node] = color_b[region_node_b[node]]
	#coloring_b[node] = color_b[name_b[node]]
	markers_b[node] = markers_dict[type_post_b[node]]
	
	
plt.subplot(312)
plt.title("Barcelona")
for node in P_weights_gephi_bar.keys():
	plt.scatter(P_weights_gephi_bar[node],z_weights_gephi_bar[node],c=coloring_b[node],marker = markers_b[node])
for region in regions_GEPHIw_bar:
	z_values = []
	P_values = []
	for node in region:
		z_values.append(z_weights_gephi_bar[node])
		P_values.append(P_weights_gephi_bar[node])
	if z_values != [] or P_values != []:
		print "REGION: R",regions_GEPHIw_bar.index(region) +1
		#plt.plot((min(P_values),max(P_values)),(max(z_values),max(z_values)),'r')
		#plt.plot((min(P_values),max(P_values)),(min(z_values),min(z_values)),'r')
		#plt.plot((min(P_values),min(P_values)),(min(z_values),max(z_values)),'r')
		#plt.plot((max(P_values),max(P_values)),(min(z_values),max(z_values)),'r')

plt.xlabel("Participation Coefficient, P")
plt.ylabel("Within Module Degree, z")

patches_b = []
#for i in names_modules_gephi_bar:
#	patches.append(mpatches.Patch( color=list_colors[names_modules_gephi_bar.index(i)],label =i ) )
for region in regions_GEPHIw_bar:
	patches_b.append(mpatches.Patch( color =list_colors[regions_GEPHIw_bar.index(region)],label =regions_GEPHIw_bar.index(region)+1))
plt.legend(handles = patches_b)



#BAR CHART OF REGION OCCUPANCIES AS PERCENTAGES
plt.subplot(313)
"""
plt.title("Combined. Blue = Gla, Yellow = Bar")

#Combined 
color_combined = []
for i in np.arange(len(P_weights_gephi_gla.values())):
	color_combined.append("blue")
for j in np.arange(len(P_weights_gephi_gla.values()),len(P_weights_gephi_gla.values())+len(P_weights_gephi_bar.values()) ):
	color_combined.append("yellow")

plt.scatter(P_weights_combined,z_weights_combined,c=color_combined)
plt.xlabel("P")
plt.ylabel("z")

plt.show()
"""
# data to plot
n_groups = 7

values_gla = R_occupancy_gla.values()
values_bar = R_occupancy_bar.values()

print R_occupancy_gla
print R_occupancy_bar
# create plot

index = np.arange(n_groups)
bar_width = 0.6
opacity = 0.8
 
plt.bar(index, values_gla, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Glasgow Data')
 
plt.bar(index + bar_width, values_bar, bar_width,
                 alpha=opacity,
                 color='y',
                 label='Barcelona Data')
 
plt.xlabel('Region')
plt.ylabel('Fraction of nodes in region')
plt.title('Region Occupancy Comparison')
plt.xticks(index + bar_width, R_occupancy_gla.keys())
plt.legend()
 
plt.tight_layout()


print "done"


#Examine composition of regions
list_types = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
list_types_b = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
for region in regions_GEPHIw_gla:
	for node in region:
		list_types[regions_GEPHIw_gla.index(region)][markers_dict.keys().index(type_post[node])] += 1

for region in regions_GEPHIw_bar:
	for node in region:
		list_types_b[regions_GEPHIw_bar.index(region)][markers_dict.keys().index(type_post_b[node])] += 1


#not working

for i in list_types:
	for j in np.arange(6):
		if sum(i) != 0:
			i[j] /= float(sum(i))
for i in list_types_b:
	for j in np.arange(6):
		if sum(i) != 0:
			i[j] /= float(sum(i))
plt.figure(2)
# data to plot
n_groups_two = 7

values_gla_two = list_types
values_bar_two = list_types_b


print values_gla_two
print values_bar_two
# create plot

index_two = (np.arange(n_groups_two))
print markers_dict.keys()



	
for i in np.arange(6):
	for j in np.arange(7):
		plt.bar(index_two + (i*(bar_width/float(12))), [el[i] for el in values_gla_two], bar_width/float(12),
        			 alpha=opacity,
                		 color=list_colors[i])
 
		plt.bar(index_two + ((i+7)*(bar_width/float(12))), [el[i] for el in values_bar_two], bar_width/float(12),
				 alpha=opacity,
       				 color=list_colors[i])
 
plt.xlabel('Region')
plt.ylabel('Fraction of nodes of type')
plt.title('Region Occupancy Comparison')
plt.xticks(index_two + bar_width, R_occupancy_gla.keys())

patches_bar = []
for i in np.arange(6):
	patches_bar.append(mpatches.Patch( color =list_colors[i],label = markers_dict.keys()[i]))
plt.legend(handles = patches_bar)
 
plt.tight_layout()
plt.show()

print "done"




