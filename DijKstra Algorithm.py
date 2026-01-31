# ============================================================================
# PART 1: SETTING UP THE CITY NETWORK (Simple Data Storage)
# ============================================================================

print("="*70)
print("EMERGENCY RESPONSE ROUTE OPTIMIZER - SIMPLE VERSION")
print("="*70)

# Instead of complex classes, we'll use simple dictionaries
# Dictionary to store which locations connect to which (and travel time)
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

# Categorize each location
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

# List of high-risk zones we need to monitor
high_risk_zones = ["School", "Market", "Factory"]

print("\n📍 City Network Created!")
print(f"Total Locations: {len(city_roads)}")
print(f"High-Risk Zones: {', '.join(high_risk_zones)}")

# ============================================================================
# PART 2: FINDING SHORTEST PATH (Simple If-Else Approach)
# ============================================================================

def find_shortest_path_simple(start_location, all_roads):
    """
    Find shortest paths using simple if-else logic
    This is easier to understand than the complex heap-based algorithm
    """
    
    print(f"\n{'='*70}")
    print(f"Finding shortest routes from: {start_location}")
    print(f"{'='*70}\n")
    
    # Step 1: Initialize distances to all locations as "infinite" (999999)
    # We'll update these as we find shorter paths
    distances = {}
    paths = {}
    
    for location in all_roads.keys():
        if location == start_location:
            distances[location] = 0  # Distance to itself is 0
            paths[location] = [start_location]  # Path to itself is just itself
        else:
            distances[location] = 999999  # Start with "infinite" distance
            paths[location] = []  # No path known yet
    
    # Step 2: Keep track of which locations we've already checked
    visited = []
    
    # Step 3: Keep checking until we've visited all locations
    step_number = 1
    
    while len(visited) < len(all_roads):
        
        # Find the unvisited location with the shortest known distance
        shortest_distance = 999999
        next_location = None
        
        for location in all_roads.keys():
            # Skip if already visited
            if location in visited:
                continue
            
            # Check if this location has a shorter distance than what we've seen
            if distances[location] < shortest_distance:
                shortest_distance = distances[location]
                next_location = location
        
        # If we couldn't find any unvisited location, we're done
        if next_location is None:
            break
        
        # Mark this location as visited
        visited.append(next_location)
        current_distance = distances[next_location]
        
        print(f"Step {step_number}: Checking '{next_location}' (current distance: {current_distance} min)")
        
        # Step 4: Check all neighbors of the current location
        if next_location in all_roads:
            neighbors = all_roads[next_location]
            
            for neighbor_name, travel_time in neighbors:
                
                # Skip if neighbor already visited
                if neighbor_name in visited:
                    continue
                
                # Calculate new distance through this route
                new_distance = current_distance + travel_time
                
                # If this new route is shorter than what we knew before, update it!
                if new_distance < distances[neighbor_name]:
                    old_distance = distances[neighbor_name]
                    distances[neighbor_name] = new_distance
                    paths[neighbor_name] = paths[next_location] + [neighbor_name]
                    
                    print(f"  → Found shorter route to '{neighbor_name}':")
                    print(f"     Old distance: {old_distance} min")
                    print(f"     New distance: {new_distance} min")
                    print(f"     Path: {' → '.join(paths[neighbor_name])}")
        
        step_number += 1
        print()
    
    return distances, paths


# ============================================================================
# PART 3: DISPLAY RESULTS IN A NICE TABLE
# ============================================================================

def show_results(start_location, distances, paths):
    """Display the results in an easy-to-read format"""
    
    print(f"\n{'='*70}")
    print(f"SHORTEST ROUTES FROM {start_location}")
    print(f"{'='*70}\n")
    print(f"{'Destination':<25} {'Time':<15} {'Route'}")
    print("-"*70)
    
    # Sort by distance (shortest first)
    sorted_locations = []
    for location, distance in distances.items():
        if location != start_location:
            sorted_locations.append((location, distance))
    
    # Simple bubble sort (easier to understand than complex sorting)
    for i in range(len(sorted_locations)):
        for j in range(i + 1, len(sorted_locations)):
            if sorted_locations[i][1] > sorted_locations[j][1]:
                # Swap if out of order
                temp = sorted_locations[i]
                sorted_locations[i] = sorted_locations[j]
                sorted_locations[j] = temp
    
    # Display each route
    for location, distance in sorted_locations:
        if distance == 999999:
            print(f"{location:<25} {'UNREACHABLE':<15}")
        else:
            route_str = ' → '.join(paths[location])
            print(f"{location:<25} {distance} min{'':<10} {route_str}")


# ============================================================================
# PART 4: RUN THE ANALYSIS
# ============================================================================

print("\n" + "█"*70)
print("ANALYZING ROUTES FROM HOSPITAL A")
print("█"*70)

# Find shortest paths from Hospital A
distances_A, paths_A = find_shortest_path_simple("Hospital_A", city_roads)
show_results("Hospital_A", distances_A, paths_A)

print("\n" + "█"*70)
print("ANALYZING ROUTES FROM HOSPITAL B")
print("█"*70)

# Find shortest paths from Hospital B
distances_B, paths_B = find_shortest_path_simple("Hospital_B", city_roads)
show_results("Hospital_B", distances_B, paths_B)


# ============================================================================
# PART 5: COMPARE HOSPITALS (Using Simple If-Else)
# ============================================================================

print("\n" + "█"*70)
print("COMPARING RESPONSE TIMES TO HIGH-RISK ZONES")
print("█"*70)

print(f"\n{'Zone':<25} {'Hospital A':<15} {'Hospital B':<15} {'Winner'}")
print("-"*70)

# Compare each high-risk zone
for zone in high_risk_zones:
    time_A = distances_A[zone]
    time_B = distances_B[zone]
    
    # Use simple if-else to determine winner
    if time_A < time_B:
        winner = "Hospital A (faster)"
        difference = time_B - time_A
    elif time_B < time_A:
        winner = "Hospital B (faster)"
        difference = time_A - time_B
    else:
        winner = "Equal"
        difference = 0
    
    print(f"{zone:<25} {time_A} min{'':<10} {time_B} min{'':<10} {winner}")
    
    if difference > 0:
        print(f"{'':25} (by {difference} minutes)")

# Calculate average times
total_time_A = 0
total_time_B = 0

for zone in high_risk_zones:
    total_time_A = total_time_A + distances_A[zone]
    total_time_B = total_time_B + distances_B[zone]

avg_time_A = total_time_A / len(high_risk_zones)
avg_time_B = total_time_B / len(high_risk_zones)

print(f"\n{'='*70}")
print("AVERAGE RESPONSE TIMES")
print(f"{'='*70}")
print(f"Hospital A average: {avg_time_A:.2f} minutes")
print(f"Hospital B average: {avg_time_B:.2f} minutes")