"""
Problem 3: Travelling Salesman Problem - Nearest Neighbour Heuristic
CSC2103 Data Structures and Algorithms - Group Project

Description:
    Given a set of cities (as 2D coordinates), find a tour that visits every
    city exactly once and returns to the start, using the Nearest Neighbour
    heuristic: from the current city, always move to the closest unvisited
    city. This does NOT guarantee the optimal (shortest possible) tour, but
    produces a good solution quickly.

Time Complexity: O(n^2) -- for each of n cities, scan remaining unvisited
                            cities to find the nearest one.

Code structure (in order below):
    1. Explanation      - prints a plain-language walkthrough of the algorithm
    2. Input handling    - get_cities() reads user input
    3. Core algorithm    - euclidean_distance, build_distance_matrix,
                            nearest_neighbour_tsp  (all manual, no libraries)
    4. Output formatting - print_distance_matrix, print_tour
    5. Testing           - run_built_in_tests() runs several fixed cases
                            so correctness can be checked without typing
                            input every time
    6. Menu / main       - lets the user choose custom input or test mode
"""

import math


# ---------------------------------------------------------------------------
# 1. EXPLANATION
# ---------------------------------------------------------------------------
def explain_algorithm():
    """Print a short, plain-language explanation of Nearest Neighbour TSP."""
    print("""
--- How the Nearest Neighbour Heuristic Works ---
1. Start at a chosen city. Mark it as visited.
2. Look at every unvisited city and measure the straight-line distance
   from the CURRENT city to each of them.
3. Move to whichever unvisited city is closest. Mark it visited.
4. Repeat steps 2-3 until every city has been visited.
5. Finally, travel back from the last city to the starting city to
   complete the loop.

This is called a "heuristic" (not a guaranteed-optimal algorithm) because
always taking the closest next step can lead to a bad final move -- e.g.
the last unvisited city might be far away, forcing a long detour home.
It trades guaranteed optimality for speed: O(n^2) instead of checking
every possible route, which would take O(n!) time.
""")


# ---------------------------------------------------------------------------
# 2. INPUT HANDLING
# ---------------------------------------------------------------------------
def get_cities():
    """Prompt the user for city names and coordinates."""
    cities = []
    while True:
        try:
            n = int(input("Enter number of cities (minimum 2): "))
            if n >= 2:
                break
            print("Please enter at least 2 cities.")
        except ValueError:
            print("Invalid number, try again.")

    for i in range(n):
        while True:
            try:
                raw = input(
                    f"City {i + 1} - enter as 'Name X Y' (e.g. A 0 0): "
                ).split()
                name, x, y = raw[0], float(raw[1]), float(raw[2])
                cities.append({"name": name, "x": x, "y": y})
                break
            except (ValueError, IndexError):
                print("Invalid format. Example: A 0 0")
    return cities


# ---------------------------------------------------------------------------
# 3. CORE ALGORITHM (manual implementation, no algorithm libraries used)
# ---------------------------------------------------------------------------
def euclidean_distance(city_a, city_b):
    """Straight-line distance between two cities. Manual calculation."""
    dx = city_a["x"] - city_b["x"]
    dy = city_a["y"] - city_b["y"]
    return math.sqrt(dx * dx + dy * dy)


def build_distance_matrix(cities):
    """Precompute distances between every pair of cities."""
    n = len(cities)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = euclidean_distance(cities[i], cities[j])
    return matrix


def nearest_neighbour_tsp(cities, matrix, start_index):
    """
    Core Nearest Neighbour heuristic.
    Works on ANY distance matrix -- whether it was calculated from
    coordinates, or entered directly (e.g. road distances, costs).
    Returns (tour_order_as_indices, total_distance).
    """
    n = len(cities)
    visited = [False] * n
    tour = [start_index]
    visited[start_index] = True
    current = start_index
    total_distance = 0.0

    for _ in range(n - 1):
        nearest_index = -1
        nearest_dist = math.inf

        # Manually scan all unvisited cities for the closest one
        for candidate in range(n):
            if not visited[candidate]:
                dist = matrix[current][candidate]
                if dist < nearest_dist:
                    nearest_dist = dist
                    nearest_index = candidate

        visited[nearest_index] = True
        tour.append(nearest_index)
        total_distance += nearest_dist
        current = nearest_index

    # Return to the starting city to complete the tour
    total_distance += matrix[current][start_index]
    tour.append(start_index)

    return tour, total_distance


