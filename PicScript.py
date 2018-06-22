import MakeNetworks as MN
import pandas as pd

path = r"C:\\Users\\Matthew Osborne\\Documents\\python_code\\DoYouEvenLift\\NBA\\"


a = pd.read_csv(path + "RTEdgeList.csv")

G,p0,ew = MN.BuildGraph(a,1)
MN.SaveNetworkFig(G,p0,ew,path+"RTPics\\MinWeight"+str(1)+".png")
del G
del ew



stop = max(a.Weight)
for i in range(2,400):
    G,p,ew = MN.BuildGraph(a,i)
    MN.SaveNetworkFig(G,p0,ew,path+"RTPics\\MinWeight"+str(i)+".png")
    del G
    del ew
    del p
    print str(i)
