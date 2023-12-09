from networkx.algorithms import community
import networkx as nx
import random

# Detects the communities for graph with resolution factor = res and returns the communities found
def detect_communities(graph,res):
	comms = community.louvain_communities(graph, weight = None, resolution = res)
	return comms


# Returns the 'connecting_edges': edges joining different communities, community_edges: edges which lie inside communities, nodes: nodes which are endpoints of connecting edges
def connecting_edges(communities,graph):
	node_community_map = {}
	for i in range(len(communities)):
		for node in communities[i]:
			node_community_map[node] = i
	connecting_edges = []
	community_edges = []
	nodes = []
	for edge in graph.edges:
		a,b = edge
		if node_community_map[a] != node_community_map[b]:
			connecting_edges.append(edge)
			nodes.append(a)
			nodes.append(b)
		else:
			community_edges.append(edge)
	nodes = list(set(nodes))
	return connecting_edges,community_edges,nodes       

# Returns graph after removing the 'connecting_edges' from it
def graph_after_rem_edges(connecting_edges,graph):
	graph.remove_edges_from(connecting_edges)
	return graph

# Returns graph after removing the nodes of 'connecting_edges' from it 
def graph_after_rem_nodes(connecting_edges, graph, k ):
	# Iteratively removes nodes based on highest value overlap
	graph_conn = nx.Graph(connecting_edges)
	deg = nx.degree_centrality(graph_conn)
	n = len(graph_conn.nodes)-1
	for i in deg:
		deg[i] = round(deg[i]*n)
	nodes_rem = []
	remaining = 0 
	for i in range(k):
		key_max = max(zip(deg.values(), deg.keys()))[1] 
		# for the case when overlap becomes zero
		if deg[key_max] == 0:
			remaining = k-i
			break 
		nodes_rem.append(key_max)
		for n in graph_conn.neighbors(key_max):
			deg[n] -= 1
		a = deg[key_max]
		graph_conn.remove_node(key_max)
		del deg[key_max]
	print ('Max overlap at end',a)
	print ('Min overlap at end',min(deg.values()))
	print (graph_conn)
	print (graph)
	graph.remove_nodes_from(nodes_rem)
	if remaining > 0:
		deg = nx.degree_centrality(graph)
		nodes = graph.nodes()
		output = sorted( nodes ,key = lambda x: deg[x])
		graph.remove_nodes_from(output[-remaining:])
	print (graph)
	return graph

# Returns graph after assigning nodes of 'connecting_edges' as verifiers
def graph_after_assigning_verifier(connecting_edges, graph, k ):
	# Assigns verifier to nodes
	graph_conn = nx.Graph(connecting_edges)
	deg = nx.degree_centrality(graph_conn)
	n = len(graph_conn.nodes)-1
	for i in deg:
		deg[i] = round(deg[i]*n)
	nodes_ver = []
	remaining = 0
	for i in range(k):
		key_max = max(zip(deg.values(), deg.keys()))[1]  
		if deg[key_max] == 0:
			remaining = k-i
			break 
		nodes_ver.append(key_max)
		for n in graph_conn.neighbors(key_max):
			deg[n] -= 1
		graph_conn.remove_node(key_max)
		del deg[key_max]

	if remaining > 0:
		graph_temp = graph.copy()
		graph_temp.remove_nodes_from(nodes_ver)
		print (graph_temp)
		deg = nx.degree_centrality(graph_temp)
		nodes = graph_temp.nodes()
		output = sorted( nodes ,key = lambda x: deg[x])
		nodes_ver.extend(output[-remaining:])
	v = {}
	for node in graph.nodes:
		v[node] = 0
	for node in nodes_ver:
		v[node] = 1
	for node in graph.nodes:
		graph.nodes[node]["verifier"] = v[node]
	return graph,nodes_ver

# Returns graph after assigning seeds to it
def graph_after_assigning_seeds(not_possible_seeds,graph,init_rate):
	g_temp = graph.copy()
	g_temp.remove_nodes_from(not_possible_seeds)
	possible_seeds = list(g_temp.nodes())
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