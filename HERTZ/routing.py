import requests
from collections import deque

def fetch_routes():
    url = "https://www.hertzfreerider.se/api/transport-routes/?country=SWEDEN"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    return requests.get(url, headers=headers).json()

def build_route_graph(routes_data):
    graph = {}
    for item in routes_data:
        start = item.get("pickupLocationName")
        end = item.get("returnLocationName")
        if start and end:
            graph.setdefault(start, []).append(end)
    return graph

def bfs_route(start, end, graph, max_depth=5):
    queue = deque()
    queue.append((start, [start]))
    while queue:
        current, path = queue.popleft()
        if current == end:
            return path
        if len(path) > max_depth:
            continue
        for neighbor in graph.get(current, []):
            if neighbor not in path:
                queue.append((neighbor, path + [neighbor]))
    return None

def get_routes_for_bot(start, end):
    try:
        routes = fetch_routes()
        graph = build_route_graph(routes)
        path = bfs_route(start, end, graph)
        if path:
            return " → ".join(path)
        else:
            return "Ingen direkt eller indirekt rutt hittades."
    except Exception as e:
        return f"Fel: {str(e)}"
