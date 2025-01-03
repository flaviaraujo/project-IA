from heapq import heappush, heappop

def calculate_travel_time_and_fuel(graph, start_node, end_node, vehicle):
    if isinstance(start_node, str):
        start_node = next((n for n in graph.nodes if n.name == start_node), None)

    if isinstance(end_node, str):
        end_node = next((n for n in graph.nodes if n.name == end_node), None)

    if start_node not in graph.nodes or end_node not in graph.nodes:
        return None, None, None

    # Priority queue for Dijkstra's algorithm
    priority_queue = [(0, 0, start_node, [])]  # (current_distance, current_fuel, current_node, path)
    distances = {node: float('inf') for node in graph.nodes}
    distances[start_node] = 0

    visited = set()

    while priority_queue:
        current_distance, current_fuel, current_node, path = heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)
        path = path + [current_node.name]

        if current_node == end_node:
            return current_distance, current_fuel, path

        for neighbor, (distance, speed_mult, travel_method, access_level) in graph.graph[current_node]:
            if not vehicle.is_travel_possible(travel_method, access_level):
                continue

            new_distance = current_distance + distance / vehicle.speed
            new_fuel = current_fuel + vehicle.calculate_fuel_needed(distance)

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heappush(priority_queue, (new_distance, new_fuel, neighbor, path))

    return float('inf'), float('inf'), []

def find_vehicles_for_catastrophe(graph, catastrophe_node, vehicles, max_response_time):
    accessible_vehicles = []

    for vehicle in vehicles:
        travel_time, fuel_used, path = calculate_travel_time_and_fuel(graph, vehicle.current_node, catastrophe_node, vehicle)
        if travel_time <= max_response_time:
            accessible_vehicles.append((vehicle.name, path, fuel_used))

    return accessible_vehicles

def update_catastrophe_data(graph, catastrophes, vehicles):
    for node in graph.nodes:
        if node.catastrophe:
            node.catastrophe.accessible_vehicles = find_vehicles_for_catastrophe(graph, node, vehicles, node.catastrophe.time)