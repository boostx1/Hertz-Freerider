import requests
from collections import deque

def fetch_routes():
    url = "https://www.hertzfreerider.se/api/transport-routes/?country=SWEDEN"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Fel vid hämtning routes:", response.status_code)
        return []

def build_route_maps(routes_data):
    from_routes = {}
    for loc in routes_data:
        start = loc.get("pickupLocationName")
        end = loc.get("returnLocationName")
        if start and end:
            from_routes.setdefault(start, []).append(end)
    return from_routes

def find_routes_by_place_names(start_place, end_place, from_routes, max_depth=5):
    all_routes = []
    queue = deque()
    queue.append(([start_place], set([start_place])))

    while queue:
        path, visited = queue.popleft()
        last = path[-1]

        if last == end_place and len(path) > 1:
            all_routes.append(path)
            continue

        if len(path) >= max_depth:
            continue

        for next_place in from_routes.get(last, []):
            if next_place not in visited:
                queue.append((path + [next_place], visited | set([next_place])))

    return all_routes
