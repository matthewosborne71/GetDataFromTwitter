# Make Networks
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def EdgeList(path,screen_namesSource,TweetFiles,Type,start,stop):
    if Type not in ["HT","RT","Ment"]:
        print "Sorry " + Type + " is not currently a supported EdgeList type."

    print "Creating EdgeList file..."
    f = open(path + Type + "EdgeList" + str(start) + "_" + str(stop) +
            ".csv","w+")
    f.write("Name1,Name2,Weight\n")


    print "Reading in the screen_names"
    a = pd.read_csv(path +  screen_namesSource)
    screen_names = a['screen_name']
    del a

    i = start
    for name1 in screen_names[start:stop]:
        print "Getting edges for " + str(name1)
        print i
        name1 = str(name1)
        DF = pd.read_csv(path + TweetFiles + name1 + "Retweets.csv")
        Set = set(DF['RTUser'].value_counts().index)
        del DF

        for name2 in screen_names[i+1:]:

            name2 = str(name2)

            tempDF = pd.read_csv(path + TweetFiles + name2 + "Retweets.csv")
            tempSet = set(tempDF['RTUser'].value_counts().index)
            del tempDF

            c = Set.intersection(tempSet)

            if bool(c) == True:
                f.write(str(name1) + "," + str(name2) + "," + str(len(c)) + "\n")

            del tempSet
            del c

        del Set
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

    #node_size = []
    #Colors = []
    #label = []
    #for node in G.nodes():
        #G.nodes[node]['color'] = Attr.color[Attr.screen_name==node].values[0]
        #G.nodes[node]['node_size'] = Attr.node_size[Attr.screen_name==node].values[0]
        #G.nodes[node]['label'] = Attr.Name[Attr.screen_name==node].values[0]
        #node_size.extend([float(Attr.node_size[Attr.screen_name==node].values[0])])
        #Colors.extend([Attr.color[Attr.screen_name==node].values[0]])
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
    nx.draw_networkx_nodes(G,pos,node_size = 5)

    # Draw the graph edges
    nx.draw_networkx_edges(G,pos,width=edgewidth)

    #nx.draw_networkx_labels(G,pos,nx.get_node_attributes(G,'label'),font_size=10)

    # This opens the plot on your machine
    plt.show()

def BuildGraph(EdgeList,Tol):
    #nodes_csv,,Label
    maxWeight = float(max(EdgeList['Weight']))

    Weights = list(EdgeList['Weight'][EdgeList['Weight']>=Tol].values.flatten()/maxWeight)

    User1 = list(EdgeList['Name1'][EdgeList['Weight']>=Tol].values.flatten())
    User2 = list(EdgeList['Name2'][EdgeList['Weight']>=Tol].values.flatten())

    # Attr = pd.read_csv(nodes_csv)
    # Attr['locate'] = "none"
    # for i in range(len(Attr)):
    #     Attr['locate'][i] = Attr['screen_name'][i].lower()
    # print Attr.head()

    del EdgeList
    EdgeList = zip(User1,User2,Weights)
    G = nx.Graph()
    nodes = list(set(User1).union(set(User2)))

    G.add_nodes_from(nodes)

    # node_size = []
    # Colors = []
    # labels = {}
    #
    # for node in G.nodes():
    #     node_size.extend([Attr['node_size'][Attr['locate']==node.lower()].values[0]])
    #     Colors.extend([Attr['color'][Attr['locate']==node.lower()].values[0]])
    #
    # if Label == "Yes":
    #     for node in G.nodes():
    #         labels[node] = node

    #del Attr

    G.add_weighted_edges_from(EdgeList)
    pos = nx.spring_layout(G)
    edgewidth = [d['weight'] for (u,v,d) in G.edges(data=True)]

    # if Label == "Yes":
    #     return G,pos,edgewidth#,node_size,Colors,labels
    #else:
    return G,pos,edgewidth#,node_size,Colors

def SaveNetworkFig(G,pos,edgewidth,FigName):
    #,node_size,Colors,FigName,Label,labels={}
    plt.figure(figsize=(9,9))
    plt.axis('off')

    nx.draw_networkx_nodes(G,pos,node_size=5)
    #node_color=Colors,node_size = node_size
    nx.draw_networkx_edges(G,pos,width=edgewidth)

    # if Label == "Yes":
    #     nx.draw_networkx_labels(G,pos,labels,font_size=10)

    xpositions = []
    ypositions = []
    for node in G.nodes():
        xpositions.extend([list(pos[node])[0]])
        ypositions.extend([list(pos[node])[1]])
    xmin = min(xpositions)
    xmax = max(xpositions)
    ymin = min(ypositions)
    ymax = max(ypositions)
    # if Label=="Yes":
    #     plt.ylim((ymin-.05,ymax+.05))
    #     plt.xlim((xmin-.05,xmax+.05))
    # else:
    plt.ylim((ymin-.01,ymax+.01))
    plt.xlim((xmin-.01,xmax+.01))

    plt.savefig(fname = FigName,bbox_inches='tight')


