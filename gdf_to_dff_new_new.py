def gdf_to_dff(location, netvizz=True, node_attr=True, isolated_nodes=True):
    import codecs
    from StringIO import StringIO
    import pandas as pd
    import networkx as nx
    import numpy as np

    # words that are not part of the node/edge attribute names
    words=['INTEGER','DOUBLE','VARCHAR','FLOAT','INT','BOOLEAN']
    # Opening input file
    gdf_file = codecs.open(location, "r", "utf-8")

    # Deducing node attributes from heading
    head1 = gdf_file.readline()
    # fixing possible netvizz bug
    if netvizz==True:
        head1 = head1.replace(',\n', '\n')
    # Removing unnecessary words
    for x in words:
        head1=head1.replace(x, '')
    head1 = head1.replace('nodedef>name', 'name')

    # Removing unnecessary/ambiguous spaces before and after ','
    l = len(head1)
    l1 = 2 * l
    while l != l1:
        l = len(head1)
        head1 = head1.replace(', ', ',')
        head1 = head1.replace(' ,', ',')
        head1 = head1.replace(' \n', '\n')
        l1 = len(head1)

    print head1
    val = head1.split(',')
    print 'header1: # of columns of the nodes df=',len(val)

    # Reading node block
    line = gdf_file.readline()
    l = len(line)
    l1 = 2 * l
    # Removing unnecessary/ambiguous spaces before and after ','
    while l != l1:
        l = len(line)
        line = line.replace(', ', ',')
        line = line.replace(' ,', ',')
        l1 = len(line)
    if netvizz==True:
        line = line.replace(',\n', '\n')
    block1=''
    val = line.split(',')
    print '1st line: # of columns of the nodes df=',len(val)

    # Node block ends where edge block starts
    val = line.split(',')[0]
    while val != "edgedef>node1 VARCHAR":
        l=len(line)
        l1=2*l
        # Removing unnecessary/ambiguous spaces before and after ','
        while l!=l1:
            l=len(line)
            line = line.replace(', ', ',')
            line = line.replace(' ,', ',')
            l1=len(line)
        # fixing possible netvizz bug
        if netvizz == True:
            line = line.replace(',\n', '\n')
        block1+=line
        line = gdf_file.readline()
        val = line.split(',')[0]

    # Deducing edge attributes from heading
    head2=line
    # Removing unnecessary words
    for x in words:
        head2=head2.replace(x, '')
    head2 = head2.replace('edgedef>node1', 'node1')
    head2=head2.encode('utf-8').strip(' ')
    # Removing unnecessary/ambiguous spaces before and after ','
    l = len(head2)
    l1 = 2 * l
    while l != l1:
        l = len(head2)
        head2 = head2.replace(', ', ',')
        head2 = head2.replace(' ,', ',')
        head2 = head2.replace(' \n', '\n')
        l1 = len(head2)
    print head2

    # Reading edge block
    line = gdf_file.readline()
    l = len(line)
    l1 = 2 * l
    # Removing unnecesary/ambiguos spaces befor and after ','
    while l != l1:
        l = len(line)
        line = line.replace(', ', ',')
        line = line.replace(' ,', ',')
        l1 = len(line)
    block2=''
    val = line.split(',')[0]

    # Edge block ends at the end of the file
    while val != "":
        block2+=line
        line = gdf_file.readline()
        l=len(line)
        l1=2*l
        # Removing unnecesary/ambiguos spaces befor and after ','
        while l!=l1:
            l=len(line)
            line = line.replace(', ', ',')
            line = line.replace(' ,', ',')
            l1=len(line)
        # fixing possible netvizz bug
        if netvizz == True:
            line = line.replace(',\n', '\n')
        val = line.split(',')[0]

    # Creating node dataframe
    nodes=StringIO(head1+block1)
    dfn = pd.read_csv(nodes,encoding='utf-8')
    #dfn = pd.read_csv(nodes)

    # Creating edge dataframe
    edges=StringIO(head2+block2)
    dfe = pd.read_csv(edges, encoding='utf-8')

    # ---- CORE ---- #
    # From edge dataframe to NetworkX graph:
    head2=head2.strip('\n')
    val = head2.split(',')
    cnames=[]
    for i in range(2,len(val)):
        cnames+=[val[i]]
    G=nx.from_pandas_dataframe(dfe, val[0], val[1], cnames)

    # Printing the number of nodes
    print 'Graph created from edge list. #Nodes=',len(G.nodes())

    # Adding isolated nodes that do not appear in the edge list (dataframe)
    if isolated_nodes==True:
        for name in dfn[dfn.columns[0]]:
            if name not in G.nodes():
                G.add_node(name)
                print 'NO EDGE AT',name
        print 'Isolated nodes added. #Nodes =',len(G.nodes())

    # Adding node attributes
    if node_attr==True:
        print len(dfn['name'])
        for i in range(len(dfn['name'])):
            n = dfn['name'][i]
            for j in range(2, len(dfn.columns)):
                G.node[n][dfn.columns[j]] = str(dfn[dfn.columns[j]][i])
        print 'Node attributes have been added'

    return G,dfn,dfe

