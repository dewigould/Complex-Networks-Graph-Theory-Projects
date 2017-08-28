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
#LAST 5 POSTS

"""
#Venues
file_location_KTWWH = '/home/dewigould/Documents/GLA_music/KTWWH/page_6550684326_2017_07_10_13_27_40.gdf'
file_location_BREL = '/home/dewigould/Documents/GLA_music/BREL/page_192284490793474_2017_07_10_13_26_59.gdf'
file_location_OM = '/home/dewigould/Documents/GLA_music/OM/page_199165466767100_2017_07_10_13_28_22.gdf'
file_location_O2 = '/home/dewigould/Documents/GLA_music/O2/page_37896989445_2017_07_10_13_30_42.gdf'
file_location_SUBCLUB = '/home/dewigould/Documents/GLA_music/SUBCLUB/page_49355553078_2017_07_10_13_32_14.gdf'
file_location_GLAD_CAFE = '/home/dewigould/Documents/GLA_music/GLAD_CAFE/page_351164933346_2017_07_11_12_35_05.gdf'
file_location_STEREO = '/home/dewigould/Documents/GLA_music/STEREO/page_198149335046_2017_07_11_12_32_40.gdf'
file_location_MONO = '/home/dewigould/Documents/GLA_music/MONO/page_359026328605_2017_07_11_12_33_32.gdf'
file_location_O2_AC = '/home/dewigould/Documents/GLA_music/O2_AC/page_34618900088_2017_07_11_12_29_48.gdf'
file_location_SSE_HYDRO = '/home/dewigould/Documents/GLA_music/SSE_HYDRO/page_303943599621915_2017_07_11_12_30_57.gdf'

#Artists
file_location_WHITE = '/home/dewigould/Documents/GLA_music/WHITE/page_380285582113401_2017_07_11_10_57_37.gdf'
file_location_CATHOLIC_ACTION ='/home/dewigould/Documents/GLA_music/CATHOLICACTION/page_585453434908724_2017_07_11_11_01_24.gdf'
file_location_HAPPYMEALS ='/home/dewigould/Documents/GLA_music/HAPPYMEALS/page_649216958512474_2017_07_11_10_59_11.gdf'
file_location_TIJUANABIBLES ='/home/dewigould/Documents/GLA_music/TIJUANABIBLES/page_108432425914828_2017_07_11_11_02_26.gdf'
file_location_NEON_WALTZ = '/home/dewigould/Documents/GLA_music/NEONWALTZ/page_507257085958297_2017_07_11_11_03_35.gdf'

#Festivals
file_location_TRNSMT = '/home/dewigould/Documents/GLA_music/TRNSMT/page_367980976875635_2017_07_11_12_36_35.gdf'
file_location_GLA_MUS_FEST = '/home/dewigould/Documents/GLA_music/GLA_MUS_FEST/page_406793692823247_2017_07_11_12_37_45.gdf'

"""
#LAST 50 POSTS

#Venues
file_location_KTWWH = '/home/dewigould/Documents/GLA_music/last 50/KTWWH/page_6550684326_2017_07_11_09_48_16.gdf'
file_location_BREL = '/home/dewigould/Documents/GLA_music/last 50/BREL/page_192284490793474_2017_07_11_09_49_58.gdf'
file_location_OM = '/home/dewigould/Documents/GLA_music/last 50/OM/page_199165466767100_2017_07_11_09_51_27.gdf'
file_location_O2 = '/home/dewigould/Documents/GLA_music/last 50/O2/page_37896989445_2017_07_11_09_52_40.gdf'
file_location_SUBCLUB = '/home/dewigould/Documents/GLA_music/last 50/SUBCLUB/page_49355553078_2017_07_11_09_54_06.gdf'
file_location_GLAD_CAFE = '/home/dewigould/Documents/GLA_music/last 50/GLAD_CAFE/page_351164933346_2017_07_11_14_22_38.gdf'
file_location_STEREO = '/home/dewigould/Documents/GLA_music/last 50/STEREO/page_198149335046_2017_07_11_14_23_45.gdf'
file_location_MONO = '/home/dewigould/Documents/GLA_music/last 50/MONO/page_359026328605_2017_07_11_14_24_34.gdf'
file_location_O2_AC = '/home/dewigould/Documents/GLA_music/last 50/O2_AC/page_34618900088_2017_07_11_14_25_28.gdf'
file_location_SSE_HYDRO = '/home/dewigould/Documents/GLA_music/last 50/HYDRO/page_303943599621915_2017_07_11_14_26_47.gdf'

