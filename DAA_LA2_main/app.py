from flask import Flask, render_template, request
import time

app = Flask(__name__)

# List of cities
cities = ["Mumbai", "Pune", "Goa", "Hyderabad", "Bengaluru", "Chennai", "Delhi", "Kolkata"]

# Cost routes (₹)   BY Anshul Shahu
cost_routes = {
    ("Mumbai", "Pune"): 200,
    ("Pune", "Goa"): 300,
    ("Goa", "Hyderabad"): 400,
    ("Hyderabad", "Bengaluru"): 250,
    ("Bengaluru", "Chennai"): 200,
    ("Chennai", "Kolkata"): 600,
    ("Delhi", "Kolkata"): 700,
    ("Delhi", "Mumbai"): 500
}

# Time routes (hours)   By Krishna Deole
time_routes = {
    ("Mumbai", "Pune"): 3,
    ("Pune", "Goa"): 6,
    ("Goa", "Hyderabad"): 8,
    ("Hyderabad", "Bengaluru"): 5,
    ("Bengaluru", "Chennai"): 4,
    ("Chennai", "Kolkata"): 10,
    ("Delhi", "Kolkata"): 9,
    ("Delhi", "Mumbai"): 12
}

# Graph for Prim’s Algorithm  By Mandar Amte
graph = {
    "Mumbai": {"Pune": 200, "Delhi": 500},
    "Pune": {"Mumbai": 200, "Goa": 300},
    "Goa": {"Pune": 300, "Hyderabad": 400},
    "Hyderabad": {"Goa": 400, "Bengaluru": 250},
    "Bengaluru": {"Hyderabad": 250, "Chennai": 200},
    "Chennai": {"Bengaluru": 200, "Kolkata": 600},
    "Delhi": {"Mumbai": 500, "Kolkata": 700},
    "Kolkata": {"Chennai": 600, "Delhi": 700}
}

# -----------------------------
# 1️⃣ Find Route by Cost          BY ANSHUL SHAHU
# -----------------------------
def find_route_cost(source, destination):
    path = [source]
    total_cost = 0
    current = source

    for _ in range(100):
        if current == destination:
            return path, total_cost

        moved = False
        for (a, b), cost in cost_routes.items():
            if a == current and b not in path:
                path.append(b)
                total_cost += cost
                current = b
                moved = True
                break
            if b == current and a not in path:
                path.append(a)
                total_cost += cost
                current = a
                moved = True
                break
        if not moved:
            break

    return (path, total_cost) if current == destination else (None, None)


# -----------------------------
# 2️⃣ Find Route by Time          BY Krishna Deole
# -----------------------------
def find_route_time(source, destination):
    path = [source]                # store route path
    total_time = 0                 # total time taken
    current = source               # start from source node

    for _ in range(100):           # limit to avoid infinite loop
        if current == destination: # if reached destination stop
            return path, total_time

        moved = False              # check if movement possible

        for (a, b), t in time_routes.items():  # check each edge
            if a == current and b not in path: # if next node is b
                path.append(b)
                total_time += t
                current = b
                moved = True
                break

            if b == current and a not in path: # if next node is a
                path.append(a)
                total_time += t
                current = a
                moved = True
                break

        if not moved:             # no movement → no route forward
            break

    return (path, total_time) if current == destination else (None, None) # return result

# -----------------------------
# 3️⃣ Prim’s Algorithm (MST)      BY MMANDAR AMTE
# -----------------------------
def prims_algorithm(start_city):
    visited = set()
    edges = []
    total_cost = 0

    visited.add(start_city)

    while len(visited) < len(graph):
        min_edge = None
        min_cost = float('inf')

        for city in visited:
            for neighbor, cost in graph[city].items():
                if neighbor not in visited and cost < min_cost:
                    min_edge = (city, neighbor)
                    min_cost = cost

        if not min_edge:
            break

        edges.append((min_edge[0], min_edge[1], min_cost))
        total_cost += min_cost
        visited.add(min_edge[1])

    return edges, total_cost


# -----------------------------
# 🌐 Main Route
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    result_text = None
    cost_data, time_data, mst_data = {}, {}, {}
    comparison = []

    if request.method == "POST":
        source = request.form.get("source")
        destination = request.form.get("destination")

        # ---------- COST FUNCTION ----------
        start = time.perf_counter()
        cost_path, total_cost = find_route_cost(source, destination)
        end = time.perf_counter()
        cost_time = (end - start) * 1000  # ms

        if cost_path:
            cost_data = {
                "path": cost_path,
                "value": total_cost,
                "exec_time": round(cost_time, 3)
            }

        # ---------- TIME FUNCTION ----------
        start = time.perf_counter()
        time_path, total_time = find_route_time(source, destination)
        end = time.perf_counter()
        algo_time = (end - start) * 1000  # ms

        if time_path:
            time_data = {
                "path": time_path,
                "value": total_time,
                "exec_time": round(algo_time, 3)
            }

        # ---------- PRIM'S FUNCTION ----------
        start = time.perf_counter()
        edges, mst_cost = prims_algorithm(source)
        end = time.perf_counter()
        mst_exec = (end - start) * 1000  # ms

        mst_data = {
            "edges": edges,
            "value": mst_cost,
            "exec_time": round(mst_exec, 3)
        }

        # ---------- COMPARISON ----------
        comparison = [
            {"Algorithm": "Delivery Cost Finder", "Time (ms)": cost_data["exec_time"]},
            {"Algorithm": "Delivery Time Finder", "Time (ms)": time_data["exec_time"]},
            {"Algorithm": "Prim’s MST", "Time (ms)": mst_data["exec_time"]},
        ]

    return render_template(
        "index.html",
        cities=cities,
        cost_data=cost_data,
        time_data=time_data,
        mst_data=mst_data,
        comparison=comparison
    )


if __name__ == "__main__":
    app.run(debug=True)


