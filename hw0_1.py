!pip install snap-stanford
!wget "http://snap.stanford.edu/data/wiki-Vote.txt.gz"
!gunzip  "/content/wiki-Vote.txt.gz"
!rm "/content/wiki-Vote.txt.gz"

import snap
import matplotlib.pyplot as plt
import numpy as np
import math

def LSRegression():
    x_np = np.array([])
    y_np = np.array([])
    ctr = 0
    for line in open('/content/outDeg.example.tab', 'r'):
        if ctr > 4:
            values = [int(s) for s in line.split()]
            x_np = np.append(x_np, [math.log(values[0])])
            y_np = np.append(y_np, [math.log(values[1])])
        else:
            ctr += 1
    p = np.polyfit(x_np, y_np, 1)
    print("regression on log-log scale with degree=1 is: %s"% (p))


def outDistPlot(graph):
    snap.PlotOutDegDistr(graph, "example", "Directed graph - out-degree Distribution")
    X, Y = [], []
    ctr = 0
    for line in open('/content/outDeg.example.tab', 'r'):
        if ctr > 3:
            values = [int(s) for s in line.split()]
            X.append(values[0])
            Y.append(values[1])
        else:
            ctr += 1

    plt.plot(X, Y)
    plt.title("dist of outDeg of nodes")

    plt.show()

if __name__ == '__main__':
    G = snap.LoadEdgeList(snap.PNGraph, "wiki-Vote.txt", 0, 1)

    print("nodes: %d, edges: %d" % (G.GetNodes(), G.GetEdges()))
    print("num of self directed egdes: %d" % (snap.CntSelfEdges(G)))
    print("num of directed edges: %d" % (snap.CntUniqDirEdges(G)))

    nodeOutDegZero = 0
    for node in G.Nodes():
        if node.GetOutDeg() == 0:
            nodeOutDegZero += 1
    print("number of nodes with zero out degree: %d" % nodeOutDegZero)


    '''for NI in G.Nodes():
      if G.IsEdge(NI.GetId(),NI.GetId()):
        print("%d"% (NI.GetId()))'''

    outDistPlot(G)
    LSRegression()

