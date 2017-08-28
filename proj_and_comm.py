from gdf_to_dff_new_new import gdf_to_dff
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
from collections import Counter
from itertools import islice
import numpy as np
import powerlaw
from operator import itemgetter

#import community


# Location of File
#infile= '/home/dewigould/Documents/Comparison/UB/UB01072016-31122016/page_124038361034_2017_06_28_11_47_37.gdf'
#infile = '/home/dewigould/Documents/Comparison/ICL/ICL01072016-31122016/page_148242696837_2017_06_28_12_03_16.gdf'


#small file
#infile = '/home/dewigould/Documents/Comparison/UB/LAST20/page_124038361034_2017_07_07_12_48_09.gdf'


#G1,dfn,dfe=gdf_to_dff(infile,netvizz=True,node_attr=True, isolated_nodes=True)

def bipartite_generate(G,Which_nodes):

	# making G1 a bipartite graph
	#top nodes are posts, bottom nodes are users
	top_nodes1=[]
	bottom_nodes1=[]
	#dictionary of id's and whether they are post '0' or user '1'
	bb={}

	for n in G.nodes():

    		if G.node[n]['type']=='post':
        		bb[n]=0
        		top_nodes1 += [n]
    		else:
        		bb[n] = 1
        		bottom_nodes1 += [n]

	nx.set_node_attributes(G,'bipartite',bb)

	#no duplicate elements
	top_nodes1=set(top_nodes1)
	bottom_nodes1=set(bottom_nodes1)
	
	


	# projection onto post nodes
	print "Is Graph bipartite?: ", bipartite.is_bipartite(G)
	if Which_nodes == "top":	
		Gp1 = bipartite.weighted_projected_graph(G,top_nodes1,ratio=True)
	if Which_nodes == "bottom":
		Gp1 = bipartite.weighted_projected_graph(G,bottom_nodes1,ratio=True)

	# removing isolate nodes (posts with no engagement)
	print 'before:',Gp1.number_of_nodes(), Gp1.number_of_edges()
	Gp1.remove_nodes_from(nx.isolates(Gp1))
	print 'after:',Gp1.number_of_nodes(), Gp1.number_of_edges()

	# giant component - we want to look at only the most connected posts
	print 'before:',Gp1.number_of_nodes(), Gp1.number_of_edges()
	Gcc=sorted(nx.connected_component_subgraphs(Gp1), key = len, reverse=True)
	Gp1=Gcc[0]
	print 'after:',Gp1.number_of_nodes(), Gp1.number_of_edges()
	"""
	# video
	nv=0
	degv=0
	for n in G1.nodes():
    		if G1.node[n]['type_post']=='video':
        		nv+=1.0
        		degv+=G1.degree(n)

	degv/=nv
	print "Average Degree (Video) = ", degv

	# photo
	nph=0
	degph=0
	for n in G1.nodes():
    		if G1.node[n]['type_post']=='photo':
        		nph+=1.0
        		degph+=G1.degree(n)

	degph/=nph
	print "Average Degree (Photo): ", degph


	# user
	nu=0
	degu=0
	for n in G1.nodes():
    		if n in bottom_nodes1:
       			nu+=1.0
        		degu+=G1.degree(n)

	degu/=nu
	print "Average Degree (Users): ", degu
	"""
	return Gp1, top_nodes1, bottom_nodes1


#produce degree distribution of POST NODES PROJECTION
def degree_distribution(G, nodes,weight):

	if weight == True:
		degree_values_users, degree_values_posts = bipartite.degrees(G,nodes,'weight')
	else:
		degree_values_users, degree_values_posts = bipartite.degrees(G,nodes)	

	#take a look at first 20 entries in each
	def take(n, iterable):
    		"Return first n items of the iterable as a list"
    		return list(islice(iterable, n))
	#print take(20,degree_values_posts.iteritems())
	#print take(20,degree_values_users.iteritems())


	vals_posts=degree_values_posts.values()
	average_degree_p = sum(vals_posts)/float(len(vals_posts))
	#crop out larger values
	vals_posts= [s for s in vals_posts if s<=2000]
	data_posts=Counter(vals_posts)

	"""	
	vals_users=degree_values_users.values()
	average_degree_u = sum(vals_users)/float(len(vals_users))
	#crop out larger values
	vals_users=[s for s in vals_users if s<=100]
	data_users=Counter(vals_users)
	"""


	plt.figure(1)

	plt.subplot(211)
	plt.hist(data_posts.keys(),label = "Average Degree = %s" %(average_degree_p))
	plt.title("Degree Distribution (post-projection) Histogram")
	plt.xlabel("Degree")
	plt.ylabel("Number of nodes with degree")
	plt.legend(loc='best')
	"""
	plt.subplot(212)
	plt.hist(data_users.keys(),label = "Average Degree = %s" %(average_degree_u))
	plt.title("Degree Distribution (user-projection) Histrogram")
	plt.xlabel("Degree")
	plt.ylabel("Number of nodes with degree")
	plt.legend(loc='best')
	"""
	plt.show()