def get_named_cities(names):
    """Build a simple city-list (name only, no coordinates) from names."""
    return [{"name": name} for name in names]


def get_matrix_input():
    """
    Prompt the user to enter a distance matrix directly, row by row,
    instead of coordinates. Useful when distances are given (e.g. a
    graph diagram or cost table) rather than derivable from positions.
    """
    while True:
        try:
            n = int(input("Enter number of cities (minimum 2): "))
            if n >= 2:
                break
            print("Please enter at least 2 cities.")
        except ValueError:
            print("Invalid number, try again.")

    names = input(f"Enter {n} city names separated by spaces (e.g. A B C D): ").split()
    while len(names) != n:
        names = input(f"Please enter exactly {n} names: ").split()

    print("\nNow enter each row of the distance matrix.")
    print("Use 0 for the diagonal (distance to itself).")
    matrix = []
    for name in names:
        while True:
            try:
                row = [float(v) for v in input(f"Row for {name} ({' '.join(names)}): ").split()]
                if len(row) == n:
                    matrix.append(row)
                    break
                print(f"Please enter exactly {n} values.")
            except ValueError:
                print("Invalid numbers, try again.")

    cities = get_named_cities(names)
    return cities, matrix


# ---------------------------------------------------------------------------
# 4. OUTPUT FORMATTING
# ---------------------------------------------------------------------------
def print_distance_matrix(cities, matrix):
    print("\nDistance Matrix:")
    header = "        " + "".join(f"{c['name']:>8}" for c in cities)
    print(header)
    for i, row in enumerate(matrix):
        row_str = "".join(f"{val:8.2f}" for val in row)
        print(f"{cities[i]['name']:>8}{row_str}")


def print_tour(cities, matrix, tour, total_distance):
    print("\n--- Nearest Neighbour Tour Result ---")

    # Path shown as a simple list
    path_names = [cities[i]["name"] for i in tour]
    print("Path taken: " + " -> ".join(path_names))

    # Step-by-step legs shown as a proper aligned table with running cost
    print("\nStep-by-step legs:")
    print(f"  {'Step':<6}{'From':<8}{'To':<8}{'Leg Dist':>10}{'Running Total':>16}")
    print("  " + "-" * 48)
    running_total = 0.0
    for i in range(len(tour) - 1):
        a_idx, b_idx = tour[i], tour[i + 1]
        a_name, b_name = cities[a_idx]["name"], cities[b_idx]["name"]
        leg_dist = matrix[a_idx][b_idx]
        running_total += leg_dist
        print(f"  {i + 1:<6}{a_name:<8}{b_name:<8}{leg_dist:>10.2f}{running_total:>16.2f}")

    # Cost summary, boxed for visibility in a screenshot
    print("\n" + "=" * 40)
    print(f"  TOTAL TOUR DISTANCE: {total_distance:.2f}")
    print("=" * 40)


def solve_and_print(cities, start_name, matrix=None):
    """
    Run the full pipeline for one dataset and print results.
    If matrix is not given, it is calculated from coordinates (x, y).
    If matrix IS given, coordinates are not needed (e.g. graph/table input).
    """
    if matrix is None:
        matrix = build_distance_matrix(cities)
    print_distance_matrix(cities, matrix)

    start_index = next(i for i, c in enumerate(cities) if c["name"] == start_name)
    tour, total_distance = nearest_neighbour_tsp(cities, matrix, start_index)
    print_tour(cities, matrix, tour, total_distance)
    return total_distance