def NumConnected(G):
    num = nx.number_connected_components(G)
    return num

def SizeGiantComp(G):
    Gc = max(nx.connected_component_subgraphs(G),key=len)
    n = len(Gc.nodes())
    return n

def GetComponents(G):
    Comps = nx.connected_components(G)
    return Comps

def WhoRT(nodes):
    # read in nodes
    # output list of who they're RTing
    print "IN Beta"

class Component:
    # Every Component instance is initialized with a set of nodes, a type that
    # must be 'RT', 'HT', or 'Ment'
    def __init__(self,Nodes,Type,MinWeight,DataPath,TweetPath):
        self.Nodes = Nodes
        self.Type = Type
        self.MinWeight = MinWeight
        self.NumNodes = len(Nodes)
        self.DataPath = DataPath
        self.TweetPath = DataPath + TweetPath

    def  CommonRTs(self):
        NodeList = list(self.Nodes)
        TempDF = pd.read_csv(self.TweetPath + NodeList[0] + "Retweets.csv")
        CommonRTs = set(TempDF['RTUser'])
        del TempDF
        for node in NodeList[1:]:
            TempDF = pd.read_csv(self.TweetPath + node + "Retweets.csv")
            CommonRTs = CommonRTs.intersection(set(TempDF['RTUser']))
            del TempDF
        return CommonRTs

    def CommonHTs(self):
        NodeList = list(self.Nodes)
        TempDF = pd.read_csv(self.TweetPath + NodeList[0] + "Hashtags.csv")
        CommonHTs = set(TempDF['hashtag'])
        del TempDF
        for node in NodeList[1:]:
            TempDF = pd.read_csv(self.TweetPath + node + "Hashtags.csv")
            CommonHTs = CommonHTs.intersection(set(TempDF['hashtag']))
            del TempDF
        return CommonHTs

    def CommonMents(self):
        # mentionName
        NodeList = list(self.Nodes)
        TempDF = pd.read_csv(self.TweetPath + NodeList[0] + "Mentions.csv")
        CommonMents = set(TempDF['mentionName'])
        del TempDF
        for node in NodeList[1:]:
            TempDF = pd.read_csv(self.TweetPath + node + "Mentions.csv")
            CommonMents = CommonMents.intersection(set(TempDF['mentionName']))
            del TempDF
        return CommonMents

    def DrawComponent(self):
        a = pd.read_csv(self.DataPath+self.Type+"EdgeList.csv")
        Edgelist = a[a['Name1'].isin(self.Nodes) & a['Name2'].isin(self.Nodes)]
        Edgelist['Weight'] = Edgelist['Weight']/max(Edgelist['Weight'])
        del a


        G = nx.Graph()
        G.add_nodes_from(self.Nodes)

        Weights = list(Edgelist['Weight'].values.flatten())
        User1 = list(Edgelist['Name1'].values.flatten())
        User2 = list(Edgelist['Name2'].values.flatten())
        del Edgelist
        Edgelist = zip(User1,User2,Weights)

        G.add_weighted_edges_from(Edgelist)

        pos = nx.spring_layout(G)
        edgewidth = [d['weight'] for (u,v,d) in G.edges(data=True)]

        # open the matplotlib.plot figure and set it to be 20 by 20
        plt.figure(figsize = (8,8))

        # turn of the axis labels
        plt.axis('off')

        # Draw the graph nodes
        if self.NumNodes > 20:
            nx.draw_networkx_nodes(G,pos,node_size = 5)
        else:
            nx.draw_networkx_nodes(G,pos,node_size = 50)
            labels = {}
            for node in G.nodes():
                labels[node] = node
            nx.draw_networkx_labels(G,pos,labels,font_size=10)

        # Draw the graph edges
        nx.draw_networkx_edges(G,pos,width=edgewidth)

        #nx.draw_networkx_labels(G,pos,nx.get_node_attributes(G,'label'),font_size=10)

        # This opens the plot on your machine
        plt.show()
