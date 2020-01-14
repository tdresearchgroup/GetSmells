def detectCycle(graph, start, vertexInCycle):
    # Set all vertexes to None, as we don't know the status of it
    visited = {v: False for v in graph}

    stack = [start]

    # Traverse from start, adding connected nodes to the stack as we go
    while stack:
        vertex = stack.pop()

        # If we hit a vertex we've seen before, it is a cycle
        if visited[vertex]:
            vertexInCycle.add(vertex)
            return True

        # Mark this vertex as visited
        visited[vertex] = True

        # Add connected nodes to stack, if any
        stack.extend(graph[vertex])

    # If stack is empty, that means no cycle for this start vertex
    return False


def getCyclicVertex(graph):
    vertexInCycle = set()
    # Loop through each vertex, and check if it has cycles or not
    for vertex in graph:
        detectCycle(graph, vertex, vertexInCycle)

    return vertexInCycle