#Artists
file_location_WHITE = '/home/dewigould/Documents/GLA_music/last 50/WHITE/page_380285582113401_2017_07_11_14_28_27.gdf'
file_location_CATHOLIC_ACTION ='/home/dewigould/Documents/GLA_music/last 50/CATHOLIC_ACTION/page_585453434908724_2017_07_11_14_29_20.gdf'
file_location_HAPPYMEALS ='/home/dewigould/Documents/GLA_music/last 50/HAPPYMEALS/page_649216958512474_2017_07_11_14_30_24.gdf'
file_location_TIJUANABIBLES ='/home/dewigould/Documents/GLA_music/last 50/TIJUANABIBLES/page_108432425914828_2017_07_11_14_31_37.gdf'
file_location_NEON_WALTZ = '/home/dewigould/Documents/GLA_music/last 50/NEONWALTZ/page_507257085958297_2017_07_11_14_32_54.gdf'
file_location_BABY_STRANGE = '/home/dewigould/Documents/GLA_music/last 50/BABY_STRANGE/page_460155270661241_2017_07_12_10_18_57.gdf'
file_location_HALFRICAN = '/home/dewigould/Documents/GLA_music/last 50/HALFRICAN/page_354798264559216_2017_07_12_10_23_48.gdf'
file_location_LAPELLES = '/home/dewigould/Documents/GLA_music/last 50/LAPELLES/page_472757336111260_2017_07_12_10_20_44.gdf'
file_location_TNFS = '/home/dewigould/Documents/GLA_music/last 50/TNFS/page_434670703223185_2017_07_12_10_15_57.gdf'


#including festivals

#Locations = [(file_location_KTWWH,"KTWWH","Venue"), (file_location_BREL, "Brel","Venue"), (file_location_OM,"OM","Venue"),( file_location_O2, "O2","Venue"),( file_location_SUBCLUB,"Subclub","Venue"),( file_location_WHITE,"White","Band"),( file_location_CATHOLIC_ACTION,"Catholic Action", "Band"),( file_location_HAPPYMEALS,"Happy Meals","Band"),( file_location_TIJUANABIBLES, "Tijuana Bibles","Band"),( file_location_NEON_WALTZ,"Neon Waltz", "Band"), (file_location_GLAD_CAFE,"Glad Cafe","Venue"),(file_location_TRNSMT,"TRNSMT","Festival"),(file_location_GLA_MUS_FEST,"Glasgow Music Festival", "Festival"),(file_location_STEREO,"Stereo","Venue"),(file_location_MONO,"MONO","Venue"),(file_location_O2_AC,"O2 Academy","Venue"),(file_location_SSE_HYDRO,"SSE HYDRO","Venue"),(file_location_BABY_STRANGE,"Baby Strange","Band"),(file_location_HALFRICAN,"Halfrican","Band"),(file_location_LAPELLES,"Lapelles","Band"),(file_location_TNFS,"The New Fabian Society","Band")]

#not including festivals
Locations = [(file_location_KTWWH,"KTWWH","Venue"), (file_location_BREL, "Brel","Venue"), (file_location_OM,"OM","Venue"),( file_location_O2, "O2","Venue"),( file_location_SUBCLUB,"Subclub","Venue"),( file_location_WHITE,"White","Band"),( file_location_CATHOLIC_ACTION,"Catholic Action", "Band"),( file_location_HAPPYMEALS,"Happy Meals","Band"),( file_location_TIJUANABIBLES, "Tijuana Bibles","Band"),( file_location_NEON_WALTZ,"Neon Waltz", "Band"), (file_location_GLAD_CAFE,"Glad Cafe","Venue"),(file_location_STEREO,"Stereo","Venue"),(file_location_MONO,"MONO","Venue"),(file_location_O2_AC,"O2 Academy","Venue"),(file_location_SSE_HYDRO,"SSE HYDRO","Venue"),(file_location_BABY_STRANGE,"Baby Strange","Band"),(file_location_HALFRICAN,"Halfrican","Band"),(file_location_LAPELLES,"Lapelles","Band"),(file_location_TNFS,"The New Fabian Society","Band")]

