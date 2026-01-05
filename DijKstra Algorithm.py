import networkx as nx
import matplotlib.pyplot as plt

# -------------------------------
# 1. Graph Construction
# -------------------------------
G = nx.Graph()

# Nodes (10 locations)
nodes = [
    "Hospital_A", "Hospital_B", "School", "Market", "Factory",
    "FireStation", "PoliceStation", "Mall", "Residential", "Intersection"
]
G.add_nodes_from(nodes)

# Edges with travel time (minutes)
edges = [
    ("Hospital_A", "Intersection", 4),
    ("Intersection", "School", 5),
    ("Intersection", "Market", 6),
    ("Market", "Mall", 3),
    ("Mall", "Hospital_A", 7),
    ("Hospital_B", "Residential", 4),
    ("Residential", "Factory", 6),
    ("Factory", "Market", 5),
    ("FireStation", "Intersection", 3),
    ("PoliceStation", "Residential", 5),
    ("FireStation", "Hospital_B", 6),
    ("PoliceStation", "Hospital_A", 8),
    ("Mall", "Residential", 7)
]

G.add_weighted_edges_from(edges)

# -------------------------------
# 2. Dijkstra’s Algorithm
# -------------------------------
dist_A, paths_A = nx.single_source_dijkstra(G, "Hospital_A")
dist_B, paths_B = nx.single_source_dijkstra(G, "Hospital_B")

print("\nShortest paths from Hospital_A:\n")
for node in G.nodes():
    print(f"{node}: Path = {' -> '.join(paths_A[node])}, Time = {dist_A[node]} min")

print("\nShortest paths from Hospital_B:\n")
for node in G.nodes():
    print(f"{node}: Path = {' -> '.join(paths_B[node])}, Time = {dist_B[node]} min")

# -------------------------------
# 3. Graph Visualization
# -------------------------------
pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(10, 8))
nx.draw(G, pos, with_labels=True, node_size=2000)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Highlight shortest path from Hospital_A to Market
shortest_path = paths_A["Market"]
path_edges = list(zip(shortest_path, shortest_path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4)

plt.title("Urban Transport Network with Shortest Path Highlighted")
plt.show()

# -------------------------------
# 4. Road Congestion Simulation
# -------------------------------
G["Intersection"]["Market"]["weight"] = 15  # simulate blockage

dist_blocked, paths_blocked = nx.single_source_dijkstra(G, "Hospital_A")

print("\nAfter road congestion (Intersection → Market):")
print("New path to Market:", " -> ".join(paths_blocked["Market"]))
print("New travel time:", dist_blocked["Market"], "min")
