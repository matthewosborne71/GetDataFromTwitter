import MakeNetworks as MN
import pandas as pd

path = r"C:\\Users\\Matthew Osborne\\Documents\\python_code\\DoYouEvenLift\\WednesdayWisdom\\"


a = pd.read_csv(path + "RTEdgeList.csv")
NumConnected = []
SizeConnected = []


stop = max(a.Weight)
for i in range(1,stop):
    G,p,ew = MN.BuildGraph(a,i)
    NumConnected.extend([MN.NumConnected(G)])
    SizeConnected.extend([MN.SizeGiantComp(G)])

    del G
    del ew
    del p
    print str(i)

NumConnected = pd.DataFrame(NumConnected,columns=['NumConnectedComponents'])
NumConnected['MinWeight'] = 0
for i in range(1,stop):
    NumConnected['MinWeight'][i-1] = i

NumConnected['GiantSize'] = SizeConnected
NumConnected = NumConnected[['MinWeight','NumConnectedComponents','GiantSize']]

NumConnected.to_csv(path+"NumConnected.csv",index=False)
