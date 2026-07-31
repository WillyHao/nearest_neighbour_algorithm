import copy


def NN(A, start):
    """
    Nearest Neighbour Algorithm for Traveling Salesperson Problem (TSP).
    A: Adjacency matrix (2D list of numbers) with float('inf') on the diagonal.
    start: 1-indexed starting node.
    """
    start = start - 1  # Convert to 0-based indexing
    n = len(A)
    path = [start]
    cost_list = []
    current_node = start

    # Deep copy matrix to avoid modifying original input
    B = copy.deepcopy(A)

    # Mark start node's column as inf so we don't revisit it early
    for row in B:
        row[start] = float("inf")

    # Visit remaining (n - 1) nodes
    for _ in range(n - 1):
        row = B[current_node]

        # Find the index of the minimum edge in the current row
        min_cost = float("inf")
        next_node = -1

        for col_idx in range(n):
            if row[col_idx] < min_cost:
                min_cost = row[col_idx]
                next_node = col_idx

        cost_list.append(min_cost)
        path.append(next_node)
        current_node = next_node

        # Mark visited node's column as inf
        for row in B:
            row[current_node] = float("inf")

    # Add return edge cost back to the starting node
    return_cost = A[path[-1]][start]
    total_cost = sum(cost_list) + return_cost
    path.append(start)

    # Convert back to 1-based indexing for display
    display_path = [i + 1 for i in path]

    print(f"Start Node: {start + 1}")
    print(f"  Path: {display_path}")
    print(f"  Cost: {total_cost}\n")

    return display_path, total_cost


def every_node(A):
    """Runs the NN algorithm starting from every node (1 through n)."""
    print("=== Running NN for All Starting Nodes ===")
    results = []
    for i in range(1, len(A) + 1):
        results.append(NN(A, i))
    return results


# ==========================================
# SAMPLE RUN 1: 4-City Distance Matrix
# ==========================================
print("--- Sample 1: 4-City Graph ---")
inf = float("inf")

# 4x4 Distance matrix (diagonal set to infinity)
matrix_4x4 = [
    [inf, 10, 15, 20],
    [10, inf, 35, 25],
    [15, 35, inf, 30],
    [20, 25, 30, inf],
]

# Single run starting from Node 1
print("Single Run starting from Node 1:")
NN(matrix_4x4, start=1)

# Run for all starting nodes
every_node(matrix_4x4)