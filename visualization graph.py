"""
SIMPLE GRAPH VISUALIZATION FOR EMERGENCY RESPONSE SYSTEM
Using Easy-to-Understand Code with If-Else Conditions

This creates visual maps of the city network and highlights shortest paths.
"""

import matplotlib.pyplot as plt
import networkx as nx

print("="*70)
print("CREATING VISUALIZATIONS OF THE CITY NETWORK")
print("="*70)

# ============================================================================
# STEP 1: Set up the same city data (simple dictionaries)
# ============================================================================

# Same road network from the main program
city_roads = {
    "Hospital_A": [
        ("Intersection_Central", 4),
        ("Mall", 7),
        ("PoliceStation", 8)
    ],
    "Hospital_B": [
        ("Residential_Area", 4),
        ("FireStation", 6)
    ],
    "School": [
        ("Intersection_Central", 5)
    ],
    "Market": [
        ("Intersection_Central", 4),
        ("Mall", 3),
        ("Factory", 5),
        ("FireStation", 3)
    ],
    "Factory": [
        ("Market", 5),
        ("Residential_Area", 6)
    ],
    "FireStation": [
        ("Intersection_Central", 3),
        ("Hospital_B", 6),
        ("Market", 3)
    ],
    "PoliceStation": [
        ("Residential_Area", 5),
        ("Hospital_A", 8)
    ],
    "Mall": [
        ("Market", 3),
        ("Hospital_A", 7),
        ("Residential_Area", 7)
    ],
    "Residential_Area": [
        ("Hospital_B", 4),
        ("Factory", 6),
        ("PoliceStation", 5),
        ("Mall", 7)
    ],
    "Intersection_Central": [
        ("Hospital_A", 4),
        ("School", 5),
        ("Market", 4),
        ("FireStation", 3)
    ]
}

# Location categories
location_types = {
    "Hospital_A": "Hospital",
    "Hospital_B": "Hospital",
    "School": "High-Risk Zone",
    "Market": "High-Risk Zone",
    "Factory": "High-Risk Zone",
    "FireStation": "Emergency Service",
    "PoliceStation": "Emergency Service",
    "Mall": "Public Place",
    "Residential_Area": "Residential",
    "Intersection_Central": "Intersection"
}

# Shortest paths we calculated (from the main program)
path_hospital_a_to_market = ["Hospital_A", "Intersection_Central", "Market"]
path_hospital_b_to_market = ["Hospital_B", "FireStation", "Market"]
path_congested = ["Hospital_A", "Intersection_Central", "FireStation", "Market"]

# ============================================================================
# STEP 2: Create the graph using NetworkX (Simple Version)
# ============================================================================

print("\n[Step 1] Building the network graph...")

# Create an empty graph
G = nx.Graph()

# Add all locations as nodes
print("  → Adding locations (nodes)...")
for location in city_roads.keys():
    # Get the type of this location
    loc_type = location_types[location]
    # Add it to the graph with its type
    G.add_node(location, node_type=loc_type)

# Add all roads as edges (connections)
print("  → Adding roads (edges)...")
edges_added = []  # Keep track so we don't add duplicates

for location, connections in city_roads.items():
    for neighbor, travel_time in connections:
        # Create edge name (sorted so "A-B" and "B-A" are the same)
        edge = tuple(sorted([location, neighbor]))
        
        # Only add if we haven't added this edge yet
        if edge not in edges_added:
            G.add_edge(location, neighbor, weight=travel_time)
            edges_added.append(edge)

print(f"  ✓ Graph created: {len(G.nodes())} locations, {len(G.edges())} roads")

# ============================================================================
# STEP 3: Function to Draw the Graph (Using Simple If-Else Logic)
# ============================================================================

