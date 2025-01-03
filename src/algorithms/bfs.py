# BFS search algorithm implementation

from graph.graph import Graph
from vehicle     import Vehicle
from operation   import Operation

from math        import ceil
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

    # Copy the graph to avoid modifying the original one
    graph = graph.copy()

    # Copy the vehicle to avoid modifying the original one
    vehicle = vehicle.copy()

    # First operation: start
    start_op = Operation(0, "start", vehicle=vehicle.name, node=start.name)

    # Load the supplies to maximize the catastrophe resolution
    supplies_loaded, _ = vehicle.load_supplies_for_catastrophe(goal.catastrophe.supplies_demand)
    load_op = Operation(0, "load", vehicle=vehicle.name, node=start.name, supplies=supplies_loaded)

    # Initialize the queue with tuples (node, operations, time)
    queue = Queue()
    queue.put((start, [start_op, load_op], 0))

    # Keep track of visited nodes
    visited = set()
    visited.add(start.name)

    while not queue.empty():
        node, operations, current_time = queue.get()

        # Solution found
        if node == goal:
            # Append the "drop supplies" operation
            cargo_supplied, remaining_cargo = node.catastrophe.supply(vehicle.cargo_contents)
            drop_op = Operation(current_time, "drop", vehicle=vehicle.name,
                                node=node.name, supplies=cargo_supplied)
            operations.append(drop_op)

            # Update the vehicle's cargo contents
            vehicle.cargo_contents = remaining_cargo
            vehicle.cargo = sum(s.amount for s in vehicle.cargo_contents)

            # Check if the catastrophe is fully resolved
            # Otherwise:
            # 1. Go to neerest node
            # 2. Fuel if needed
            # 3. Load the supplies min(demand, cargo_capacity)
            # 4. Go to the catastrophe
            # 5. Drop the supplies
            # 6. Repeat until the catastrophe is resolved

            # Find the nearest node to the catastrophe
            neighbors = []
            for prox, edge in graph.graph[node]:
                _, _, e_travel_method, e_access_level = edge
                if not vehicle.is_travel_possible(e_travel_method, e_access_level):
                    continue

                neighbors.append((prox, edge))

            # If there are no neighbors the vehicle can't help the catastrophe
            if not neighbors:
                fuel_consumption = ceil(sum([op.fuel_consumed or 0 for op in operations]) * 100) / 100
                return operations, fuel_consumption

            nearest_node, edge = min(neighbors, key=lambda x: x[1][0])

            # Unpack the nearest the edge from the neerest node to the catastrophe
            e_distance, _, e_travel_method, e_access_level = edge

            while not node.catastrophe.is_resolved():

                if node.catastrophe.has_time_expired(current_time):
                    break

                tmp_vehicle = vehicle.copy()
                tmp_operations = [op.copy() for op in operations]
                tmp_current_time = current_time

                # Travel to the nearest node
                travel_time, fuel_used = tmp_vehicle.travel(e_distance)
                start_time_travel = tmp_current_time
                tmp_current_time += travel_time

                if tmp_current_time >= response_time:
                    break

                travel_op = Operation(start_time_travel, "move", vehicle=vehicle.name,
                                      node=nearest_node.name, fuel_consumed=fuel_used)
                tmp_operations.append(travel_op)

                # Refuel if necessary
                if not tmp_vehicle.has_enough_fuel(e_distance):
                    fuel_needed = tmp_vehicle.calculate_fuel_needed(e_distance)
                    refuel_op = Operation(current_time, "refuel", vehicle=vehicle.name,
                                          node=nearest_node.name, fuel=fuel_needed)

                    _, refuel_time = tmp_vehicle.refuel(fuel_needed)
                    tmp_current_time += refuel_time
                    tmp_operations.append(refuel_op)

                    if tmp_current_time >= response_time:
                        break

                # Load the supplies
                supplies_loaded, _ = tmp_vehicle.load_supplies_for_catastrophe(node.catastrophe.supplies_demand)
                load_op = Operation(current_time, "load", vehicle=vehicle.name,
                                    node=nearest_node.name, supplies=supplies_loaded)
                tmp_operations.append(load_op)

                # Travel to the catastrophe
                travel_time, fuel_used = tmp_vehicle.travel(e_distance)
                start_time_travel = tmp_current_time
                tmp_current_time += travel_time

                if tmp_current_time >= response_time:
                    break

                travel_op = Operation(start_time_travel, "move", vehicle=vehicle.name,
                                      node=node.name, fuel_consumed=fuel_used)
                tmp_operations.append(travel_op)

                # Drop the supplies
                cargo_supplied, remaining_cargo = node.catastrophe.supply(tmp_vehicle.cargo_contents)

                drop_op = Operation(current_time, "drop", vehicle=vehicle.name,
                                    node=node.name, supplies=cargo_supplied)
                tmp_operations.append(drop_op)

                # Update the vehicle's cargo contents
                tmp_vehicle.cargo_contents = remaining_cargo
                tmp_vehicle.cargo = sum(s.amount for s in tmp_vehicle.cargo_contents)

                # Update the state
                vehicle = tmp_vehicle
                operations = tmp_operations
                current_time = tmp_current_time

            fuel_consumption = ceil(sum([op.fuel_consumed or 0 for op in operations]) * 100) / 100
            return operations, fuel_consumption

        # Explore neighbors
        for prox, (e_distance, _, e_travel_method, e_access_level) in graph.graph[node]:

            # TODO consider the supplies with expiration in the vehicle

            # Clone the vehicle state for this edge
            tmp_vehicle = vehicle.copy()
            tmp_operations = [op.copy() for op in operations]
            tmp_current_time = current_time

            # If the response time for the catastrophe has passed, stop processing
            if tmp_current_time >= response_time:
                continue

            # Check if the vehicle can access the node
            if not tmp_vehicle.is_travel_possible(e_travel_method, e_access_level):
                continue

            # Check if the node has already been visited
            # NOTE the check is made here do to the multiple edges between nodes
            # this way unnecessary visits are avoided
            if prox.name in visited:
                continue

            visited.add(prox.name)

            # Ensure the vehicle has enough fuel
            if not tmp_vehicle.has_enough_fuel(e_distance):
                # Refuel if necessary
                fuel_needed = tmp_vehicle.calculate_fuel_needed(e_distance)

                refuel_op = Operation(tmp_current_time, "refuel", vehicle=tmp_vehicle.name,
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
            start_time_travel = tmp_current_time
            tmp_current_time += travel_time

            # Check response time after traveling
            if tmp_current_time >= response_time:
                continue

            # Restore the state when adding the neighbor to the queue
            vehicle = tmp_vehicle
            operations = tmp_operations
            current_time = tmp_current_time

            # Add the neighbor to the queue
            travel_op = Operation(start_time_travel, "move", vehicle=tmp_vehicle.name,
                                  node=prox.name, fuel_consumed=fuel_used)
            queue.put((prox, tmp_operations + [travel_op], tmp_current_time))

    # No solution found
    return None
