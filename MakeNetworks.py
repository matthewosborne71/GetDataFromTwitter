###############################################################################
### MakeNetworks.py                                                         ###
### Matthew Osborne                                                         ###
### last updated: June 27, 2018                                             ###
###############################################################################
###############################################################################
# This file contains code to create networks using the Twitter data I've      #
# colleceted. Then I can analyze the components of said networks to search    #
# communities within the network.                                             #
###############################################################################

# Import the packages I will use throughout the code
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


# This function will read through my tweet files and construct an edgelist for a
# network based upon common features of tweets that have been sent.
def EdgeList(path,screen_namesSource,TweetFiles,Type,start,stop):

# Type must be HT, RT, or Ment
    if Type == "RT":
        FileType = "Retweets.csv"
        feature = 'RTUser'
    elif Type == "HT":
        FileType = "Hashtags.csv"
        feature = 'hashtag'
    elif Type == "Ment":
        FileType == "Mentions.csv"
        feature = 'mentionName'
    else:
        print "Sorry " + Type + " is not currently a supported EdgeList type."
# Create the Edgelist file
    print "Creating EdgeList file..."
    f = open(path + Type + "EdgeList" + str(start) + "_" + str(stop) +
            ".csv","w+")
    f.write("Name1,Name2,Weight\n")

# collect the screen_names for the nodes
    print "Reading in the screen_names"
    a = pd.read_csv(path +  screen_namesSource)
    screen_names = a['screen_name']
    del a

# Search through the tweet files to find the number of common Type data between
# the start and stop input.
    i = start
    for name1 in screen_names[start:stop]:
        print "Getting edges for " + str(name1)
        print i
        name1 = str(name1)
        # Read in the files for name1
        DF = pd.read_csv(path + TweetFiles + name1 + FileType)

        # Get the unique features
        Set = set(DF[feature].value_counts().index)
        del DF

        for name2 in screen_names[i+1:]:

            name2 = str(name2)

            # read in the data for name2 and grab the unique features
            tempDF = pd.read_csv(path + TweetFiles + name2 + FileType)
            tempSet = set(tempDF[feature].value_counts().index)
            del tempDF

            # Find the common features for name1 and name2
            c = Set.intersection(tempSet)

            if bool(c) == True:
                f.write(str(name1) + "," + str(name2) + "," + str(len(c)) + "\n")

            del tempSet
            del c

        del Set
        i=i+1

# Close the file since we're done
    print "All Done!"
    f.close()

# This function will take in an edgelist and show the network formed when
# considering the edges with weight that meet a certain tolerance level, Tol.
def ShowRTNetwork(EdgeList,nodes_csv,Tol):

# Find the largest edgeweight to scale the displayed edgewidth
    maxWeight = float(max(EdgeList['Weight']))

# Get edge weights from the edgelist
    Weights = list(EdgeList['Weight'][EdgeList['Weight']>=Tol].values.flatten()/maxWeight)

# Get the nodes
    User1 = list(EdgeList['Name1'][EdgeList['Weight']>=Tol].values.flatten())
    User2 = list(EdgeList['Name2'][EdgeList['Weight']>=Tol].values.flatten())

# This will be used if the edgelist has any attributes
#    Attr = pd.read_csv(nodes_csv)

# We're done using the edgelist and want to conserve memory
    del EdgeList

# Make the list of nodes that we will feed into the networkx object
    nodes = list(set(User1).union(set(User2)))

# Make the edgelist that we will feed into the networkx object
    EdgeList = zip(User1,User2,Weights)

# make the networkx graph object
    G = nx.Graph()

# add the nodes
    G.add_nodes_from(nodes)

# possible attribute functionality that will be implemented at a later date
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
    #del Attr

# add the weighted edges
    G.add_weighted_edges_from(EdgeList)

# get a position for the nodes
    pos = nx.spring_layout(G)

# give the edges a width for the graphic
    edgewidth = [d['weight'] for (u,v,d) in G.edges(data=True)]

