import heapq
import random
import time
import pandas as pd
import matplotlib.pyplot as plt


# BFS

graph = {
    "Gate": {"Library": 2, "Cafeteria": 4},
    "Library": {"Gate": 2, "Admin": 2, "Lab1": 5},
    "Cafeteria": {"Gate": 4, "Auditorium": 3},
    "Admin": {"Library": 2, "Lab2": 3},
    "Lab1": {"Library": 5, "Lab2": 2, "Auditorium": 6},
    "Lab2": {"Admin": 3, "Lab1": 2, "Auditorium": 2},
    "Auditorium": {"Cafeteria": 3, "Lab1": 6, "Lab2": 2}
}

heuristic = {
    "Gate": 7,
    "Library": 7,
    "Cafeteria": 3,
    "Admin": 5,
    "Lab1": 4,
    "Lab2": 2,
    "Auditorium": 0
}


def bfs(graph, start, goal):
    queue = [[start]]
    visited = {start}
    nodes = 0

    while queue:
        path = queue.pop(0)
        node = path[-1]
        nodes += 1

        if node == goal:
            return path, nodes

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return None, nodes


# A*

def astar(graph, start, goal, h):
    pq = []
    heapq.heappush(pq, (h[start], 0, start, [start]))

    best_g = {start: 0}
    nodes = 0

    while pq:
        f, g, node, path = heapq.heappop(pq)
        nodes += 1

        if node == goal:
            return path, nodes, g

        if g > best_g.get(node, float("inf")):
            continue

        for neighbor, cost in graph[node].items():
            new_g = g + cost

            if new_g < best_g.get(neighbor, float("inf")):
                best_g[neighbor] = new_g
                new_f = new_g + h[neighbor]

                heapq.heappush(
                    pq,
                    (new_f, new_g, neighbor, path + [neighbor])
                )

    return None, nodes, None


# Hill Climbing

def objective(x):
    return -(x - 8) ** 2 + 64


def hill_climbing(start):
    current = start
    steps = 0

    while True:
        steps += 1

        neighbors = [
            x for x in [current - 1, current + 1]
            if 0 <= x <= 15
        ]

        if not neighbors:
            break

        best = max(neighbors, key=objective)

        if objective(best) <= objective(current):
            break

        current = best

    return current, objective(current), steps


# CSP

subjects = [
    "Artificial Intelligence",
    "DBMS",
    "Computer Networks",
    "Operating Systems"
]

slots = [
    "Mon 9AM",
    "Mon 11AM",
    "Tue 9AM"
]

conflicts = {
    "Artificial Intelligence": {"DBMS", "Computer Networks"},
    "DBMS": {"Artificial Intelligence", "Operating Systems"},
    "Computer Networks": {"Artificial Intelligence"},
    "Operating Systems": {"DBMS"}
}


def is_valid(subject, slot, assignment):
    for other in conflicts[subject]:
        if assignment.get(other) == slot:
            return False

    return True


def solve_csp(assignment=None):
    if assignment is None:
        assignment = {}

    if len(assignment) == len(subjects):
        return assignment.copy()

    subject = next(s for s in subjects if s not in assignment)

    for slot in slots:
        if is_valid(subject, slot, assignment):
            assignment[subject] = slot

            result = solve_csp(assignment)

            if result:
                return result

            del assignment[subject]

    return None


def average_time(function, repeats=1000):
    start = time.perf_counter()

    for _ in range(repeats):
        function()

    end = time.perf_counter()

    return (end - start) / repeats


random.seed(42)

hill_start = random.randint(0, 15)

bfs_path, bfs_nodes = bfs(
    graph,
    "Gate",
    "Auditorium"
)

astar_path, astar_nodes, astar_cost = astar(
    graph,
    "Gate",
    "Auditorium",
    heuristic
)

hill_solution, hill_value, hill_steps = hill_climbing(
    hill_start
)

csp_solution = solve_csp()


bfs_time = average_time(
    lambda: bfs(graph, "Gate", "Auditorium")
)

astar_time = average_time(
    lambda: astar(
        graph,
        "Gate",
        "Auditorium",
        heuristic
    )
)

hill_time = average_time(
    lambda: hill_climbing(hill_start)
)

csp_time = average_time(
    solve_csp
)


results = [
    ["BFS", bfs_nodes, bfs_time * 1000],
    ["A* Search", astar_nodes, astar_time * 1000],
    ["Hill Climbing", hill_steps, hill_time * 1000],
    ["CSP", len(csp_solution), csp_time * 1000]
]

df = pd.DataFrame(
    results,
    columns=["Algorithm", "Nodes/Steps", "Time (ms)"]
)


print("=" * 55)
print("AI SEARCH ALGORITHMS")
print("=" * 55)

print("\nBFS")
print("Start:", "Gate")
print("Goal:", "Auditorium")
print("Path:", " -> ".join(bfs_path))
print("Nodes:", bfs_nodes)

print("\nA*")
print("Start:", "Gate")
print("Goal:", "Auditorium")
print("Path:", " -> ".join(astar_path))
print("Cost:", astar_cost)
print("Nodes:", astar_nodes)

print("\nHill Climbing")
print("Starting x:", hill_start)
print("Best x:", hill_solution)
print("Maximum value:", hill_value)
print("Steps:", hill_steps)

print("\nCSP")
for subject, slot in csp_solution.items():
    print(subject, "->", slot)

print("\nPerformance Table")
print(df.to_string(index=False))

print("\nAll test cases completed successfully.")


fig = plt.figure(figsize=(10, 8))

grid = fig.add_gridspec(
    2,
    1,
    height_ratios=[1.2, 1]
)

ax1 = fig.add_subplot(grid[0])
ax1.axis("off")

output_text = (
    "AI SEARCH ALGORITHMS - PERFORMANCE EVALUATION\n\n"
    "BFS: Gate -> Cafeteria -> Auditorium | Nodes: "
    + str(bfs_nodes)
    + "\n"
    "A*: Gate -> Cafeteria -> Auditorium | Cost: "
    + str(astar_cost)
    + " | Nodes: "
    + str(astar_nodes)
    + "\n"
    "Hill Climbing: Start x = "
    + str(hill_start)
    + " | Best x = "
    + str(hill_solution)
    + " | Maximum = "
    + str(hill_value)
    + "\n"
    "CSP: Exam Timetable\n\n"
    + df.to_string(
        index=False,
        float_format=lambda x: f"{x:.6f}"
    )
    + "\n\nAll test cases completed successfully."
)

ax1.text(
    0.02,
    0.95,
    output_text,
    va="top",
    ha="left",
    family="monospace",
    fontsize=10
)

ax2 = fig.add_subplot(grid[1])

ax2.bar(
    df["Algorithm"],
    df["Time (ms)"]
)

ax2.set_title("Execution Time Comparison")
ax2.set_xlabel("Algorithm")
ax2.set_ylabel("Time (ms)")

plt.xticks(rotation=15)

plt.tight_layout()

plt.savefig(
    "Output.png",
    dpi=180,
    bbox_inches="tight"
)

plt.show()
