import requests

def fetch_locations():
    url = "https://www.hertzfreerider.se/api/locations/"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    r = requests.get(url, headers=headers)
    if r.ok:
        return r.json()
    return []

def fetch_routes():
    url = "https://www.hertzfreerider.se/api/transport-routes/?country=SWEDEN"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    r = requests.get(url, headers=headers)
    if r.ok:
        return r.json()
    return []

def build_graph(routes):
    graph = {}
    for route in routes:
        start = route.get("pickupLocationName")
        end = route.get("returnLocationName")
        if start and end:
            graph.setdefault(start, set()).add(end)
    # Sätt om till listor för lättare hantering
    for k in graph:
        graph[k] = list(graph[k])
    return graph
