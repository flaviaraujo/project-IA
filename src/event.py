from src.graph import graph
from src.graph.graph import Graph
from src.supply import Supply

# Unidade de tempo passada por vêz
CLOCK_CYCLE = 5
# Tempo necessário para reeabastecer os suprimentos daquele nodo
SUPPLY_REFILL_RATE = 20
# Quantidade a reabastecer de COMBUSTIVEL
REFUEL_AMOUNT = 50
# Quantidade a reabastecer de SUPRIMENTOS
FOOD_AMOUNT = 450
WATER_AMOUNT = 100
SOSKIT_AMOUNT = 20


def handle_catastrophe(time, node, map_graph: Graph, catastrophe):
    print(f"Time remaining for catastrophe on node {node['id']}: {catastrophe.time - time}")

    if catastrophe.time - time <= 0:
        if catastrophe.supplies_demand > 0:
            map_graph.destructive_nodes.add(node)
            print(f"Catastrophe on node {node['id']} unresolved! Destroying node.")

    else:
        vehicles = node.get("vehicles", [])
        for vehicle in vehicles:
            for supply, amount in vehicle.cargo_contents.items():
                if supply in catastrophe.supplies_demand:
                    delivered_amount = min(amount, catastrophe.supplies_demand[supply])
                    catastrophe.supplies_demand[supply] -= delivered_amount
                    vehicle.cargo_contents[supply] -= delivered_amount
                    print(f"Delivered {delivered_amount} of {supply} to catastrophe on node {node['id']}.")
                    if catastrophe.supplies_demand[supply] <= 0:
                        del catastrophe.supplies_demand[supply]


def handle_vehicle(time, node, map_graph: Graph, vehicle):
    print(f"Vehicle {vehicle.name} is on node {node['id']}.")

    if vehicle.action.action_type == "wait":
        print(f"{vehicle.name} is waiting on node {node['id']}.")

    elif vehicle.action.action_type == "supply":
        for supply, amount in vehicle.cargo_contents.items():
            if supply in node['supplies']:
                node['supplies'][supply].amount += amount
            else:
                node['supplies'][supply] = Supply(supply, amount)
        vehicle.cargo_contents.clear()
        vehicle.cargo = 0
        print(f"{vehicle.name} has delivered supplies on node {node['id']}.")


    elif vehicle.action.action_type == "restock":
        total_cargo_space = vehicle.cargo_capacity - vehicle.cargo
        for supply_name, supply in node['supplies'].items():
            if total_cargo_space <= 0:
                break
            amount_to_load = min(supply.amount, total_cargo_space)
            if supply_name in vehicle.cargo_contents:
                vehicle.cargo_contents[supply_name] += amount_to_load

            else:
                vehicle.cargo_contents[supply_name] = amount_to_load
            supply.amount -= amount_to_load
            vehicle.cargo += amount_to_load
            total_cargo_space -= amount_to_load
        print(
            f"{vehicle.name} has restocked supplies on node {node['id']}. Current cargo: {vehicle.cargo_contents}")


    elif vehicle.action.action_type == "fuel":
        if "fuel" in node['supplies']:
            fuel_available = node['supplies']['fuel'].amount
            fuel_needed = vehicle.tank_capacity - vehicle.tank
            fuel_to_transfer = min(fuel_available, fuel_needed)
            vehicle.tank += fuel_to_transfer
            node['supplies']['fuel'].amount -= fuel_to_transfer
            print(f"{vehicle.name} has refueled with {fuel_to_transfer} units of fuel on node {node['id']}.")
        else:
            print(f"No fuel available on node {node['id']} for {vehicle.name}.")

    elif vehicle.action.action_time == time:
        target_node_id = vehicle.action
        if vehicle.can_travel(vehicle.travel_method, node['access_level'], vehicle.action.distance_traveled):
            if vehicle.target_node_id in map_graph.nodes:
                node['vehicles'].remove(vehicle)
                vehicle.travel(vehicle.travel_method, node['access_level'], vehicle.action.distance_traveled)
                target_node = map_graph.nodes[vehicle.target_node_id]
                target_node['vehicles'].append(vehicle)
                print(f"{vehicle.name} has moved from node {node['id']} to node {target_node_id}.")
        else:
            print(f"{vehicle.name} cannot move to {target_node_id}")


def handle_fuel(time, node):
    if time % SUPPLY_REFILL_RATE == 0:
        node.fuel += REFUEL_AMOUNT


def handle_supply(time, supply):
    if time % SUPPLY_REFILL_RATE == 0:
        if supply == "food":
            supply.amount += FOOD_AMOUNT
        elif supply == "water":
            supply.amount += WATER_AMOUNT
        elif supply == "soskit":
            supply.amount += SOSKIT_AMOUNT



class Event:
    def __init__(self):
        self.time = 0

    def __str__(self):
        return f"{{ Current Time: {self.time} }}"

    def execute(self, graph: Graph):
        self.time += 5
        print(self.__str__())

        for node_id, node_data in graph.nodes.items():
            catastrophe = node_data.get("catastrophe")
            if catastrophe:
                handle_catastrophe(self.time, node_id, catastrophe)

            vehicles = node_data.get("vehicles", [])
            for vehicle in vehicles:
                handle_vehicle(self.time, node_id, graph, vehicle)

            handle_fuel(self.time, node_id)

            supplies = node_data.get("supplies", {})
            for supply_name, supply in supplies.items():
                handle_supply(self.time, supply)

        return self.time