# open the matplotlib.plot figure and set the size
    plt.figure(figsize = (8,8))

# turn off the axis labels
    plt.axis('off')

# Draw the graph nodes
    nx.draw_networkx_nodes(G,pos,node_size = 5)

# Draw the graph edges
    nx.draw_networkx_edges(G,pos,width=edgewidth)

# functionality to be worked on at a later date
    #nx.draw_networkx_labels(G,pos,nx.get_node_attributes(G,'label'),font_size=10)

    # This opens the plot on your machine
    # you'll need to close it manually
    plt.show()

# This code will build a networkx graph object using the input edgelist. The
# edges will all meet the input tolerance level, Tol
def BuildGraph(EdgeList,Tol):

# Find the largest weight
    maxWeight = float(max(EdgeList['Weight']))

# make a list of all the edgelists
    Weights = list(EdgeList['Weight'][EdgeList['Weight']>=Tol].values.flatten()/maxWeight)

# make a list of all the nodes for all edges
    User1 = list(EdgeList['Name1'][EdgeList['Weight']>=Tol].values.flatten())
    User2 = list(EdgeList['Name2'][EdgeList['Weight']>=Tol].values.flatten())

# functionality that will be looked at later
    # Attr = pd.read_csv(nodes_csv)
    # Attr['locate'] = "none"
    # for i in range(len(Attr)):
    #     Attr['locate'][i] = Attr['screen_name'][i].lower()
    # print Attr.head()

# We don't need the input edgelist anymore
    del EdgeList

# zip together the three lists we just made for our new edgelist
    EdgeList = zip(User1,User2,Weights)

# Make our graph object
    G = nx.Graph()

# make a list of nodes to input into the graph object
    nodes = list(set(User1).union(set(User2)))

# add the nodes
    G.add_nodes_from(nodes)

# functionality to be added at a later date
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

# add the edges now
    G.add_weighted_edges_from(EdgeList)

# get a position for the nodes
    pos = nx.spring_layout(G)

# Give the edges a width
    edgewidth = [d['weight'] for (u,v,d) in G.edges(data=True)]

# return the graph with positions for the nodes and weights for the edges
    return G,pos,edgewidth

# This function takes in a graph along with positions, edgewidths and then saves
# a plot of that graph with the name, FigName
def SaveNetworkFig(G,pos,edgewidth,FigName):

# Make the figure the graph will go on
    plt.figure(figsize=(9,9))

# turn off the axis
    plt.axis('off')

# draw the nodes and edges
    nx.draw_networkx_nodes(G,pos,node_size=5)
    nx.draw_networkx_edges(G,pos,width=edgewidth)

# This code allows us to set our axes tight on the graph
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

# Finally we save the figure on our machine!
    plt.savefig(fname = FigName,bbox_inches='tight')
    plt.close()

# Finds how many connected components a graph, G, has
def NumConnected(G):
    num = nx.number_connected_components(G)
    return num

# Finds the size of the giant component of the graph G
def SizeGiantComp(G):
    Gc = max(nx.connected_component_subgraphs(G),key=len)
    n = len(Gc.nodes())
    return n

# Returns the connected components of the graph G
def GetComponents(G):
    Comps = nx.connected_components(G)
    return Comps

# This class will help us better decipher the components that exist within a
# given graph.
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


