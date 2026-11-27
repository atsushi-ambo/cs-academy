def sift_up(heap, i):
    """
    Change a list of integers in place and return None. The list was a min-heap until
    one value was just appended; i is that last index. Use index comparisons and swaps,
    with no heap library or sort. Sift up at index 3 in [2, 7, 5, 1] to get [1, 2, 5, 7].
    """
    while i > 0:
        parent = (i - 1) // 2
        if heap[parent] <= heap[i]:
            break
        heap[i], heap[parent] = heap[parent], heap[i]
        i = parent


def push(heap, value, sift_up):
    """
    Append an integer to the given heap list in place and use the given sift_up(heap, i)
    to repair it. Return None. Do not use heapq or sort. Push 3 into [5, 7, 8] to get [3,
    5, 8, 7].
    """
    heap.append(value)
    sift_up(heap, len(heap) - 1)


def sift_down(heap, i):
    """
    Repair the subtree at a valid index i in place, with both child subtrees already min-
    heaps. Return None. Use no heap library or sort. [10, 6, 3, 7, 9, 4] at i = 0 becomes
    [3, 6, 4, 7, 9, 10].
    """
    while 2*i + 1 < len(heap):
        child = 2*i + 1
        right = child + 1
        if right < len(heap) and heap[right] < heap[child]:
            child = right
        if heap[i] <= heap[child]:
            break
        heap[i], heap[child] = heap[child], heap[i]
        i = child


def pop_min(heap, sift_down):
    """
    For an integer heap, update the same list and return its minimum, or None for an
    empty heap. Use the given sift_down(heap, i). Use no heapq or sort. For [2, 4, 3, 7],
    return 2 and leave [3, 4, 7].
    """
    if not heap:
        return None
    smallest = heap[0]
    last = heap.pop()
    if heap:
        heap[0] = last
        sift_down(heap, 0)
    return smallest


def heapify(heap, sift_down):
    """
    Turn an integer list into a min-heap by sifting parents from the bottom. Use the
    given sift_down(heap, i). Do not use heapq, sorting, or a second list. Return None.
    For [9, 1, 4], the list becomes [1, 9, 4].
    """
    for i in range(len(heap) // 2 - 1, -1, -1):
        sift_down(heap, i)


def schedule(jobs):
    """
    Use heapq to return job names from a list of (integer priority, name) pairs. Smaller
    priorities run first. Equal priorities follow arrival order. Keep the input
    unchanged, and keep repeat names. [(2, "log"), (1, "alert"), (2, "sync")] becomes
    ["alert", "log", "sync"].
    """
    from heapq import heappop, heappush

    heap = []
    for index, (priority, name) in enumerate(jobs):
        heappush(heap, (priority, index, name))
    result = []
    while heap:
        priority, index, name = heappop(heap)
        result.append(name)
    return result
