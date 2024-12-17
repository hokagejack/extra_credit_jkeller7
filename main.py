import csv
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

def load_graph_from_csv(file_path):
    graph = {}
    start_node = None
    goal_node = None

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for row in reader:
            if row[0] == 'START':
                start_node = row[1]
            elif row[0] == 'GOAL':
                goal_node = row[1]
            else:
                node, neighbor = row[0], row[1]
                
                if node not in graph:
                    graph[node] = []
                if neighbor not in graph:
                    graph[neighbor] = []
                
                graph[node].append(neighbor)

    if start_node is None or goal_node is None:
        raise ValueError("The CSV file must specify START and GOAL nodes.")
    if start_node not in graph:
        raise ValueError(f"Start node '{start_node}' not found in the graph.")
    if goal_node not in graph:
        raise ValueError(f"Goal node '{goal_node}' not found in the graph.")

    return graph, start_node, goal_node

def bfs_recognizer(graph, start, goal):
    visited = set()
    queue = deque([start])
    path = []
    
    while queue:
        current = queue.popleft()
        path.append(current)
        
        # check if we've reached goal
        if current == goal:
            visualize_graph(graph, path, start, goal)
            return True
        
        # mark current node as visited
        if current not in visited:
            visited.add(current)
            
            # add unvisited neighbors to queue
            for neighbor in graph.get(current, []):
                if neighbor not in visited:
                    queue.append(neighbor)
    
    # goal not found
    visualize_graph(graph, path, start, goal, success=False)
    return False

def visualize_graph(graph, path, start, goal, success=True):
    # new implementation of graph visualization using networkx
    G = nx.DiGraph()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 6))
    
    # draw all nodes and edges
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=700, font_size=15, edge_color='gray')
    
    # highlight traversal path
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='yellow')
    
    # highlight start and goal nodes
    nx.draw_networkx_nodes(G, pos, nodelist=[start], node_color='green', node_size=800, label='Start')
    nx.draw_networkx_nodes(G, pos, nodelist=[goal], node_color='blue', node_size=800, label='Goal')
    
    if success:
        plt.title("BFS Path Found")
    else:
        plt.title("BFS Path Not Found")
    
    plt.legend()
    plt.show()


file_path = 'graph1.csv'  #name based on which graph you want to test
graph, start, goal = load_graph_from_csv(file_path)
print(f"Graph: {graph}")
print(f"Start Node: {start}")
print(f"Goal Node: {goal}")
result = bfs_recognizer(graph, start, goal)
print("Path Found:" if result else "No Path Found")
