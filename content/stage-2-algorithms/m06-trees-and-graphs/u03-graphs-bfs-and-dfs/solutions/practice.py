def hop_counts(graph, start):
    from collections import deque

    if start not in graph:
        return {}
    distances = {start: 0}
    frontier = deque([start])
    while frontier:
        node = frontier.popleft()
        for neighbor in graph[node]:
            if neighbor not in distances:
                distances[neighbor] = distances[node] + 1
                frontier.append(neighbor)
    return distances


def stack_reachable(graph, start):
    if start not in graph:
        return set()
    seen = {start}
    stack = [start]
    while stack:
        node = stack.pop()
        for neighbor in graph[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return seen


def component_count(graph):
    seen = set()
    count = 0
    for start in graph:
        if start in seen:
            continue
        count += 1
        seen.add(start)
        pending = [start]
        while pending:
            node = pending.pop()
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    pending.append(neighbor)
    return count


def flood_size(grid, row, col):
    if not grid or not (0 <= row < len(grid) and 0 <= col < len(grid[0])):
        return 0
    if grid[row][col] == 0:
        return 0
    seen = {(row, col)}
    pending = [(row, col)]
    while pending:
        r, c = pending.pop()
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                if grid[nr][nc] == 1 and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    pending.append((nr, nc))
    return len(seen)
