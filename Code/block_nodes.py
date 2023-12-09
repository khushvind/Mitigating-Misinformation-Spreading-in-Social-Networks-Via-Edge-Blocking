import networkx as nx
import numpy as np
import random

# Outputs a list of nodes in random order
def random_nodes(graph):
	nodes = list(graph.nodes())
	random.shuffle(nodes)
	return nodes

# Outputs a list of nodes in increasing order of degree
def highest_degree(graph):
	nodes = graph.nodes()
	deg = nx.degree_centrality(graph)
	output = sorted( nodes ,key = lambda x: deg[x])
	return output

# Outputs a list of nodes in increasing order of closeness centrality
def highest_closeness(graph):
	nodes = graph.nodes()
	deg = nx.closeness_centrality(graph,wf_improved= True)
	output = sorted( nodes ,key = lambda x: deg[x])
	return output

# Outputs a list of nodes in increasing order of betweenness centrality
def highest_betweenness(graph):
	nodes = graph.nodes()
	deg = nx.betweenness_centrality(graph)
	output = sorted( nodes ,key = lambda x: deg[x])
	return output

# Outputs a list of nodes in increasing order of eigenvector centrality
def highest_eignevector(graph):
	nodes = graph.nodes()
	deg = nx.eigenvector_centrality(graph)
	output = sorted( nodes ,key = lambda x: deg[x])
	return output

# Outputs a list of nodes in increasing order of weighted degree
def highest_wt_degree(graph):
	deg = {}
	for node in graph.nodes():
		deg[node] = 0
	for e in graph.edges():
		deg[e[0]] += graph[e[0]][e[1]]['weight']
		deg[e[1]] += graph[e[0]][e[1]]['weight']
	nodes = graph.nodes()
	output = sorted( nodes ,key = lambda x: deg[x])
	return output

# Outputs a list of nodes in increasing order of weighted closeness centrality
def highest_wt_closeness(graph):
	nodes = graph.nodes()
	deg = nx.closeness_centrality(graph, distance= 'distance',wf_improved= True)
	output = sorted( nodes ,key = lambda x: deg[x])
	return output

# Outputs a list of nodes in increasing order of weighted betweenness centrality
def highest_wt_betweenness(graph):
	nodes = graph.nodes()
	deg = nx.betweenness_centrality(graph, weight= 'distance')
	output = sorted( nodes ,key = lambda x: deg[x])
	return output

# Outputs a list of nodes in increasing order of weighted eigenvector centrality
def highest_wt_eigenvector(graph):
	nodes = graph.nodes()
	deg = nx.betweenness_centrality(graph, weight= 'weight')
	output = sorted( nodes ,key = lambda x: deg[x])
	return output

# Outputs a list of nodes in increasing order of two-hub-degree
def highest_two_hub_degree(graph):
	nodes = graph.nodes()
	deg = nx.degree_centrality(graph)
	n = len(nodes)-1
	for i in deg:
		deg[i] = round(deg[i]*n)
	two_hub_deg = {}
	for node in graph.nodes:
		# two_hub_deg[node] = deg[node]
		nearby = []
		nearby.extend(graph.neighbors(node))
		for first_neighour in graph.neighbors(node):
			nearby.extend(graph.neighbors(first_neighour))
		nearby = list(set(nearby))
		if node in nearby:
			nearby.remove(node)
		two_hub_deg[node] = len(nearby)
	output = sorted( nodes ,key = lambda x: two_hub_deg[x])
	return output

def greedy_alg(graph):
	active_graph = nx.Graph()
	for e in graph.edges:
		flip = np.random.random_sample()
		if flip < graph[e[0]][e[1]]['weight']:
			active_graph.add_edge(e[0],e[1])
	connected = nx.connected_components(active_graph)
	output = []
	for c in connected:
		output.append(c)
	return output

def highest_greedy_inf(graph,k,times=1):
	A = []
	nodes = graph.nodes()
	empty_dict = {}
	for n in graph.nodes:
		empty_dict[n] = 0
	component_list = []
	for i in range(times):
		component_list.append(greedy_alg(graph))
	for ran in range(int(k*len(graph.nodes))):
		inf_on_adding_v = empty_dict.copy()
		for i in range(times):
			component = component_list[i]
			node_component_map = {}
			component_activated = {}
			temp_inf = empty_dict.copy()
			component_idx = 0
			remaining = set(nodes)
			for c in component:
				remaining -= c
				component_activated[component_idx] = 0
				inf_in_c = len(c)
				for node in c:
					node_component_map[node] = component_idx
					temp_inf[node] += inf_in_c
				component_idx += 1
			for node in remaining:
				component_activated[component_idx] = 0
				node_component_map[node] = component_idx
				temp_inf[node] += 1
				component_idx += 1

			inf = 0
			for node in A:
				if not component_activated[node_component_map[node]]:
					inf += temp_inf[node]
					component_activated[node_component_map[node]] = 1
			for node in list(set(nodes)-set(A)):
				if not component_activated[node_component_map[node]]:
					added = inf+temp_inf[node]
				else:
					added = inf
				inf_on_adding_v[node] += added
		Keymax = max(zip(inf_on_adding_v.values(), inf_on_adding_v.keys()))[1]
		A.append(Keymax)
	A.reverse()
	return A

# Removes k fraction of nodes from the graph and outputs the resulting graph.
def rem_nodes(graph,output,k): # Input : graph, sorted list of nodes, fraction of nodes to be removed
	req = int(len(graph.nodes)-int(k*len(graph.nodes)))
	graph.remove_nodes_from(output[req:])
	return graph