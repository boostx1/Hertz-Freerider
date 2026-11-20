import requests
from collections import deque

def fetch_locations():
    response = requests.get("https://www.hertzfreerider.se/api/locations/", headers={"User-Agent": "Mozilla/5.0"})
    return response.json() if response.status_code == 200 else []

def fetch_routes():
    response = requests.get("https://www.hertzfreerider.se/api/transport-routes/?country=SWEDEN", headers={"User-Agent": "Mozilla/5.0"})
    return response.json() if response.status_code == 200 else []

def build_route_graph(routes):
    graph = {}
    for loc in routes:
        start = loc.get("pickupLocationName")
        end = loc.get("returnLocationName")
        if start and end:
            graph.setdefault(start, []).append(end)
    return graph

def find_routes(graph, start, end, max_depth=5):
    routes = []
    queue = deque()
    queue.append(([start], {start}))
    while queue:
        path, visited = queue.popleft()
        last = path[-1]
        if last == end and len(path) > 1:
            routes.append(path)
            continue
        if len(path) >= max_depth:
            continue
        for neighbor in graph.get(last, []):
            if neighbor not in visited:
                queue.append((path + [neighbor], visited | {neighbor}))
    return routes