def draw_city_network(graph, title, highlight_path=None, filename=None):
    """
    Draw the city network with colors and optional path highlighting
    Uses simple if-else conditions to assign colors
    """
    
    print(f"\n[Drawing] {title}...")
    
    # Create a new figure
    plt.figure(figsize=(14, 10))
    
    # Position the nodes nicely (spring layout spreads them out)
    print("  → Positioning locations...")
    pos = nx.spring_layout(graph, k=2, iterations=50, seed=42)
    
    # ========================================================================
    # Assign colors to each location using IF-ELSE
    # ========================================================================
    print("  → Assigning colors to locations...")
    
    node_colors = []
    
    for location in graph.nodes():
        # Get the type of this location
        loc_type = graph.nodes[location]['node_type']
        
        # Use if-else to decide the color
        if loc_type == "Hospital":
            color = '#FF6B6B'  # Red for hospitals
        elif loc_type == "High-Risk Zone":
            color = '#FFA500'  # Orange for high-risk zones
        elif loc_type == "Emergency Service":
            color = '#4ECDC4'  # Teal for emergency services
        elif loc_type == "Public Place":
            color = '#95E1D3'  # Light green for public places
        elif loc_type == "Residential":
            color = '#F8E16C'  # Yellow for residential
        else:  # Intersection
            color = '#A8E6CF'  # Light green for intersections
        
        node_colors.append(color)
    
    # ========================================================================
    # Draw the base network
    # ========================================================================
    print("  → Drawing locations (circles)...")
    
    # Draw all nodes (locations) as circles
    nx.draw_networkx_nodes(
        graph, pos,
        node_color=node_colors,
        node_size=3000,
        alpha=0.9,
        edgecolors='black',
        linewidths=2
    )
    
    # Draw location names
    print("  → Adding location names...")
    nx.draw_networkx_labels(
        graph, pos,
        font_size=9,
        font_weight='bold'
    )
    
    # Draw all roads (edges) in gray
    print("  → Drawing roads (lines)...")
    nx.draw_networkx_edges(
        graph, pos,
        edge_color='gray',
        width=2,
        alpha=0.6
    )
    
    # Draw travel times on roads
    print("  → Adding travel times on roads...")
    edge_labels = {}
    for location1, location2, data in graph.edges(data=True):
        edge_labels[(location1, location2)] = data['weight']
    
    nx.draw_networkx_edge_labels(
        graph, pos,
        edge_labels=edge_labels,
        font_size=8,
        font_color='red'
    )
    
    # ========================================================================
    # Highlight the shortest path if provided (Using If-Else)
    # ========================================================================
    
    if highlight_path is not None:
        print(f"  → Highlighting path: {' → '.join(highlight_path)}")
        
        # Create list of edges in the path
        path_edges = []
        
        # Use a simple loop to create edge pairs
        for i in range(len(highlight_path) - 1):
            edge = (highlight_path[i], highlight_path[i + 1])
            path_edges.append(edge)
        
        # Draw the path edges in blue (thick lines)
        nx.draw_networkx_edges(
            graph, pos,
            edgelist=path_edges,
            edge_color='blue',
            width=5,
            alpha=0.8
        )
        
        # Highlight the locations in the path with yellow circles
        nx.draw_networkx_nodes(
            graph, pos,
            nodelist=highlight_path,
            node_color='yellow',
            node_size=3500,
            alpha=0.8,
            edgecolors='blue',
            linewidths=3
        )
    
    # ========================================================================
    # Add title and legend
    # ========================================================================
    
    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    
    # Create a legend (color guide)
    from matplotlib.patches import Patch
    legend_items = [
        Patch(facecolor='#FF6B6B', edgecolor='black', label='Hospitals'),
        Patch(facecolor='#FFA500', edgecolor='black', label='High-Risk Zones'),
        Patch(facecolor='#4ECDC4', edgecolor='black', label='Emergency Services'),
        Patch(facecolor='#95E1D3', edgecolor='black', label='Public Places'),
        Patch(facecolor='#F8E16C', edgecolor='black', label='Residential'),
        Patch(facecolor='#A8E6CF', edgecolor='black', label='Intersections')
    ]
    
    plt.legend(handles=legend_items, loc='upper left', fontsize=10)
    
    # Remove axes
    plt.axis('off')
    plt.tight_layout()
    
    # Save the image if filename provided
    if filename is not None:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved as: {filename}")
    
    plt.show()
    print("  ✓ Display complete!")

# ============================================================================
# STEP 4: Create All Visualizations
# ============================================================================

print("\n" + "="*70)
print("GENERATING VISUALIZATIONS")
print("="*70)

# Visualization 1: Complete network overview
print("\n📊 Visualization 1 of 4")
draw_city_network(
    G,
    "City Road Network - Complete Overview",
    highlight_path=None,
    filename="network_overview.png"
)

# Visualization 2: Hospital A to Market (normal route)
print("\n📊 Visualization 2 of 4")
draw_city_network(
    G,
    "Shortest Path: Hospital A → Market (8 minutes)",
    highlight_path=path_hospital_a_to_market,
    filename="hospital_a_to_market.png"
)

# Visualization 3: Hospital B to Market
print("\n📊 Visualization 3 of 4")
draw_city_network(
    G,
    "Shortest Path: Hospital B → Market (9 minutes)",
    highlight_path=path_hospital_b_to_market,
    filename="hospital_b_to_market.png"
)

# Visualization 4: Congested route (alternative path)
print("\n📊 Visualization 4 of 4")
draw_city_network(
    G,
    "Congested Route: Hospital A → Market (10 minutes)",
    highlight_path=path_congested,
    filename="congested_route.png"
)

# ============================================================================
# STEP 5: Summary
# ============================================================================

print("\n" + "="*70)
print("VISUALIZATION COMPLETE!")
print("="*70)

print("\n✓ Created 4 visualizations:")
print("  1. network_overview.png - Shows entire city network")
print("  2. hospital_a_to_market.png - Normal route from Hospital A")
print("  3. hospital_b_to_market.png - Route from Hospital B")
print("  4. congested_route.png - Alternative route during traffic")

print("\n📁 All images saved in the current directory")
print("   Look for .png files to view the maps!\n")

print("="*70)
print("HOW THE VISUALIZATION WORKS (Simple Explanation)")
print("="*70)

print("""
1. CREATE GRAPH
   - Add each location as a node (circle)
   - Add each road as an edge (line connecting circles)

2. ASSIGN COLORS (using if-else)
   if location_type == "Hospital":
       color = red
   elif location_type == "High-Risk Zone":
       color = orange
   ... and so on

3. DRAW EVERYTHING
   - Draw circles for locations
   - Draw lines for roads
   - Add labels and travel times

4. HIGHLIGHT PATH (if provided)
   - Make path edges blue and thick
   - Make path nodes yellow
   - This shows the shortest route clearly!

Simple, right? It's just if-else conditions deciding colors! 🎨
""")

print("="*70 + "\n")