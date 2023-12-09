import numpy as np
import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep
import random

# Returns a list of nodes arranged randomly
def random_nodes(graph):
	nodes = list(graph.nodes())
	random.shuffle(nodes)
	return nodes

# Selects 'init_rate' nodes as sources of misinformation
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

def influence_count_multiple(graph,init_rate,times):
    g =  assign_s(graph.copy(), random_nodes(graph),init_rate)
    affected = 0
    for time in range(times):
        affected += Independent_Cascade_Model(g)
    return affected/times

# ICM   
def Independent_Cascade_Model(graph):
    ''' Calculate influent result
    Args:
        1: intermediate_red
        2: red
        3: orange
    Return:
        final_actived_node (list): list of influent nodes;
    '''
    
    inactive_nodes = []
    active_nodes = []
    nodes_status = {}

    for n in graph.nodes: 
        if graph.nodes[n]['seed'] == 1:
            active_nodes.append(n)
        else:
            inactive_nodes.append(n)

    for node in inactive_nodes:
        nodes_status[node] = 0
    for node in active_nodes:
        nodes_status[node] = 2

    while(active_nodes):
        new_actived_nodes = []
        for a in active_nodes: 
            for b in graph.neighbors(a):
                if nodes_status[b] == 0:
                    p = graph[a][b]['weight']
                    flip = np.random.random_sample()
                    if flip <=p:
                        new_actived_nodes.append(b)
                        nodes_status[b] = 1
        for node in active_nodes:
            nodes_status[node] = 3
        for node in new_actived_nodes:
            nodes_status[node] = 2
        active_nodes = new_actived_nodes

    final_actived_node = 0
    for node in graph.nodes:
        if nodes_status[node] == 3:
            final_actived_node += 1
    return final_actived_node   

# ICM For Verifier Method
def influence_count_verifier(graph):
    ''' Calculate influent result
    Args:
        1: intermediate
        2: red
        3: orange
        4: green
        5: light green
    Return:
        final_actived_node (list): list of influent nodes;
    '''
    verifiers = nx.get_node_attributes(graph, "verifier")
    inactive_nodes = []
    active_nodes = []
    truth_active_nodes = []
    nodes_status = {}

    for n in graph.nodes: 
        if graph.nodes[n]['seed'] == 1:
            active_nodes.append(n)
        else:
            inactive_nodes.append(n)

    for node in inactive_nodes:
        nodes_status[node] = 0
    for node in active_nodes:
        nodes_status[node] = 2

    while(active_nodes or truth_active_nodes):
        new_actived_nodes = []
        new_truth_actived_nodes = []
        for a in truth_active_nodes:
            for b in graph.neighbors(a):
                if nodes_status[b] == 0:
                    p = graph[a][b]['weight']
                    flip = np.random.random_sample()
                    if flip <=p:
                        new_truth_actived_nodes.append(b)
                        nodes_status[b] = 1

        for a in active_nodes: 
            for b in graph.neighbors(a):
                if nodes_status[b] == 0:
                    p = graph[a][b]['weight']
                    flip = np.random.random_sample()
                    if flip <=p:
                        if verifiers[b] == 0:
                            new_actived_nodes.append(b)
                        else:
                            new_truth_actived_nodes.append(b)
                        nodes_status[b] = 1
        for node in truth_active_nodes:
            nodes_status[node] = 5
        for node in new_truth_actived_nodes:
            nodes_status[node] = 4
        for node in active_nodes:
            nodes_status[node] = 3
        for node in new_actived_nodes:
            nodes_status[node] = 2
        active_nodes = new_actived_nodes
        truth_active_nodes = new_truth_actived_nodes

    final_actived_node = 0
    for node in graph.nodes:
        if nodes_status[node] == 3:
            final_actived_node += 1
    return final_actived_node   


# ICM with Python Libraries
# It takes input the graph, and 'init_rate' : fraction of initially infected nodes as input and assigns the seeds nodes itself.
def Independent_Cascade_Model_(g,init_rate):
    # Model Configuration
    config = mc.Configuration()
    config.add_model_parameter('fraction_infected', init_rate)
    for e in g.edges():
        config.add_edge_configuration("threshold", e, g[e[0]][e[1]]['weight'])
    # Model selection
    model = ep.IndependentCascadesModel(g)
    model.set_initial_status(config)

    # Simulation execution
    iterations = model.iteration()
    while iterations['node_count'][1] >0:
        iterations = model.iteration()
    affected = (iterations['node_count'][2])
    return affected