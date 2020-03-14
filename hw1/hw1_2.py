!pip install snap-stanford
!pip install networkx
!wget "www-personal.umich.edu/~mejn/netdata/netscience.zip"
!unzip "netscience.zip"

import snap
import networkx as nx
import math

G5 = nx.read_gml("netscience.gml")
G5 = G5.to_undirected()
print(G5.nodes)
print(G5.edges)

featureMat = {}

def cosineSim(v1, v2):
  result = 0

  sizev1 = 0
  sizev2 = 0
  for i in range(len(v1)):
    sizev1 += (v1[i] * v1[i])
    sizev2 += (v2[i] * v2[i])

    result += v1[i] * v2[i]
  if sizev1==0 or sizev2==0:
    return 0
  result = result / (math.sqrt(sizev1) * math.sqrt(sizev2))
  return result

def findSim(nodeName, featureMat, Graph):
  simList = {}
  for node in Graph.nodes():
    simList[node] = cosineSim(featureMat[nodeName], featureMat[node])
  simList = {k: v for k, v in sorted(simList.items(), key=lambda item: item[1], reverse = True)}
  return simList


for (u, v, wt) in G5.edges(data=True):
  wt['value'] = 1

for node in G5.nodes():
  featureMat[node] = []
  featureMat[node] += [G5.degree[node]]
  tmpEgo = nx.ego_graph(G5, node)
  featureMat[node] += [tmpEgo.size()]
  totalEdges = G5.degree[node]
  for neiNode in G5[node]:
    totalEdges += G5.degree[neiNode]
  featureMat[node] += [totalEdges - (2*tmpEgo.size())]


huberManSim = findSim('HUBERMAN, B', featureMat, G5)

print("similarity for huberman is(sorted): %s"%(huberManSim))
print(featureMat)

#for (u, v, wt) in G5.edges.data('value'):
#  if wt < 0.5: print('(%s, %s, %.3f)' % (u, v, wt))
#    if wt < 0.5: print('(%s, %s, %.3f)' % (n, nbr, wt))

def recursiveMeanSum(Graph, featureMat):
  for node in Graph.nodes():
    features = featureMat[node]
    for i in range(len(features)):
      featureSum = 0
      for neiNode in Graph[node]:
        featureSum += featureMat[neiNode][i]
      if Graph.degree(node) == 0:
        featureMat[node] += [0]
        featureMat[node] += [0]
      else:
        featureMat[node] += [featureSum]
        featureMat[node] += [featureSum/Graph.degree(node)]
  return featureMat




featureMat = recursiveMeanSum(G5, featureMat)
print(featureMat)
huberManSim = findSim('HUBERMAN, B', featureMat, G5)
print(huberManSim)

import matplotlib.pyplot as plt

simWithHuber = []
for key, value in huberManSim.items():
  simWithHuber += [value]


n, bins, patches = plt.hist(simWithHuber, 20, density=1, alpha=0.8)
plt.title("similarity with Huberman by f")
plt.show()

print("\n")

print("\n\nwe want to compare structure of HUBERMAN, B subgraph with its nearest node that we calculate, KOCH, C: \n")
ego = nx.ego_graph(G5, "KOCH, C")
pos = nx.spring_layout(ego)
nx.draw(ego, pos, node_color='b', node_size=50, with_labels=True)
plt.title("KOCH, C ego graph")
plt.show()

ego = nx.ego_graph(G5, "HUBERMAN, B")
pos = nx.spring_layout(ego)
nx.draw(ego, pos, node_color='b', node_size=50, with_labels=True)
plt.title("HUBERMAN, B ego graph")
plt.show()

