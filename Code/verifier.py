import random
import numpy as np
import networkx as nx

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

# Outputs a list of nodes in increasing order of closeness
def highest_closeness(graph):
	nodes = graph.nodes()
	deg = nx.closeness_centrality(graph,wf_improved= True)
	output = sorted( nodes ,key = lambda x: deg[x])
	return output

# Outputs a list of nodes in increasing order of betweenness
def highest_betweenness(graph):
	nodes = graph.nodes()
	deg = nx.betweenness_centrality(graph)
	output = sorted( nodes ,key = lambda x: deg[x])
	return output

# Outputs a list of nodes in increasing order of eigenvector centrality
def highest_eigenvector(graph):
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

# Outputs a list of nodes in increasing order of weighted closeness
def highest_wt_closeness(graph):
	nodes = graph.nodes()
	deg = nx.closeness_centrality(graph, distance= 'distance',wf_improved= True)
	output = sorted( nodes ,key = lambda x: deg[x])
	return output

# Outputs a list of nodes in increasing order of weighted betweenness
def highest_wt_betweenness(graph):
	nodes = graph.nodes()
	deg = nx.betweenness_centrality(graph, weight= 'distance')
	output = sorted( nodes ,key = lambda x: deg[x])
	return output

# Outputs a list of nodes in increasing order of weighted eigenvector
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

# Greedy Algo
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

# Outputs a list of nodes in increasing order of greedy algo
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
	to_be_added = list(set(nodes)-set(A))
	for extra in to_be_added:
		A.append(extra)
	A.reverse()
	return A    


def hybrid_algo(graph,comm,deg,clo,bet,k):
	nodes = graph.nodes()
	random.shuffle(comm)
	comm_s = comm[0: int(len(nodes)*k)]
	A = set(comm_s)
	B = set(nodes)
	not_comm = list(B.difference(A))
	random.shuffle(not_comm)
	comm_s.extend(not_comm)
	COM = {}
	for i in range(len(nodes)):
		COM[comm_s[i]] = i
	output = sorted( nodes ,key = lambda x: (deg[x]+COM[x]+clo[x]+bet[x]),reverse= True)
	return output

def hybrid_algo_1(graph):
	nodes = graph.nodes()
	DEG = highest_degree(graph)
	DEG_map = {}
	for i in range(1,len(nodes)+1):
		DEG_map[DEG[-i]] = i
	CLO = highest_closeness(graph)
	CLO_map = {}
	for i in range(1,len(nodes)+1):
		CLO_map[CLO[-i]] = i
	BET = highest_betweenness(graph)
	BET_map = {}
	for i in range(1,len(nodes)+1):
		BET_map[BET[-i]] = i
	output = sorted( nodes ,key = lambda x: (DEG_map[x]+CLO_map[x]+BET_map[x]),reverse= True)
	return output
	

# Assigns the verifiers and seeds to the network
def initialise_v_s(graph, type,k, init_rate,extra = None):
	req_verifier = int(k*len(graph.nodes))
	req_seeds = int(init_rate*len(graph.nodes))
	if type == 'random':
		node_list = random_nodes(graph)
	elif type == 'degree':
		node_list = highest_degree(graph)
	elif type == 'closeness':
		node_list = highest_closeness(graph)
	elif type == 'betweenness':
		node_list = highest_betweenness(graph)
	elif type == 'eigenvector':
		node_list = highest_eigenvector(graph)
	elif type == 'wt_degree':
		node_list = highest_wt_degree(graph)
	elif type == 'wt_closeness':
		node_list = highest_wt_closeness(graph)
	elif type == 'wt_betweenness':
		node_list = highest_wt_betweenness(graph)
	elif type == 'wt_eigenvector':
		node_list = highest_wt_eigenvector(graph)
	elif type == 'two_hub_deg':
		node_list = highest_two_hub_degree(graph)
	elif type == 'greedy_inf':
		node_list = highest_greedy_inf(graph)
	elif type == 'hybrid_algo_1':
		node_list = hybrid_algo_1(graph)
	elif type == 'hybrid_algo':
		node_list = hybrid_algo(graph,extra[0],extra[1],extra[2],extra[3],k)
	verifiers = node_list[-req_verifier:]
	possible_seeds = node_list[:-req_verifier]
	np.random.shuffle(possible_seeds)
	seeds = possible_seeds[-req_seeds:]
	return verifiers,seeds

# Assigns verifiers to the graph
def assign_v(graph,verifier):
	v = {}
	for node in graph.nodes:
		v[node] = 0
	for node in verifier:
		v[node] = 1
	for node in graph.nodes:
		graph.nodes[node]["verifier"] = v[node]
	return graph

# Assigns seeds to the graph
def assign_s(graph,possible_seeds,init_rate):
	req_seeds = int(init_rate*(len(graph.nodes)))
	random.shuffle(possible_seeds)
	seeds = possible_seeds[-req_seeds:]
	s = {}
	for node in graph.nodes:
		s[node] = 0
	for node in seeds:
		s[node] = 1
	for node in graph.nodes:
		graph.nodes[node]['seed'] = s[node]
	return graph