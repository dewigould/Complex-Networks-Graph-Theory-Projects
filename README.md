# Barcelona_Networks_Project
Social Network Analysis of Music Communities in Major Cities

Information on Python Codes, Files etc.
Dewi Gould
27.7.17



SPOTIFY DATA information
the following website was used to find the most popular songs (and by extension bands) in the target areas:
https://spotifymaps.github.io/musicalcities/
I then used Netvizz to download the data for last 50 posts from the Facebook pages of these bands. One or two bands were not used as they didn’t have any engagement at all on their posts, or they had far too much engagement for the computer to handle.


	•	proj_and_comm.py
	⁃	contains various functions used throughout both projects
	⁃	bipartite_generate
	⁃	produces NetworkX bipartite graph given networkX graph
	⁃	other functions pretty much self-explanatory
	⁃	to_gephi(G,name)
	⁃	this converts a networkx graph file to a .gexf file to be analysed in Gephi


Codes for work on University Pages.

	•	Engagement_Plotter.py 
	⁃	engagement_numbers(Location)
	⁃	Location is the file path to the ‘full statistics’ file generated using Netvizz
	⁃	This function generates a list of ‘engagement numbers’ from the file
	⁃	produce_data(Location)
	⁃	Location is same as above
	⁃	this yields a plot of either histogram or powerlaw/ exponential/ stretched exponential/ lognormal fit
	⁃	Choice of data, timeframe and type of graph plotted set using variables ‘University, TimeFrame, graph_type’
	•	Compare.py
	⁃	same functions as Engagement_Plotter
	⁃	also contains function ‘combine_data(Locations)’
	⁃	this takes a list of file paths and combines them into one large list for grouped analysis
	⁃	This code in general can plot the data for one specific University page over a larger time frame, to see if the fits and data have changed dramatically over time or not.

Codes for Work on Music Community Analysis.

	•	gdf_to_dff_new_new.py
	⁃	converts .gdf file from Netvizz to NetworkX graph and Pandas data frame object.
	•	Gephi_tables.py
	⁃	takes node file path and edge file path (exported from Gephi in .csv format) and generates a NetworkX graph
	⁃	only adds back attributes needed for further analysis 
	•	Cartography.py
	⁃	creates z/P plane plot
	⁃	list_of_modules(G,feature)
	⁃	feature is a string (in my case either “Name” or “modularity_class”, by which you define the modules)
	⁃	within_mod_deg_vs_part_coeff
	⁃	plots the z/P graph
	⁃	lots of things returned by function, names reasonable self-explanatory…this function is quite messy with a lot of stuff I kept but don’t use anymore
	•	Barcelona.py
	⁃	this is just an example code of how I used the other codes to produce a networkx graph given the raw data
	•	COMBINE.py
	⁃	creates one large projected or raw NetworkX graph by combining .gdf files from any amount of pages.
	•	Tester.py
	⁃	this is just what I used to implement different ideas
	⁃	it is very messy and jumbled, but basically just how I plotted the various combinations of z/P graphs and bar charts.
	⁃	There is a lot of extraneous stuff that isn’t needed, but I was just playing around to try and see what I could produce
	⁃	this code probably isn’t very useful, sorry!




Acronym Information:


GLASGOW: 750 nodes, 51,144 edges (projected graph)

Acronym: Band Name: Number of engaged users: number of engagements (likes+ comments)

GB: George Bowie: 6831:10,095
GC: Gerry Cinnamon: 6154:23,919
TP: The Proclaimers: 14,382:29,532
CH: Charlie and the Bhoys: 10,037:21,857
TV: The View: 10,838: 24,175
FM: Frankie Miller: 3,383 : 8,471
TA: Twin Atlantic: 3,687: 12,096
RR: Runrig: 12,760: 31,923
QF: QFX: 2,635: 5,183
DB: Deacon Blue: 9,969: 26,549
LF: The LaFontaines: 4,064: 13,928
DM: Dougie MacLean: 2,858: 9,740
SK: Skipinnish: 9,408: 24,736
NT: N-Trance: 455: 897


BARCELONA: 750 nodes, 188,563 edges (projected graph)
Acronym: Band Name: Number of engaged users: number of engagements (likes+ comments)

TX: Txarango: 16,834: 55,991
EL: Els Amics de les Arts: 3,394: 8,467
BL: Blaumut: 3,311: 12,949
DP: Doctor Prats: 12,719: 40,213
SC: Sopra de Cabris: 1,629: 5,806
EC: Els Cotarres: 19,733: 56,356
GO: Gossos: 1,391: 4236
BH: Buhos: 13,015: 35,354
ML: Maurel: 6,488: 14,300
JD: Joan Dosa: 3,865: 11,825
LB: Lax’n’busto: 6,282: 18,276
IB: Itaca Band: 10,026: 18,176
AF: Antonia Font: 7,141: 18,629
LI: La Iaia: 2,033: 61,655
EP: Els Pets: 2,947: 4,740