# This function will return the top n accounts that have been retweeted by all
# of the nodes in the component. Note that this does not mean that every node in
# the component has retweeted these accounts, for instance one node may retweet
# a single account 3200 times. If Perc is True you will see what percentage of
# the total retweets that account represents. If NumAccount = True, you will see
# the total unique nodes that retweeted that account.
    def TopRTs(self,Perc=False,NumAccount=False,n=10):
        print "Finding the top " + str(n) + " retweeted accounts for " + str(self.NumNodes) +" nodes."
        print "This may take a while."
        RunningTally = []
        for node in self.Nodes:
            TempDF = pd.read_csv(self.TweetPath+str(node)+"Retweets.csv")
            TempCount = TempDF['RTUser'].value_counts()
            RTUsers = list(TempCount.index)
            RTCounts = list(TempCount.values)
            Append = zip(RTUsers,RTCounts)
            RunningTally.extend(Append)



        RunningTallyDF = pd.DataFrame(RunningTally,columns=['RTUser','TotalTimesRTed'])
        del RunningTally

        TopRTers = RunningTallyDF.groupby(['RTUser']).sum()
        if NumAccount:
            NumAccounts = RunningTallyDF['RTUser'].value_counts()
            NumAccounts = pd.DataFrame(NumAccounts.values,index=NumAccounts.index,columns=['ByNumNodes'])
        del RunningTallyDF

        if Perc:
            TopRTers['PercentageOfTotalRTs'] = (TopRTers['TotalTimesRTed']/sum(TopRTers.TotalTimesRTed))*100
            TopRTers['PercentageOfTotalRTs'] = map(lambda x:round(x,2),TopRTers['PercentageOfTotalRTs'])

        if NumAccount:
            TopRTers = pd.concat([TopRTers,NumAccounts],axis=1)

        print "These are the top " + str(n) + " accounts that have been"
        print "retweeted by the nodes in this component."
        TopRTers = TopRTers.sort_values(by='TotalTimesRTed',ascending=False)
        print TopRTers.head(n)

# Same function as TopRTs but for hashtags
    def TopHTs(self,Perc=False,NumAccount=False,n=10):
        print "Finding the top " + str(n) + " hashtags for " + str(self.NumNodes) +" nodes."
        print "This may take a while."
        RunningTally = []
        for node in self.Nodes:
            TempDF = pd.read_csv(self.TweetPath+str(node)+"Hashtags.csv")
            TempCount = TempDF['hashtag'].value_counts()
            HTs = list(TempCount.index)
            HTCounts = list(TempCount.values)
            Append = zip(HTs,HTCounts)
            RunningTally.extend(Append)

        RunningTallyDF = pd.DataFrame(RunningTally,columns=['Hashtag','TotalTimesUsed'])
        del RunningTally

        TopHTs = RunningTallyDF.groupby(['Hashtag']).sum()
        if NumAccount:
            NumAccounts = RunningTallyDF['Hashtag'].value_counts()
            NumAccounts = pd.DataFrame(NumAccounts.values,index=NumAccounts.index,columns=['ByNumNodes'])
        del RunningTallyDF

        if Perc:
            TopHTs['PercentageOfTotalHTs'] = (TopHTs['TotalTimesUsed']/sum(TopHTs.TotalTimesUsed))*100
            TopHTs['PercentageOfTotalHTs'] = map(lambda x:round(x,2),TopHTs['PercentageOfTotalHTs'])

        if NumAccount:
            TopHTs = pd.concat([TopHTs,NumAccounts],axis=1)

        TopHTs = TopHTs.sort_values(by='TotalTimesUsed',ascending=False)

        print "These are the top " + str(n) + " hashtags that have been"
        print "used by the nodes in this component."
        print TopHTs.head(n)

# Same as TopRTs but for mentions
    def TopMents(self,Perc=False,NumAccount=False,n=10):
        print "Finding the top " + str(n) + " mentions for " + str(self.NumNodes) +" nodes."
        print "This may take a while."
        RunningTally = []
        for node in self.Nodes:
            TempDF = pd.read_csv(self.TweetPath+str(node)+"Mentions.csv")
            TempCount = TempDF['mentionName'].value_counts()
            Ments = list(TempCount.index)
            MentCounts = list(TempCount.values)
            Append = zip(Ments,MentCounts)
            RunningTally.extend(Append)

        RunningTallyDF = pd.DataFrame(RunningTally,columns=['Mention','TotalTimesUsed'])
        if NumAccount:
            NumAccounts = RunningTallyDF['Mention'].value_counts()
            NumAccounts = pd.DataFrame(NumAccounts.values,index=NumAccounts.index,columns=['ByNumNodes'])
        del RunningTally

        TopMents = RunningTallyDF.groupby(['Mention']).sum()
        del RunningTallyDF

        if Perc:
            TopMents['PercentageOfTotalMents'] = (TopMents['TotalTimesUsed']/sum(TopMents.TotalTimesUsed))*100
            TopMents['PercentageOfTotalMents'] = map(lambda x:round(x,2),TopMents['PercentageOfTotalMents'])

        if NumAccount:
            TopMents = pd.concat([TopMents,NumAccounts],axis=1)

        TopMents = TopMents.sort_values(by='TotalTimesUsed',ascending=False)

        print "These are the top " + str(n) + " mentions that have been"
        print "made by the nodes in this component."
        print TopMents.head(n)

