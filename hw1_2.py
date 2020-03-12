!pip install snap-stanford
!pip install networkx
!wget "www-personal.umich.edu/~mejn/netdata/netscience.zip"
!unzip "netscience.zip"

import snap
import networkx as nx

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
  
  result = result / (math.sqrt(sizev1) * math.sqrt(sizev2))
  return result


for (u, v, wt) in G5.edges(data=True):
  wt['value'] = 1

print(G5.degree['YAN, G'])
for node in G5.nodes():
  featureMat[node] = []
  featureMat[node] += [G5.degree[node]]
  tmpEgo = nx.ego_graph(G5, node)
  featureMat[node] += [tmpEgo.size()]
  totalEdges = G5.degree[node]
  for neiNode in G5[node]:
    totalEdges += G5.degree[neiNode]
  featureMat[node] += [totalEdges - (2*tmpEgo.size())]


huberManSim = {}
for node in G5.node():
  huberManSim[node] = cosineSim(featureMat['HUBERMAN, B'], featureMat[node])


print(featureMat)
print(huberManSim)
#for (u, v, wt) in G5.edges.data('value'):
#  if wt < 0.5: print('(%s, %s, %.3f)' % (u, v, wt))
#    if wt < 0.5: print('(%s, %s, %.3f)' % (n, nbr, wt))
