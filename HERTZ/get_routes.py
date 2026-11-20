import requests
from collections import defaultdict, deque
import heapq

def fetch_locations():
    url = "https://www.hertzfreerider.se/api/locations/"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Could not retrieve locations:", response.status_code)
        return []

def fetch_routes():
    url = "https://www.hertzfreerider.se/api/transport-routes/?country=SWEDEN"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Could not retrieve routes:", response.status_code)
        return []

def build_graph_with_distance(routes_data):
    graph = defaultdict(list)  # Neighbors and edge distances
    for loc in routes_data:
        start = loc.get("pickupLocationName")
        end = loc.get("returnLocationName")
        distance = loc.get("distance")
        if start and end and distance is not None:
            graph[start].append( (end, distance) )
    return graph

def print_graph(graph):
    print("Graph (location → [destination (distance)])")
    for start, edges in graph.items():
        print(f"{start}:")
        for (dest, dist) in edges:
            print(f"  → {dest} ({dist} km)")
    print("\n")

def dijkstra(graph, start, end):
    queue = [(0, start, [start])]  # (cost, node, path)
    visited = set()

    while queue:
        cost, node, path = heapq.heappop(queue)
        if node == end:
            return path, cost

        if node in visited:
            continue
        visited.add(node)

        for neighbor, dist in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(queue, (cost + dist, neighbor, path + [neighbor]))

    return None, float('inf')

def main():
    print("Retrieving locations...")
    locations = fetch_locations()
    if not locations:
        print("No locations available.")
        return

    print("Retrieving routes...")
    routes = fetch_routes()
    if not routes:
        print("No routes available.")
        return

    print("Building the distance graph...")
    graph = build_graph_with_distance(routes)

    print_graph(graph)

    start_place = input("Enter the exact pickup location (pickupLocationName): ").strip()
    end_place = input("Enter the exact return location (returnLocationName): ").strip()

    if not start_place or not end_place:
        print("Enter both a pickup location and a destination.")
        return

    print(f"\nFinding the shortest route from '{start_place}' to '{end_place}'...")

    path, cost = dijkstra(graph, start_place, end_place)

    if path:
        print(f"Shortest route (total {cost:.1f} km):")
        print(" → ".join(path))
    else:
        print(f"No route found between {start_place} and {end_place}.")

if __name__ == "__main__":
    main()