# This function prints a list of the n accounts that have been retweeted by the
# most unique nodes in descending order. For example if an account has a value
# of 300 that means 300 unique nodes have retweeted that account at least once.
    def NumNodesRTing(self,n=10):
        print "Calculating for " + str(self.NumNodes) + " nodes."
        print "This could take a bit."

        RunningTally = []
        for node in self.Nodes:
            TempDF = pd.read_csv(self.TweetPath+str(node)+"Retweets.csv")
            TempCount = TempDF['RTUser'].value_counts()
            RTUsers = list(TempCount.index)
            RunningTally.extend(RTUsers)

        RunningTallyDF = pd.DataFrame(RunningTally,columns = ['RTUser'])
        del RunningTally

        NumNodes = RunningTallyDF['RTUser'].value_counts()

        NumNodesDF = pd.DataFrame(NumNodes.values,index=NumNodes.index,columns=['NumAccountsThatRTed'])
        del NumNodes

        print "These " + str(n) + " accounts have been retweeted by this"
        print "component. The next column tells you how many nodes in the"
        print "component have retweeted that account."
        print NumNodesDF.head(n)

# This function is the same as NumNodesRTing but for hashtags.
    def NumNodesHTing(self,n):
        print "Calculating for " + str(self.NumNodes) + " nodes."
        print "This could take a bit."

        RunningTally = []
        for node in self.Nodes:
            TempDF = pd.read_csv(self.TweetPath+str(node)+"Hashtags.csv")
            TempCount = TempDF['hashtag'].value_counts()
            HTs = list(TempCount.index)
            RunningTally.extend(HTs)

        RunningTallyDF = pd.DataFrame(RunningTally,columns = ['hashtag'])
        del RunningTally

        NumNodes = RunningTallyDF['hashtag'].value_counts()

        NumNodesDF = pd.DataFrame(NumNodes.values,index=NumNodes.index,columns=['NumAccountsThatUsed'])
        del NumNodes

        print "These " + str(n) + " hashtags have been tweeted by this"
        print "component. The next column tells you how many nodes in the"
        print "component have used that hashtag."
        print NumNodesDF.head(n)

# This function is the same as NumNodesRTing but for mentions.
    def NumNodesMenting(self,n=10):
        print "Calculating for " + str(self.NumNodes) + " nodes."
        print "This could take a bit."

        RunningTally = []
        for node in self.Nodes:
            TempDF = pd.read_csv(self.TweetPath+str(node)+"Mentions.csv")
            TempCount = TempDF['hashtag'].value_counts()
            Ments = list(TempCount.index)
            RunningTally.extend(Ments)

        RunningTallyDF = pd.DataFrame(RunningTally,columns = ['mentionName'])
        del RunningTally

        NumNodes = RunningTallyDF['mentionName'].value_counts()

        NumNodesDF = pd.DataFrame(NumNodes.values,index=NumNodes.index,columns=['NumAccountsThatUsed'])
        del NumNodes

        print "These " + str(n) + " mentions have been tweeted by this"
        print "component. The next column tells you how many nodes in the"
        print "component have made that mention."
        print NumNodesDF.head(n)

