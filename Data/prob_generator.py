# Run this file for generating the Jaccard-Index weights for the edges
# Change the name of source file and new file name according to your need
source_file = "Facebook"
new_file = "edges_facebook"

from random import randint
from collections import defaultdict
import numpy as np
import networkx as nx
def weights(edges):
	graph = defaultdict(list)
	# Loop to iterate over every edge of the graph
	for edge in edges:
		a, b = edge[0], edge[1]
		# Creating the graph as adjacency list
		graph[a].append(b)
		graph[b].append(a)
	weight = {}
	for edge in edges:
		a = graph[edge[0]] + [edge[0]]
		b = graph[edge[1]] + [edge[1]]
		c = [x for x in a if x in b]
		c = list(set(c))
		weight[edge] = len(c)/len(list(set(a+b)))
	return weight


print ("Initiating Edges")
edges = []
file = open(source_file+'.txt','r')
file2 = open(new_file+'.txt','w')
while True:
	t=file.readline()
	if not t:
		break
	a,b= list(map(int,t.split(' ')))
	if a==b:
		pass
	else:
		edges.append((a,b))
print (len(edges))
g = nx.Graph(edges)
print ("Directed: ",nx.is_directed(g))
print (nx.average_clustering(g))
print (len(g.edges)*2/len(g.nodes))
print ("Now Weights")
print (len(g.nodes))
print (len(g.edges))
edges = list(g.edges())
weight = weights(edges)
for edge in edges:	
	a,b = edge
	# max_wt = max(weight.values())
	file2.write(str(a)+'\t'+str(b)+"\t"+ str(weight[edge])+'\t'+'\n')
	# file2.write(str(a)+'\t'+str(b)+"\t"+ str(randint(1,10)/100)+'\t'+'\n')
print ('Done') 