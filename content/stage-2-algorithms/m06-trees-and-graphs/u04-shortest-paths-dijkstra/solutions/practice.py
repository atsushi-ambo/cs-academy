def latencies(graph, start):
    if start not in graph:
        return {}
    from heapq import heappop, heappush

    best = {start: 0}
    heap = [(0, start)]
    while heap:
        cost, node = heappop(heap)
        if cost != best[node]:
            continue
        for neighbor, weight in graph[node]:
            candidate = cost + weight
            if neighbor not in best or candidate < best[neighbor]:
                best[neighbor] = candidate
                heappush(heap, (candidate, neighbor))
    return best


def trace_route(parent, start, target):
    if target != start and target not in parent:
        return []
    path = [target]
    while path[-1] != start:
        path.append(parent[path[-1]])
    return path[::-1]


def lowest_latency(graph, start, target):
    from heapq import heappop, heappush

    if start not in graph or target not in graph:
        return (None, [])
    best = {start: 0}
    parent = {}
    heap = [(0, start)]
    while heap:
        cost, node = heappop(heap)
        if cost != best[node]:
            continue
        if node == target:
            path = [target]
            while path[-1] != start:
                path.append(parent[path[-1]])
            return (cost, path[::-1])
        for neighbor, weight in graph[node]:
            candidate = cost + weight
            if neighbor not in best or candidate < best[neighbor]:
                best[neighbor] = candidate
                parent[neighbor] = node
                heappush(heap, (candidate, neighbor))
    return (None, [])
