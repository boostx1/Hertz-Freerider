from collections import deque

def bfs_find_routes(graph, start, end, max_depth=5):
    queue = deque()
    queue.append(([start], set([start])))
    routes = []

    while queue:
        path, visited = queue.popleft()
        current = path[-1]

        if current == end and len(path) > 1:
            routes.append(path)
            continue

        if len(path) >= max_depth:
            continue

        for nxt in graph.get(current, []):
            if nxt not in visited:
                queue.append((path + [nxt], visited | {nxt}))

    return routes
