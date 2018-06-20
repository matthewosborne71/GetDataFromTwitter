import MakeNetworks as MN
import pandas as pd

a = pd.read_csv(r"C:\\Users\\Matthew Osborne\\Documents\\python_code\\DoYouEvenLift\\LukeObrien\\RTEdgeList.csv")

G,p0,ew = MN.BuildGraph(a,1)
MN.SaveNetworkFig(G,p0,ew,r"C:\\Users\\Matthew Osborne\\Documents\\python_code\\DoYouEvenLift\\LukeObrien\\RTPics\\MinWeight"+str(1)+".png")
del G
del ew



stop = max(a.Weight)
for i in range(2,stop):
    G,p,ew = MN.BuildGraph(a,i)
    MN.SaveNetworkFig(G,p0,ew,r"C:\\Users\\Matthew Osborne\\Documents\\python_code\\DoYouEvenLift\\LukeObrien\\RTPics\\MinWeight"+str(i)+".png")
    del G
    del ew
    del p
    print str(i)
