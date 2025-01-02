# BFS search algorithm implementation

from graph.graph import Graph
from vehicle     import Vehicle
from operation   import Operation

from queue       import Queue


def search(graph: Graph,
           vehicle: Vehicle,
           response_time: int,
           start_name: str,
           goal_name: str) -> list[Operation]:

    if isinstance(start_name, str):
        start = next((n for n in graph.nodes if n.name == start_name), None)

    if isinstance(goal_name, str):
        goal = next((n for n in graph.nodes if n.name == goal_name), None)

    if start is None or goal is None:
        return None

    # Copy the vehicle to avoid modifying the original one
    vehicle = vehicle.copy()

    # First operation: start
    start_op = Operation("start", vehicle=vehicle.name, node=start.name)

    # Initialize the queue with tuples (node, operations, time, fuel_consumption)
    queue = Queue()
    queue.put((start, [start_op], 0, 0))  # Start node, operations, time, fuel consumption

    # Keep track of visited nodes
    visited = set()

    while not queue.empty():
        node, operations, current_time, fuel_consumption = queue.get()

        # Solution found
        if node == goal:
            # TODO: append the "drop supplies" operation
            # NOTE copy the graph to avoid modifying the original one
            # TODO: check if the catastrophe is fully resolved
            # otherwise:
            # 1. Go to neerest node
            # 2. Fuel if needed
            # 3. Load the supplies min(demand, cargo_capacity)
            # 4. Go to the catastrophe
            # 5. Drop the supplies
            # 6. Repeat until the catastrophe is resolved
            return operations, fuel_consumption

        # Explore neighbors
        for prox, (e_distance, _, e_travel_method, e_access_level) in graph.graph[node]:

            # Clone the vehicle state for this edge
            tmp_vehicle = vehicle.copy()
            tmp_operations = operations.copy()
            tmp_current_time = current_time
            tmp_fuel_consumption = fuel_consumption

            # If the response time for the catastrophe has passed, stop processing
            if tmp_current_time >= response_time:
                continue

            # Check if the vehicle can access the node
            if not tmp_vehicle.is_travel_possible(e_travel_method, e_access_level):
                continue

            # Check if the node has already been visited
            # NOTE the check is made here do to the multiple edges between nodes
            # this way unnecessary visits are avoided
            if prox in visited:
                continue

            visited.add(prox)

            # Ensure the vehicle has enough fuel
            if not tmp_vehicle.has_enough_fuel(e_distance):
                # Refuel if necessary
                fuel_needed = tmp_vehicle.calculate_fuel_needed(e_distance)
                refuel_op = Operation("refuel", vehicle=tmp_vehicle.name,
                                      node=node.name, fuel=fuel_needed)

                # refuel the ammount needed in order to reach the node
                # NOTE ignores fuel left in node as it is not considered in this model
                _, refuel_time = tmp_vehicle.refuel(fuel_needed)
                tmp_current_time += refuel_time
                tmp_operations.append(refuel_op)

                # Check response time after refueling
                if tmp_current_time >= response_time:
                    continue

            # Travel to the next node
            travel_time, fuel_used = tmp_vehicle.travel(e_distance)
            tmp_current_time += travel_time
            tmp_fuel_consumption += fuel_used

            # Check response time after traveling
            if tmp_current_time >= response_time:
                continue

            # Restore the state when adding the neighbor to the queue
            vehicle = tmp_vehicle
            operations = tmp_operations
            current_time = tmp_current_time
            fuel_consumption = tmp_fuel_consumption

            # Add the neighbor to the queue
            travel_op = Operation("move", vehicle=tmp_vehicle.name, node=prox.name)
            queue.put((prox, tmp_operations + [travel_op], tmp_current_time, tmp_fuel_consumption))

    # No solution found
    return None