# ---------------------------------------------------------------------------
# 5. TESTING WITH DIFFERENT INPUT CASES
# ---------------------------------------------------------------------------
def run_built_in_tests():
    """
    Runs the algorithm on several predefined datasets so correctness can be
    checked quickly and consistently, without retyping input each time.

    Test cases chosen to cover different scenarios:
      Test 1: Small square (4 cities) - easy to verify NN result by hand.
      Test 2: Clustered points with one outlier - shows NN's weakness,
               since visiting the outlier last forces a long return trip.
      Test 3: Evenly spaced points on a line - NN should behave near-optimally.
    """
    test_cases = [
        {
            "name": "Test 1: Simple square",
            "cities": [
                {"name": "A", "x": 0, "y": 0},
                {"name": "B", "x": 0, "y": 10},
                {"name": "C", "x": 10, "y": 10},
                {"name": "D", "x": 10, "y": 0},
            ],
            "start": "A",
        },
        {
            "name": "Test 2: Cluster + far outlier (shows NN weakness)",
            "cities": [
                {"name": "A", "x": 0, "y": 0},
                {"name": "B", "x": 1, "y": 1},
                {"name": "C", "x": 2, "y": 0},
                {"name": "D", "x": 1, "y": -1},
                {"name": "E", "x": 50, "y": 50},  # far outlier
            ],
            "start": "A",
        },
        {
            "name": "Test 3: Points roughly on a line",
            "cities": [
                {"name": "A", "x": 0, "y": 0},
                {"name": "B", "x": 5, "y": 1},
                {"name": "C", "x": 10, "y": 0},
                {"name": "D", "x": 15, "y": 1},
                {"name": "E", "x": 20, "y": 0},
            ],
            "start": "A",
        },
    ]

    for case in test_cases:
        print("\n" + "=" * 60)
        print(case["name"])
        print("=" * 60)
        solve_and_print(case["cities"], case["start"])

    # --- Test 4: direct distance matrix (not from coordinates) ---
    # This is the 8-city graph/table example: distances are given
    # directly (like road distances or costs), not calculated from
    # (x, y) positions.
    print("\n" + "=" * 60)
    print("Test 4: 8-city graph with given distance matrix (no coordinates)")
    print("=" * 60)
    names = ["A", "B", "C", "D", "E", "F", "G", "H"]
    cities = get_named_cities(names)
    matrix = [
        [0, 4, 24, 16, 20, 15, 9, 22],
        [4, 0, 20, 20, 20, 14, 8, 21],
        [24, 20, 0, 9, 4, 22, 16, 7],
        [16, 20, 9, 0, 5, 14, 17, 6],
        [20, 20, 4, 5, 0, 18, 12, 3],
        [15, 14, 22, 14, 18, 0, 6, 19],
        [9, 8, 16, 17, 6, 6, 0, 13],
        [22, 21, 7, 6, 3, 19, 13, 0],
    ]
    solve_and_print(cities, "A", matrix=matrix)

    # --- Test 5: another direct distance matrix example (5 cities) ---
    # Same idea as Test 4, but a smaller matrix. Useful as a quick,
    # easy-to-check example for the report alongside the bigger 8-city one.
    print("\n" + "=" * 60)
    print("Test 5: 5-city example with given distance matrix (no coordinates)")
    print("=" * 60)
    names5 = ["A", "B", "C", "D", "E"]
    cities5 = get_named_cities(names5)
    matrix5 = [
        [0.00, 1.41, 4.47, 8.60, 12.81],
        [1.41, 0.00, 3.16, 7.21, 11.40],
        [4.47, 3.16, 0.00, 4.24, 8.49],
        [8.60, 7.21, 4.24, 0.00, 4.24],
        [12.81, 11.40, 8.49, 4.24, 0.00],
    ]
    solve_and_print(cities5, "A", matrix=matrix5)


# ---------------------------------------------------------------------------
# 6. MENU / MAIN
# ---------------------------------------------------------------------------
def main():
    print("=== Travelling Salesman Problem - Nearest Neighbour Heuristic ===")

    while True:
        print("""
Menu:
  1. Explain how the algorithm works
  2. Enter cities by (x, y) coordinates
  3. Enter cities by direct distance matrix (e.g. a graph/table)
  4. Run built-in test cases (different input scenarios)
  5. Exit
""")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            explain_algorithm()

        elif choice == "2":
            cities = get_cities()
            names = [c["name"] for c in cities]
            while True:
                start_name = input(f"Choose a starting city {names}: ").strip()
                if start_name in names:
                    break
                print("City not found, try again.")
            solve_and_print(cities, start_name)

        elif choice == "3":
            cities, matrix = get_matrix_input()
            names = [c["name"] for c in cities]
            while True:
                start_name = input(f"Choose a starting city {names}: ").strip()
                if start_name in names:
                    break
                print("City not found, try again.")
            solve_and_print(cities, start_name, matrix=matrix)

        elif choice == "4":
            run_built_in_tests()

        elif choice == "5":
            print("Goodbye.")
            break

        else:
            print("Invalid option, please choose 1-5.")


if __name__ == "__main__":
    main()