#just bands
#Locations = [( file_location_WHITE,"White","Band"),( file_location_CATHOLIC_ACTION,"Catholic Action", "Band"),( file_location_HAPPYMEALS,"Happy Meals","Band"),( file_location_TIJUANABIBLES, "Tijuana Bibles","Band"),( file_location_NEON_WALTZ,"Neon Waltz", "Band"),(file_location_BABY_STRANGE,"Baby Strange","Band"),(file_location_HALFRICAN,"Halfrican","Band"),(file_location_LAPELLES,"Lapelles","Band"),(file_location_TNFS,"The New Fabian Society","Band")]

#just venues
#Locations = [(file_location_KTWWH,"KTWWH","Venue"), (file_location_BREL, "Brel","Venue"), (file_location_OM,"OM","Venue"),( file_location_O2, "O2","Venue"), (file_location_GLAD_CAFE,"Glad Cafe","Venue"),(file_location_STEREO,"Stereo","Venue"),(file_location_MONO,"MONO","Venue"),(file_location_O2_AC,"O2 Academy","Venue"),(file_location_SSE_HYDRO,"SSE HYDRO","Venue")]


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
		nx.set_node_attributes(graph,"Type of Page", Locations[counter][2])
		counter += 1

	#add all individual graphs into one connected graph

	G_complete = nx.Graph()
	for graph in G_raw:
		G_complete = nx.compose(G_complete,graph)



	G_complete_p,top_nodes,bottom_nodes = bipartite_generate(G_complete, Which_nodes = top_or_bottom)
	return G_complete,G_complete_p,top_nodes,bottom_nodes


#produce graph from data above (RAW) ie. unprojected, and PROJECTED graph
G_raw,G_p,top_nodes,bottom_nodes = combine_graphs_and_project(Locations,"top")

#yield edge weight distributions for raw and projected graphs
#edge_weight_distribution(G_complete,top_nodes)
#edge_weight_distribution(G_complete_p,top_nodes)

#yield degree distribution for projected graph
#degree_distribution(G_p,top_nodes)


#create .gexf file for raw or projected graphs
#to_gephi(G_raw,"All_proj")
#to_gephi(G_p, "just_venues")





#Plot z-P plane graph for projected graph (modules are "Name")
names_modules = list_of_modules(G_p,"Name")[0]
feature=list_of_modules(G_p,"Name")[1]
z_links,z_weights,P_links,P_weights,regionsl,regionsw = within_mod_deg_vs_part_coeff(G_p,names_modules,feature)



#node and edge files exported from GEPHI
#Bands and Venues
node_file = '/home/dewigould/Documents/GLA_music/FORCOMPARISON/Bands_and_venues/Nodes(bandsandvenues).csv'
edge_file = '/home/dewigould/Documents/GLA_music/FORCOMPARISON/Bands_and_venues/Edges(bansdandvenues).csv'

#Just Bands
#node_file = '/home/dewigould/Documents/GLA_music/FORCOMPARISON/Just_bands/Nodes_justbands.csv'
#edge_file = '/home/dewigould/Documents/GLA_music/FORCOMPARISON/Just_bands/Edges_justbands.csv'

#Just Venues
#node_file = '/home/dewigould/Documents/GLA_music/FORCOMPARISON/Just_venues/Nodes_justvenues.csv'
#edge_file = '/home/dewigould/Documents/GLA_music/FORCOMPARISON/Just_venues/Edges_justvenues.csv'

G_gephi = csv_to_nx_graph(node_file,edge_file)

#Plot z-p graph for GEPHI modularity modules
names_modules_gephi = list_of_modules(G_gephi,"modularity_class")[0]
feature_gephi=list_of_modules(G_gephi,"modularity_class")[1]
z_links_gephi,z_weights_gephi,P_links_gephi, P_weights_gephi,regions_GEPHIl,regions_GEPHIw = within_mod_deg_vs_part_coeff(G_gephi,names_modules_gephi,feature_gephi)