# This function returns a list of the accounts that have been retweeted by EVERY
# node in the component.
    def  CommonRTs(self):
        NodeList = list(self.Nodes)
        TempDF = pd.read_csv(self.TweetPath + str(NodeList[0]) + "Retweets.csv")
        CommonRTs = set(TempDF['RTUser'])
        del TempDF
        for node in NodeList[1:]:
            TempDF = pd.read_csv(self.TweetPath + str(node) + "Retweets.csv")
            CommonRTs = CommonRTs.intersection(set(TempDF['RTUser']))
            del TempDF
        return CommonRTs

# Same as CommonRTs but for hashtags.
    def CommonHTs(self):
        NodeList = list(self.Nodes)
        TempDF = pd.read_csv(self.TweetPath + str(NodeList[0]) + "Hashtags.csv")
        CommonHTs = set(TempDF['hashtag'])
        del TempDF
        for node in NodeList[1:]:
            TempDF = pd.read_csv(self.TweetPath + str(node) + "Hashtags.csv")
            CommonHTs = CommonHTs.intersection(set(TempDF['hashtag']))
            del TempDF
        return CommonHTs

# Same as CommonRTs but for mentions.
    def CommonMents(self):
        # mentionName
        NodeList = list(self.Nodes)
        TempDF = pd.read_csv(self.TweetPath + str(NodeList[0]) + "Mentions.csv")
        CommonMents = set(TempDF['mentionName'])
        del TempDF
        for node in NodeList[1:]:
            TempDF = pd.read_csv(self.TweetPath + str(node) + "Mentions.csv")
            CommonMents = CommonMents.intersection(set(TempDF['mentionName']))
            del TempDF
        return CommonMents

# This function will draw the component and show it to you. If there are less
# than 20 nodes in the component the nodes will be labeled. You will need to
# manually close the figure to do more in your console.
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

def DrawWithComponent(G,pos,ew,Components):

# Make the figure the graph will go on
    plt.figure(figsize=(9,9))

# turn off the axis
    plt.axis('off')

    NodeColors = []
    NumComp = len(Components)
    CMap = plt.cm.get_cmap('hsv',2*NumComp)
    # Add colors


    # for node in G.nodes():
    #     for i in range(len(Components)):
    #         if node in Components[i].Nodes:
    #             NodeColors.extend([CMap(2*i)])
    #
    #
    # nx.draw_networkx_nodes(G,pos,node_size=5,node_color = NodeColors)

# draw the nodes and edges
    for i in range(len(Components)):
        nx.draw_networkx_nodes(G,pos,nodelist = list(Components[i].Nodes),node_size=5,node_color = CMap(2*i),label = "Component " + str(i))


    for node in G.nodes():
        for i in range(len(Components)):
            if node in Components[i].Nodes:
                NodeColors.extend([CMap(2*i)])


    nx.draw_networkx_nodes(G,pos,node_size=5,node_color = NodeColors)
    nx.draw_networkx_edges(G,pos,width=ew)

# This code allows us to set our axes tight on the graph
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

    plt.legend(loc='best')

    plt.show()

def GetRTed(path,Profiles,TweetFiles,kind):
    RunningTally = []
    nodes = list(Profiles[kind])
    for node in nodes:
        TempDF = pd.read_csv(path+TweetFiles+str(node)+"Retweets.csv")
        TempCount = TempDF['RTUser'].value_counts()
        RTUsers = list(TempCount.index)
        RTCounts = list(TempCount.values)
        Append = zip(RTUsers,RTCounts)
        RunningTally.extend(Append)



    RunningTallyDF = pd.DataFrame(RunningTally,columns=['RTUser','TotalTimesRTed'])
    del RunningTally

    TopRTers = RunningTallyDF.groupby(['RTUser']).sum().sort_values('TotalTimesRTed',ascending=False)
    TotalRTs = sum(TopRTers['TotalTimesRTed'])
    TopRTers['Perc'] = TopRTers['TotalTimesRTed']/TotalRTs

    return TopRTers
