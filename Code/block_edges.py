from collections import defaultdict
from math import log
from math import fsum
import numpy as np
import networkx as nx
import random

def IEED_remove_edges(nodes,edges,weights,k):
	no_of_edges = len(edges)
	edges = np.array(edges)
	row  = {}
	graph_matrix = {}
	for node in nodes:
		row[node] = 0
	for node in nodes:
		graph_matrix[node] = row.copy()
	def build_graph(edges):
		graph = defaultdict(list)
		# Loop to iterate over every edge of the graph
		for edge in edges:
			a, b = edge[0], edge[1]
			c = weights[(a,b)]
			# Creating the graph as adjacency list
			graph[a].append((b,c))
			graph[b].append((a,c))
			graph_matrix[a][b] = c
			graph_matrix[b][a] = c
		return graph
	Graph = build_graph(edges)
	influence = {}		# Dictionary of Influence of each edge
	W = {}			# Sum of weights
	def w_sum(vertex):
		nonlocal Graph
		sum = 0
		for element in Graph[vertex]:
			sum += element[1]
		return sum

	def inf(vertex):
		nonlocal Graph
		inf = 0
		for element in Graph[vertex]:
			inf += (element[1]/W[vertex])*log(element[1]/W[vertex])
		if len(Graph[vertex]) == 0:
			return 0
		inf *= -W[vertex]/len(Graph[vertex])
		return inf

	for vertex in nodes:			
		W[vertex] = w_sum(vertex)	# Sum of weights attached to each vertex
	for vertex in nodes:
		influence[vertex] = inf(vertex)		# Influence of each vertex
	def efficiency(edge):
		nonlocal Graph
		a,b = edge
		eff = weights[(edge[0],edge[1])]
		for i in Graph[a]:
			eff *= (1-graph_matrix[i[0]][b]*graph_matrix[a][i[0]])
		return eff

	A = []              # In the form of  [eff,inf1,inf2]
	for edge in edges:
		eff = efficiency(edge)
		A.append([eff,influence[edge[0]],influence[edge[1]]])
	A  = np.array(A)
	S = []
	for iterations in range(int(k*no_of_edges)):										# Normalised matrix N
		np.seterr(invalid='ignore')
		N = A/np.sum(A,axis = 0)
		N[np.isnan(N)] = 0
		x = np.ma.log(N)
		H_matrix = N*x.filled(0)*(-1/log(len(N)))
		H = np.sum(H_matrix,axis=0)

		alp = [(1-H[i])/(3-fsum(H)) for i in range(len(H))]			# List that contains the values of alpha 1, 2 and 3

		def crit_indx(alp):	
			critical = alp[0]*N[:,0]+alp[1]*N[:,1]+alp[2]*N[:,2]
			critical = critical.reshape(1,len(N))
			crit = np.argmax(critical, axis = 1)[0]
			return crit
		index = crit_indx(alp)
		S.append((edges[index][0],edges[index][1]))
		# Following code updates the Graph, edges and A
		A = np.delete(A,index,0)
		edges = np.delete(edges,index,0)

		a,b = S[-1]
		graph_matrix[a][b]=0
		graph_matrix[b][a]=0
		for i in range(len(Graph[a])):
			if Graph[a][i][0] == b:
				del Graph[a][i]
				break
		for i in range(len(Graph[b])):
			if Graph[b][i][0] == a:
				del Graph[b][i]
				break

		W[a]= w_sum(a)
		influence[a] = inf(a)
		W[b]= w_sum(b)
		influence[b] = inf(b)

		for i in range(len(edges)):
			if edges[i][0] == a:
				A[i][1] = influence[a]
				A[i][0] = efficiency(edges[i])
			elif edges[i][1] == a:
				A[i][2] = influence[a]
				A[i][0] = efficiency(edges[i])
			if edges[i][0] == b:
				A[i][1] = influence[b]
				A[i][0] = efficiency(edges[i])
			elif edges[i][1] == b:
				A[i][2] = influence[b]
				A[i][0] = efficiency(edges[i])
	output = []
	for edge in edges:
		output.append((edge[0],edge[1]))
	print ("Edges removed: ", len(S))
	return output


# Outputs a list of edges in random order
def RNDM(graph):
	edges = list(graph.edges)
	random.shuffle(edges)
	return (edges)

# Outputs a list of edges in increasing order of wt
def HWGT(graph):
	edges = list(graph.edges)
	output = sorted(edges,key = lambda x: graph[x[0]][x[1]]['weight'])
	return (output)

# Outputs a list of edges in increasing order of betweenness
def BTWN(graph):
	edges = list(graph.edges)
	bw = nx.edge_betweenness_centrality(graph,)
	output = sorted(edges,key= lambda x: bw[x])
	return output

# Outputs a list of edges in increasing order of weighted betweenness
def WBET(graph):
	edges = list(graph.edges)
	bw = nx.edge_betweenness_centrality(graph,weight = 'distance')
	output = sorted(edges,key= lambda x: bw[x])
	return output

# Outputs a list of edges in increasing order of highest degree
def HDEG(graph):
	edges = list(graph.edges)
	deg = nx.degree_centrality(graph)
	output = sorted(edges,key= lambda x: deg[x[0]]+deg[x[1]])
	return output

# Outputs a list of edges in increasing order of closeness
def CLO(graph):
	edges = list(graph.edges)
	deg = nx.closeness_centrality(graph,wf_improved= True)
	output = sorted(edges,key= lambda x: deg[x[0]]+deg[x[1]])
	return output

# Outputs a list of edges in increasing order of weighted closeness
def WCLO(graph):
	edges = list(graph.edges)
	deg = nx.closeness_centrality(graph, distance= 'distance',wf_improved= True)
	output = sorted(edges,key= lambda x: deg[x[0]]+deg[x[1]])
	return output

# Outputs a list of edges in increasing order of weighted degree
def WDEG(graph):
	edges = list(graph.edges)
	deg = {}
	for node in graph.nodes():
		deg[node] = 0
	for e in graph.edges():
		deg[e[0]] += graph[e[0]][e[1]]['weight']
		deg[e[1]] += graph[e[0]][e[1]]['weight']
	output = sorted(edges,key= lambda x: deg[x[0]]+deg[x[1]]-2*graph[x[0]][x[1]]['weight'])
	return output

# Outputs a list of edges in increasing order of pagerank centrality
def PGRK(graph):
	edges = list(graph.edges)
	pg_rnk = nx.pagerank(graph, alpha=0.9)
	output = sorted(edges,key= lambda x: pg_rnk[x[0]]+pg_rnk[x[1]])
	return output


# Removes k fraction of edges from the graph and outputs the resulting graph.
def rem_edges(graph,output,k):  # Input : graph, sorted list of edges, fraction of edges to be removed
	req = int(len(graph.edges)-int(k*len(graph.edges)))
	graph.remove_edges_from(output[req:])
	return graph

