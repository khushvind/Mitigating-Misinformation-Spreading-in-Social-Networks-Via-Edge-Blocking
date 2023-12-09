from collections import defaultdict

# Assigns weights to edges based on Jaccard Index
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
		weight[edge] = len(c)/len(list(set(a+b)))
	return weight

# Loads the data from path
def data_load(path):
	'''Load data from path
	Args: 
		path (str): path to data files;
	'''
	nodes = []
	edges = []
	weights = {}
	file = open(path)
	for line in file:
		source, target, prob = list(line.split())
		nodes.append(int(source))
		nodes.append(int(target))
		edges.append((int(source), int(target)))
		weights[(int(source), int(target))] = float(prob)
		weights[(int(target), int(source))] = float(prob)
	nodes = list(set(nodes))
	num_nodes = len(nodes)
	num_edges = len(edges)
	print('Number of Nodes: {}'.format(num_nodes))
	print('Number of Edges: {}'.format(num_edges))
	return nodes, edges, weights