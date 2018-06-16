# Make Networks
import pandas as pd
import DataPaths as DP
import networkx as nx
import matplotlib.pyplot as plt

path = DP.GetPaths()


def RTEdgeList(screen_namesSource,TweetFiles,EListloc):
    print "Creating EdgeList file..."
    f = open(path+EListloc+"RTEdgeList.csv","w+")
    f.write("Name1,Name2,Weight\n")


    print "Reading in the screen_names"
    a = pd.read_csv(path +  screen_namesSource)
    screen_names = a['screen_name']
    del a


    i = 0
    for name1 in screen_names:
        print "Getting edges for " + name1
        RTDF = pd.read_csv(path + TweetFiles + name1 + "Retweets.csv")
        RTset = set(RTDF['RTUser'].value_counts().index)
        del RTDF

        print i
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

    print "All Done!"
    f.close()

def RTNetwork(EdgeList,Tol):
    maxWeight = float(max(EdgeList['Weight']))

    Weights = list(EdgeList['Weight'][EdgeList['Weight']>=Tol].values.flatten()/maxWeight)

    User1 = list(EdgeList['Name1'][EdgeList['Weight']>=Tol].values.flatten())
    User2 = list(EdgeList['Name2'][EdgeList['Weight']>=Tol].values.flatten())

    del EdgeList
    EdgeList = zip(User1,User2,Weights)
    G = nx.Graph()
    nodes = list(set(User1).union(set(User2)))
    G.add_nodes_from(nodes)
    G.add_weighted_edges_from(EdgeList)
    pos = nx.spring_layout(G)
    edgewidth = [d['weight'] for (u,v,d) in G.edges(data=True)]

    # open the matplotlib.plot figure and set it to be 20 by 20
    plt.figure(figsize = (8,8))

    # turn of the axis labels
    plt.axis('off')

    # Draw the graph nodes
    nx.draw_networkx_nodes(G,pos,node_size=10)

    # Draw the graph edges
    nx.draw_networkx_edges(G,pos,width=Weights)

    # This opens the plot on your machine
    plt.show()