print "done"


plt.figure(1)
plt.subplot(311)
plt.title("Modules = Band/ Venue Names")
plt.scatter(P_weights.values(),z_weights.values())
plt.plot((0, 1), (2.5, 2.5), 'r')
plt.plot((0,1),(5,5),'r')
plt.plot((0.05,0.05),(0,2.5),'r')
plt.plot((0.625,0.625),(0,2.5),'r')
plt.plot((0.8,0.8),(0,2.5),'r')
plt.plot((0.3,0.3),(2.5,5),'r')
plt.plot((0.75,0.75),(2.5,5),'r')
plt.xlabel("Weighted Participation Coefficient, P")
plt.ylabel("Weighted Within Module Degree, z")


"""
plt.subplot(312)
plt.title("Modules = Modularity algorithm (Gephi)")
plt.scatter(P_weights.values(), z_weights_gephi.values())
plt.plot((0, 1), (2.5, 2.5), 'r')
plt.plot((0,1),(5,5),'r')
plt.plot((0.05,0.05),(0,2.5),'r')
plt.plot((0.625,0.625),(0,2.5),'r')
plt.plot((0.8,0.8),(0,2.5),'r')
plt.plot((0.3,0.3),(2.5,5),'r')
plt.plot((0.75,0.75),(2.5,5),'r')
plt.xlabel("Weighted Participation Coefficient, P")
plt.ylabel("Weighted Within Module Degree, z")

plt.subplot(313)
plt.title("Combined")
plt.plot((0, 1), (2.5, 2.5), 'r')
plt.plot((0,1),(5,5),'r')
plt.plot((0.05,0.05),(0,2.5),'r')
plt.plot((0.625,0.625),(0,2.5),'r')
plt.plot((0.8,0.8),(0,2.5),'r')
plt.plot((0.3,0.3),(2.5,5),'r')
plt.plot((0.75,0.75),(2.5,5),'r')
plt.scatter(P_weights.values(),z_weights.values(),label="Modules = Bands/Venues")
plt.scatter(P_weights.values(), z_weights_gephi.values(),label="Modules=Louvain Algorithm")
plt.xlabel("Weighted Participation Coefficient, P")
plt.ylabel("Weighted Within Module Degree, z")
plt.legend(loc='best')
"""
#plt.show()



"""
plt.figure(2)
plt.subplot(311)
plt.title("Modules = Band/ Venue Names")
plt.scatter(P_links.values(),z_links.values())
plt.xlabel("Participation Coefficient, P")
plt.ylabel("Within Module Degree, z")

plt.subplot(312)
plt.title("Modules = Modularity algorithm (Gephi)")
plt.scatter(P_links.values(), z_links_gephi.values())
#plt.xlim(xmin,xmax)
plt.xlabel("Participation Coefficient, P")
plt.ylabel("Within Module Degree, z")

plt.subplot(313)
plt.title("Combined")
#plt.plot((xmin, xmax), (2.5, 2.5), 'r')
plt.scatter(P_links.values(),z_links.values(),label="Modules = Bands/Venues")
plt.scatter(P_links.values(), z_links_gephi.values(),label="Modules=Louvain Algorithm")
plt.xlabel("Participation Coefficient, P")
plt.ylabel("Within Module Degree, z")
plt.legend(loc='best')

plt.show()

"""

jet= plt.get_cmap('jet')
colors = iter(jet(np.linspace(0,1,10)))
#colouring the various zones

#plt.figure(4)
plt.subplot(312)
for region in regionsw:
	print len(region)
	z_values = []
	P_values = []
	for node in region:
		z_values.append(z_weights[node])
		P_values.append(P_weights[node])
	plt.scatter(P_values,z_values,color=next(colors))
	if z_values != [] or P_values != []:
		plt.plot((min(P_values),max(P_values)),(max(z_values),max(z_values)),'r')
		plt.plot((min(P_values),max(P_values)),(min(z_values),min(z_values)),'r')
plt.xlabel("Participation Coefficient, P")
plt.ylabel("Within Module Degree, z")
plt.show()
	





