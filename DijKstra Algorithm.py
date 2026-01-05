import heapq
import matplotlib.pyplot as plt
import networkx as nx

# 1. Graph Construction (Adjacency List)

graph = {
    "Hospital_A": [("Intersection", 4), ("Mall", 7), ("PoliceStation", 8)],
    "Hospital_B": [("Residential", 4), ("FireStation", 6)],
    "School": [("Intersection", 5)],
    "Market": [("Intersection", 4), ("Mall", 3), ("Factory", 5), ("FireStation", 3)],
    "Factory": [("Market", 5), ("Residential", 6)],
    "FireStation": [("Intersection", 3), ("Hospital_B", 6), ("Market", 3)],
    "PoliceStation": [("Residential", 5), ("Hospital_A", 8)],
    "Mall": [("Market", 3), ("Hospital_A", 7), ("Residential", 7)],
    "Residential": [("Hospital_B", 4), ("Factory", 6), ("PoliceStation", 5), ("Mall", 7)],
    "Intersection": [("Hospital_A", 4), ("School", 5), ("Market", 4), ("FireStation", 3)]
}

# 2. Manual Dijkstra's Algorithm

def dijkstra(graph, start):
    """
    Manual implementation of Dijkstra's algorithm
    Returns: distances dictionary and paths dictionary
    """
    # Initialize distances to infinity for all nodes
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    # Initialize paths
    paths = {node: [] for node in graph}
    paths[start] = [start]
    
    # Priority queue: (distance, node)
    pq = [(0, start)]
    
    # Visited set
    visited = set()
    
    print(f"\n{'='*60}")
    print(f"Starting Dijkstra's Algorithm from: {start}")
    print(f"{'='*60}\n")
    
    step = 1
    
    while pq:
        # Get node with minimum distance
        current_dist, current_node = heapq.heappop(pq)
        
        # Skip if already visited
        if current_node in visited:
            continue
        
        # Mark as visited
        visited.add(current_node)
        
        print(f"Step {step}: Visiting '{current_node}' (distance: {current_dist})")
        print(f"  Current path: {' -> '.join(paths[current_node])}")
        
        # Explore neighbors
        for neighbor, weight in graph[current_node]:
            if neighbor not in visited:
                # Calculate new distance
                new_dist = current_dist + weight
                
                # Update if we found a shorter path
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    paths[neighbor] = paths[current_node] + [neighbor]
                    heapq.heappush(pq, (new_dist, neighbor))
                    print(f"    → Updated '{neighbor}': distance = {new_dist}, path = {' -> '.join(paths[neighbor])}")
        
        print()
        step += 1
    
    return distances, paths

# 3. Run Dijkstra from Hospital_A

distances_A, paths_A = dijkstra(graph, "Hospital_A")

print(f"\n{'='*60}")
print("FINAL SHORTEST PATHS FROM Hospital_A:")
print(f"{'='*60}\n")

for node in sorted(graph.keys()):
    if distances_A[node] == float('inf'):
        print(f"{node:15} → UNREACHABLE")
    else:
        print(f"{node:15} → {distances_A[node]:2} min | Path: {' -> '.join(paths_A[node])}")

# 4. Run Dijkstra from Hospital_B

distances_B, paths_B = dijkstra(graph, "Hospital_B")

print(f"\n{'='*60}")
print("FINAL SHORTEST PATHS FROM Hospital_B:")
print(f"{'='*60}\n")

for node in sorted(graph.keys()):
    if distances_B[node] == float('inf'):
        print(f"{node:15} → UNREACHABLE")
    else:
        print(f"{node:15} → {distances_B[node]:2} min | Path: {' -> '.join(paths_B[node])}")

# 5. Visualize the Graph

G = nx.Graph()
for node, neighbors in graph.items():
    for neighbor, weight in neighbors:
        G.add_edge(node, neighbor, weight=weight)

pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(12, 8))

# Draw all nodes and edges
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2000)
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
nx.draw_networkx_edges(G, pos, edge_color='gray', width=2)

# Draw edge labels
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

# Highlight shortest path from Hospital_A to Market
if "Market" in paths_A:
    path_to_market = paths_A["Market"]
    path_edges = [(path_to_market[i], path_to_market[i+1]) for i in range(len(path_to_market)-1)]
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=4)
    plt.title(f"Shortest Path from Hospital_A to Market: {' → '.join(path_to_market)} ({distances_A['Market']} min)", 
              fontsize=14, fontweight='bold')

plt.axis('off')
plt.tight_layout()
plt.show()

# 6. Road Congestion Simulation

print(f"\n{'='*60}")
print("SIMULATING ROAD CONGESTION")
print(f"{'='*60}\n")

# Create a copy of the graph
congested_graph = {node: list(edges) for node, edges in graph.items()}

# Simulate congestion: Intersection → Market now takes 15 minutes
for i, (neighbor, weight) in enumerate(congested_graph["Intersection"]):
    if neighbor == "Market":
        congested_graph["Intersection"][i] = ("Market", 15)

for i, (neighbor, weight) in enumerate(congested_graph["Market"]):
    if neighbor == "Intersection":
        congested_graph["Market"][i] = ("Intersection", 15)

print("⚠️  Road congestion: Intersection ↔ Market now takes 15 minutes (was 4)\n")

# Run Dijkstra again with congestion
distances_congested, paths_congested = dijkstra(congested_graph, "Hospital_A")

print(f"\n{'='*60}")
print("COMPARISON: Normal vs Congested Route to Market")
print(f"{'='*60}\n")

print(f"Normal Route:")
print(f"  Path: {' -> '.join(paths_A['Market'])}")
print(f"  Time: {distances_A['Market']} minutes\n")

print(f"Congested Route:")
print(f"  Path: {' -> '.join(paths_congested['Market'])}")
print(f"  Time: {distances_congested['Market']} minutes\n")

if paths_A['Market'] != paths_congested['Market']:
    print("✓ Algorithm found an alternative route due to congestion!")
else:
    print("✓ Same route still optimal despite congestion")