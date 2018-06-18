# Make Networks
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def RTEdgeList(path,screen_namesSource,TweetFiles,EListloc,start,stop):
    print "Creating EdgeList file..."
    f = open(path + EListloc + "RTEdgeList" + str(start) + "_" + str(stop) +
            ".csv","w+")
    f.write("Name1,Name2,Weight\n")


    print "Reading in the screen_names"
    a = pd.read_csv(path +  screen_namesSource)
    screen_names = a['screen_name']
    del a


    i = start
    for name1 in screen_names[start:stop]:
        #print "Getting edges for " + name1
        RTDF = pd.read_csv(path + TweetFiles + name1 + "Retweets.csv")
        RTset = set(RTDF['RTUser'].value_counts().index)
        del RTDF

        for name2 in screen_names[i+1:]:
            #print name2
            tempDF = pd.read_csv(path + TweetFiles + name2 + "Retweets.csv")
            tempSet = set(tempDF['RTUser'].value_counts().index)
            del tempDF

            c = RTset.intersection(tempSet)

            if bool(c) == True:
                f.write(name1 + "," + name2 + "," + str(len(c)) + "\n")

            del tempSet
            del c

        del RTset
        i=i+1

    #print "All Done!"
    f.close()

def ShowRTNetwork(EdgeList,nodes_csv,Tol):
    maxWeight = float(max(EdgeList['Weight']))

    Weights = list(EdgeList['Weight'][EdgeList['Weight']>=Tol].values.flatten()/maxWeight)

    User1 = list(EdgeList['Name1'][EdgeList['Weight']>=Tol].values.flatten())
    User2 = list(EdgeList['Name2'][EdgeList['Weight']>=Tol].values.flatten())

    Attr = pd.read_csv(nodes_csv)

    del EdgeList
    EdgeList = zip(User1,User2,Weights)
    G = nx.Graph()
    nodes = list(set(User1).union(set(User2)))

    G.add_nodes_from(nodes)

    node_size = []
    Colors = []
    #label = []
    for node in G.nodes():
        #G.nodes[node]['color'] = Attr.color[Attr.screen_name==node].values[0]
        #G.nodes[node]['node_size'] = Attr.node_size[Attr.screen_name==node].values[0]
        G.nodes[node]['label'] = Attr.Name[Attr.screen_name==node].values[0]
        node_size.extend([float(Attr.node_size[Attr.screen_name==node].values[0])])
        Colors.extend([Attr.color[Attr.screen_name==node].values[0]])
        #label.extend([Attr.Name[Attr.screen_name==node].values[0]])


    del Attr

    G.add_weighted_edges_from(EdgeList)
    pos = nx.spring_layout(G)
    edgewidth = [d['weight'] for (u,v,d) in G.edges(data=True)]

    # open the matplotlib.plot figure and set it to be 20 by 20
    plt.figure(figsize = (8,8))

    # turn of the axis labels
    plt.axis('off')

    # Draw the graph nodes
    nx.draw_networkx_nodes(G,pos,node_color=Colors,node_size = node_size)

    # Draw the graph edges
    nx.draw_networkx_edges(G,pos,width=Weights)

    #nx.draw_networkx_labels(G,pos,nx.get_node_attributes(G,'label'),font_size=10)

    # This opens the plot on your machine
    plt.show()

def BuildGraph(EdgeList,nodes_csv,Tol):
    maxWeight = float(max(EdgeList['Weight']))

    Weights = list(EdgeList['Weight'][EdgeList['Weight']>=Tol].values.flatten()/maxWeight)

    User1 = list(EdgeList['Name1'][EdgeList['Weight']>=Tol].values.flatten())
    User2 = list(EdgeList['Name2'][EdgeList['Weight']>=Tol].values.flatten())

    Attr = pd.read_csv(nodes_csv)

    del EdgeList
    EdgeList = zip(User1,User2,Weights)
    G = nx.Graph()
    nodes = list(set(User1).union(set(User2)))

    G.add_nodes_from(nodes)

    node_size = []
    Colors = []

    for node in G.nodes():
        node_size.extend([float(Attr.node_size[Attr.screen_name==node].values[0])])
        Colors.extend([Attr.color[Attr.screen_name==node].values[0]])

    del Attr

    G.add_weighted_edges_from(EdgeList)
    pos = nx.spring_layout(G)
    edgewidth = [d['weight'] for (u,v,d) in G.edges(data=True)]

    return G,pos,edgewidth,node_size,Colors

def SaveNetworkFig(G,pos,edgewidth,node_size,Colors,FigName):
    plt.figure(figsize=(9,9))
    plt.axis('off')

    nx.draw_networkx_nodes(G,pos,node_color=Colors,node_size = node_size)
    nx.draw_networkx_edges(G,pos,width=edgewidth)

    xpositions = []
    ypositions = []
    for node in G.nodes():
        xpositions.extend([list(pos[node])[0]])
        ypositions.extend([list(pos[node])[1]])
    xmin = min(xpositions)
    xmax = max(xpositions)
    ymin = min(ypositions)
    ymax = max(ypositions)
    plt.ylim((ymin-.01,ymax+.01))
    plt.xlim((xmin-.01,xmax+.01))

    plt.savefig(fname = FigName,bbox_inches='tight')





def SaveNetworkDrawing(EdgeList,Tol):
    print "Hello"