def edge_weight_distribution(G,nodes):
	edge_s= G.edges(nodes,"weight")
	weights=[]
	for elements in edge_s:
		weights.append(elements[2])
	
	data_weights = Counter(weights)
	print data_weights
	#vals= data_weights.keys()
	#only look at significant portion
	#vals =[s for s in vals if s<=0.018]
	#average_weight = sum(vals)/float(len(vals))
	plt.figure(2)

	#plt.hist(vals,label = "Average Weight = %s" %(average_weight))
	plt.hist(weights,label = "Hist")
	#plt.scatter(vals,np.log(data_weights.values()))
	plt.title("Weight distribution of projected graph (posts)")
	plt.xlabel("Weight")
	plt.ylabel("Distribution")
	plt.legend(loc='best')
	
	plt.show()

#not working
def edge_weight_fit(G,nodes):
	edges= G.edges(nodes,"weight")
	weights=[]
	for elements in edges:
		weights.append(elements[2])
	data_weights = Counter(weights)
	vals= data_weights.keys()



	d=np.array(vals)
	fit = powerlaw.Fit(d,discrete=True,xmin=0)
	fit.lognormal.plot_pdf(color='b', linestyle='--', label='fit pdf')
	fit.plot_pdf(color='r')
	plt.show()


def to_gephi(G,name):
#write to gexf format for gephi opening
	nx.write_gexf(G, "%s.gexf" %(name))

#GET RESULTS
#G_p, top_nodes, bottom_nodes = bipartite_generate(G1)

#produce plot of degree distribution
#degree_distribution(G1, top_nodes)


#produce plot of weight distribution
#edge_weight_distribution(G_p, top_nodes)

#look at fit on edge weight distribution
#edge_weight_fit(G_p,top_nodes)

#create .gexf file
#to_gephi(G_p)





#some basic statistics

#print "average clustering = ", nx.average_clustering(G_p,top_nodes)
"""
bet_cent_vals_raw = nx.betweenness_centrality(G_p).values()
bet_cent_vals = sorted(bet_cent_vals_raw)
rank=[]
for i in range(1,len(bet_cent_vals)+1):
	rank.append(len(bet_cent_vals)-i)
rank_ten=[]
bet_cent_ten=[]
for i in range(10):
	rank_ten.append(i)
	bet_cent_ten.append(bet_cent_vals[len(bet_cent_vals)-i-1])


cl_cent_vals = nx.closeness_centrality(G_p).values()
print rank_ten
print bet_cent_ten

plt.figure(4)
plt.subplot(211)
plt.title("Betweenness Centrality")
plt.hist(bet_cent_vals)


plt.subplot(212)
plt.title("Closeness Centrality")
plt.hist(cl_cent_vals)
plt.show()

plt.figure(5)
plt.subplot(211)
plt.bar(rank,bet_cent_vals,width=0.8)
plt.ylabel("betweenness centrality")
plt.xlabel("rank of user")
plt.subplot(212)
plt.title("Top ten users")
plt.bar(rank_ten,bet_cent_ten,width=0.8)
plt.ylabel("betweenness centrality")
plt.xlabel("rank of user")
plt.show()
"""

#trying to plot scatter of average lengths...will take WAY too long
"""
lengths_raw=[]
for i in G_p.nodes():
	for j in G_p.nodes():
		print i, nx.dijkstra_path_length(G_p,i,j,"weight")
		a= (i,nx.dijkstra_path_length(G_p,i,j,weight="weight"))
		lengths_raw.append(a)
lengths = sorted(lengths_raw,key=itemgetter(1))

users = zip(*lengths)[0]
lengths_only = zip(*lengths)[1]


plt.figure(6)
plt.scatter(users, lengths_only)
plt.xlabel("Rank of user")
plt.ylabel("Path Length to other users")
plt.show()

"""




