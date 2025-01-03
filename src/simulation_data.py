from mission_planner import MissionPlanner
from catastrophe     import Catastrophe
from vehicle         import Vehicle
# from supply          import Supply
from graph.graph     import Graph

from vehicle import (
    LOW_ACCESS_LEVEL,
    MEDIUM_ACCESS_LEVEL,
    HIGH_ACCESS_LEVEL
)

from graph.heurisitics import (
    heuristic_fn1,
    heuristic_fn2,
    heuristic_fn3
)


def init_simulation(option: int) -> (MissionPlanner, int):
    match option:
        case 1:
            # Description: city with 10 nodes

            ###
            # Create catastrophes
            ###

            catastrophes = {
                "B": Catastrophe(600, {"food": 300, "water": 200}),
                "F": Catastrophe(300, {"food": 300, "water": 500, "soskit": 50}),
                "I": Catastrophe(400, {"medicine": 200, "water": 300}),
            }

            ###
            # Create the vehicles
            ###

            fleet = {
                "A": [
                    Vehicle("Bike1", "motorcycle"),
                    Vehicle("Car1", "car"),
                    Vehicle("Truck1", "truck"),
                    Vehicle("Drone1", "drone")
                ],
                "D": [
                    Vehicle("Drone1", "drone"),
                    Vehicle("Helicopter1", "helicopter"),
                    Vehicle("Boat1", "small_boat")
                ],
                "H": [
                    Vehicle("Car2", "car"),
                    Vehicle("Truck2", "truck"),
                ]
            }

            ###
            # Create the supplies
            ###

            # NOTE Currently assuming that the supplies are infinite
            supplies = {
                # "A": {
                #     "food":     Supply("food",      500, perishable_time=600),
                #     "water":    Supply("water",    1000),
                #     "soskit":   Supply("soskit",    100)
                # },
                # "D": {
                #     "medicine": Supply("medicine",  200, perishable_time=500),
                #     "water":    Supply("water",     300),
                # },
                # "H": {
                #     "food":     Supply("food",      600, perishable_time=400),
                #     "water":    Supply("water",     500),
                #     "medicine": Supply("medicine",  300)
                # }
            }

            ###
            # Create the graph
            ###

            graph = Graph(directed=False)

            # Add the nodes
            for node, fuel in [
                ("A", 50),
                ("B", 0),
                ("C", 10),
                ("D", 25),
                ("E", 15),
                ("F", 0),
                ("G", 10),
                ("H", 20),
                ("I", 0),
                ("J", 30)
            ]:
                catastrophe = catastrophes.get(node, None)
                vehicles = fleet.get(node, [])
                starting_supplies = supplies.get(node, {})
                graph.add_node(node,
                               fuel,
                               catastrophe,
                               vehicles,
                               starting_supplies)

            # Add the edges
            graph.add_edge("A", "B", 20, 1.00, "air",   MEDIUM_ACCESS_LEVEL)
            graph.add_edge("A", "C", 30, 0.85, "land",  MEDIUM_ACCESS_LEVEL)
            graph.add_edge("A", "D", 40, 0.80, "water", HIGH_ACCESS_LEVEL)
            graph.add_edge("A", "E", 50, 0.70, "land",  HIGH_ACCESS_LEVEL)
            graph.add_edge("B", "C", 25, 0.75, "land",  MEDIUM_ACCESS_LEVEL)
            graph.add_edge("B", "D", 30, 0.90, "air",   MEDIUM_ACCESS_LEVEL)
            graph.add_edge("B", "D", 35, 0.70, "water", MEDIUM_ACCESS_LEVEL)
            graph.add_edge("B", "F", 45, 0.95, "air",   MEDIUM_ACCESS_LEVEL)
            graph.add_edge("C", "E", 30, 1.00, "land",  LOW_ACCESS_LEVEL)
            graph.add_edge("C", "F", 60, 1.00, "land",  LOW_ACCESS_LEVEL)
            graph.add_edge("D", "G", 30, 0.80, "water", MEDIUM_ACCESS_LEVEL)
            graph.add_edge("D", "H", 25, 0.70, "air",   MEDIUM_ACCESS_LEVEL)
            graph.add_edge("E", "F", 20, 1.00, "land",  LOW_ACCESS_LEVEL)
            graph.add_edge("E", "H", 40, 0.75, "land",  MEDIUM_ACCESS_LEVEL)
            graph.add_edge("F", "I", 50, 1.00, "land",  LOW_ACCESS_LEVEL)
            graph.add_edge("G", "H", 20, 1.00, "land",  LOW_ACCESS_LEVEL)
            graph.add_edge("G", "I", 40, 0.85, "land",  MEDIUM_ACCESS_LEVEL)
            graph.add_edge("H", "J", 30, 0.85, "land",  MEDIUM_ACCESS_LEVEL)
            graph.add_edge("F", "I", 30, 0.80, "air",   HIGH_ACCESS_LEVEL)
            graph.add_edge("I", "J", 35, 0.80, "land",  MEDIUM_ACCESS_LEVEL)

            # Add heuristics values to nodes
            heuristic_option = 1
            heuristic_fn1({
                "graph": graph,
                "catastrophes": catastrophes,
                "vehicles": sum(fleet.values(), [])
            })

            # Create destructive nodes conditions
            destructive_nodes = {
                "C": 300,
                "G": 400
            }
            graph.destructive_nodes = destructive_nodes

            # Create destructive edges conditions
            destructive_edges = {
                ("A", "D"): 350,
                ("E", "H"): 250,
                ("F", "I"): 200
            }
            graph.destructive_edges = destructive_edges

            # Return the MissionPlanner object
            return MissionPlanner(graph, catastrophes, fleet, supplies), heuristic_option

        case 2:
            # Description: Azores archipelago with 9 islands

            ###
            # Create catastrophes
            ###

            catastrophes = {
                "Sao Miguel":  Catastrophe(500, {"food": 200, "water": 100}),
                "Santa Maria": Catastrophe(400, {"medicine": 150, "water": 200}),
                "Faial":       Catastrophe(300, {"food": 100, "soskit": 50}),
                "Pico":        Catastrophe(600, {"water": 400, "medicine": 300}),
            }

            ###
            # Create the vehicles
            ###

            fleet = {
                "Terceira": [
                    Vehicle("Boat1", "small_boat"),
                    Vehicle("Boat2", "medium_boat"),
                ],
                "Graciosa": [
                    Vehicle("Airplane1", "airplane"),
                    Vehicle("Helicopter1", "helicopter"),
                ]
            }

            ###
            # Create the supplies
            ###

            # NOTE Currently assuming that the supplies are infinite
            supplies = {
                # "Terceira": {
                #     "food":     Supply("food",     400, perishable_time=500),
                #     "water":    Supply("water",    800),
                #     "soskit":   Supply("soskit",   100),
                # },
                # "Sao Jorge": {
                #     "medicine": Supply("medicine", 300, perishable_time=600),
                #     "water":    Supply("water",    500),
                # },
                # "Corvo": {
                #     "food":     Supply("food",     600, perishable_time=400),
                #     "water":    Supply("water",    700),
                # }
            }

            ###
            # Create the graph
            ###

            graph = Graph(directed=False)

            # Add the islands (nodes)
            for node, fuel in [
                ("Sao Miguel",  50),
                ("Santa Maria", 40),
                ("Faial",       30),
                ("Pico",        60),
                ("Flores",      20),
                ("Corvo",       50),
                ("Terceira",    30),
                ("Graciosa",    40),
                ("Sao Jorge",   25)
            ]:
                catastrophe = catastrophes.get(node, None)
                vehicles = fleet.get(node, [])
                starting_supplies = supplies.get(node, {})
                graph.add_node(node,
                               fuel,
                               catastrophe,
                               vehicles,
                               starting_supplies)

            # Add the edges
            graph.add_edge("Sao Miguel",  "Santa Maria",   81, 0.75, "water", MEDIUM_ACCESS_LEVEL)
            graph.add_edge("Sao Miguel",  "Santa Maria",   81, 0.60, "air",   LOW_ACCESS_LEVEL)

            graph.add_edge("Sao Miguel",  "Terceira",     144, 0.75, "water", MEDIUM_ACCESS_LEVEL)
            graph.add_edge("Sao Miguel",  "Terceira",     144, 0.60, "air",   LOW_ACCESS_LEVEL)

            graph.add_edge("Santa Maria", "Terceira",     175, 0.80, "water", MEDIUM_ACCESS_LEVEL)
            graph.add_edge("Santa Maria", "Terceira",     175, 0.65, "air",   LOW_ACCESS_LEVEL)

            graph.add_edge("Terceira",    "Graciosa",      81, 0.85, "water", MEDIUM_ACCESS_LEVEL)
            graph.add_edge("Terceira",    "Graciosa",      81, 0.70, "air",   LOW_ACCESS_LEVEL)

            graph.add_edge("Graciosa",    "Sao Jorge",     42, 0.85, "water", MEDIUM_ACCESS_LEVEL)
            graph.add_edge("Graciosa",    "Sao Jorge",     42, 0.75, "air",   LOW_ACCESS_LEVEL)

            graph.add_edge("Faial",       "Pico",           8, 0.85, "water", MEDIUM_ACCESS_LEVEL)
            graph.add_edge("Faial",       "Pico",           8, 0.65, "air",   LOW_ACCESS_LEVEL)

            graph.add_edge("Sao Jorge",   "Faial",         56, 0.75, "water", MEDIUM_ACCESS_LEVEL)
            graph.add_edge("Sao Jorge",   "Faial",         56, 0.60, "air",   LOW_ACCESS_LEVEL)

            graph.add_edge("Flores",      "Corvo",         23, 0.80, "water", MEDIUM_ACCESS_LEVEL)
            graph.add_edge("Flores",      "Corvo",         23, 0.75, "air",   LOW_ACCESS_LEVEL)

            graph.add_edge("Pico",        "Sao Jorge",     58, 0.85, "water", MEDIUM_ACCESS_LEVEL)
            graph.add_edge("Pico",        "Sao Jorge",     58, 0.70, "air",   LOW_ACCESS_LEVEL)

            graph.add_edge("Flores",      "Faial",        240, 0.85, "water", MEDIUM_ACCESS_LEVEL)
            graph.add_edge("Flores",      "Faial",        240, 0.70, "air",   LOW_ACCESS_LEVEL)

            graph.add_edge("Flores",      "Sao Jorge",    260, 0.90, "water", MEDIUM_ACCESS_LEVEL)
            graph.add_edge("Flores",      "Sao Jorge",    260, 0.70, "air",   LOW_ACCESS_LEVEL)

            graph.add_edge("Corvo",       "Faial",        230, 0.85, "water", MEDIUM_ACCESS_LEVEL)
            graph.add_edge("Corvo",       "Faial",        230, 0.70, "air",   LOW_ACCESS_LEVEL)

            graph.add_edge("Corvo",       "Sao Miguel",   350, 0.85, "water", MEDIUM_ACCESS_LEVEL)
            graph.add_edge("Corvo",       "Sao Miguel",   350, 0.65, "air",   LOW_ACCESS_LEVEL)

            graph.add_edge("Pico",        "Terceira",     120, 0.80, "water", MEDIUM_ACCESS_LEVEL)
            graph.add_edge("Pico",        "Terceira",     120, 0.65, "air",   LOW_ACCESS_LEVEL)

            graph.add_edge("Santa Maria", "Sao Jorge",    190, 0.85, "water", MEDIUM_ACCESS_LEVEL)
            graph.add_edge("Santa Maria", "Sao Jorge",    190, 0.70, "air",   LOW_ACCESS_LEVEL)

            graph.add_edge("Sao Miguel",  "Faial",        180, 0.85, "water", MEDIUM_ACCESS_LEVEL)
            graph.add_edge("Sao Miguel",  "Faial",        180, 0.70, "air",   LOW_ACCESS_LEVEL)

            # Add heuristics values to nodes
            heuristic_option = 3
            heuristic_fn3({
                "graph": graph,
                "catastrophes": catastrophes,
                "vehicles": sum(fleet.values(), [])
            })

            # Create destructive nodes conditions
            destructive_nodes = {
                "Santa Maria": 400,
                "Flores": 100,
                # "Terceira": 0
            }
            graph.destructive_nodes = destructive_nodes

            # Create destructive edges conditions
            destructive_edges = {
                ("Flores", "Faial"): 200,
                ("Graciosa", "Sao Jorge"): 250,
            }
            graph.destructive_edges = destructive_edges

            # Return the MissionPlanner object
            return MissionPlanner(graph, catastrophes, fleet, supplies), heuristic_option

        case 3:
            # Description: Test simulation with 15 nodes

            ###
            # Create catastrophes
            ###

            catastrophes = {
                "G": Catastrophe(300, {"food": 150, "water": 100, "soskit": 50}),
                "L": Catastrophe(600, {"food": 175, "water":  25})
            }

            ###
            # Create the vehicles
            ###

            fleet = {
                "A": [
                    Vehicle("Bike1",       "motorcycle"),
                    Vehicle("Car1",        "car"),
                    Vehicle("Helicopter1", "helicopter"),
                    Vehicle("Boat1",       "small_boat")  # This vehicle will never be used
                ]
            }

            ###
            # Create the supplies
            ###

            # NOTE Currently assuming that the supplies are infinite
            supplies = {
                # "A": {
                #     "food":   Supply("food",    600, perishable_time=600),
                #     "water":  Supply("water",  1000),
                #     "soskit": Supply("soskit",  100)
                # }
            }

            ###
            # Create the graph
            ###

            graph = Graph(directed=False)

            # Add the nodes
            for node, fuel in [
                ("A", float('inf')),
                ("B", float('inf')),
                ("C", float('inf')),
                ("D", float('inf')),
                ("E", float('inf')),
                ("F", float('inf')),
                ("G", float('inf')),
                ("H", float('inf')),
                ("I", float('inf')),
                ("J", float('inf')),
                ("K", float('inf')),
                ("L", float('inf')),
                ("M", float('inf')),
                ("N", float('inf')),
                ("O", float('inf'))
            ]:
                catastrophe = catastrophes.get(node, None)
                vehicles = fleet.get(node, [])
                starting_supplies = supplies.get(node, {})
                graph.add_node(node,
                               fuel,
                               catastrophe,
                               vehicles,
                               starting_supplies)

            # Add the edges
            graph.add_edge("A", "B", 20, 1.00, "land", MEDIUM_ACCESS_LEVEL)
            # graph.add_edge("A", "B", 20, 1.00, "air",  MEDIUM_ACCESS_LEVEL)

            graph.add_edge("A", "C",  5, 1.00, "land", MEDIUM_ACCESS_LEVEL)  # Low-cost direct path (UCS favored)
            # graph.add_edge("A", "C",  5, 1.00, "air",  MEDIUM_ACCESS_LEVEL)

            graph.add_edge("A", "D", 15, 1.00, "land", MEDIUM_ACCESS_LEVEL)  # Adds depth for DFS
            # graph.add_edge("A", "D", 15, 1.00, "air",  MEDIUM_ACCESS_LEVEL)

            graph.add_edge("B", "E", 10, 1.00, "land", MEDIUM_ACCESS_LEVEL)  # Shortcut for BFS
            # graph.add_edge("B", "E", 10, 1.00, "air",  MEDIUM_ACCESS_LEVEL)

            graph.add_edge("B", "F", 50, 1.00, "land", MEDIUM_ACCESS_LEVEL)  # Higher cost (disfavor UCS)
            # graph.add_edge("B", "F", 50, 1.00, "air",  MEDIUM_ACCESS_LEVEL)

            graph.add_edge("C", "F", 10, 1.00, "land", MEDIUM_ACCESS_LEVEL)  # Favor UCS
            # graph.add_edge("C", "F", 10, 1.00, "air",  MEDIUM_ACCESS_LEVEL)

            graph.add_edge("C", "G", 30, 1.00, "land", MEDIUM_ACCESS_LEVEL)  # Suboptimal for UCS, BFS
            # graph.add_edge("C", "G", 30, 1.00, "air",  MEDIUM_ACCESS_LEVEL)

            graph.add_edge("D", "H", 10, 1.00, "land", MEDIUM_ACCESS_LEVEL)  # Adds depth for DFS
            # graph.add_edge("D", "H", 10, 1.00, "air",  MEDIUM_ACCESS_LEVEL)

            graph.add_edge("E", "J", 25, 1.00, "land", MEDIUM_ACCESS_LEVEL)  # Creates a detour
            # graph.add_edge("E", "J", 25, 1.00, "air",  MEDIUM_ACCESS_LEVEL)

            graph.add_edge("F", "L",  5, 1.00, "land", MEDIUM_ACCESS_LEVEL)  # Optimal for UCS
            # graph.add_edge("F", "L",  5, 1.00, "air",  MEDIUM_ACCESS_LEVEL)

            graph.add_edge("F", "M", 15, 1.00, "land", MEDIUM_ACCESS_LEVEL)  # Non-optimal
            # graph.add_edge("F", "M", 15, 1.00, "air",  MEDIUM_ACCESS_LEVEL)

            graph.add_edge("G", "N", 10, 1.00, "land", MEDIUM_ACCESS_LEVEL)
            # graph.add_edge("G", "N", 10, 1.00, "air",  MEDIUM_ACCESS_LEVEL)

            graph.add_edge("G", "O", 20, 1.00, "land", MEDIUM_ACCESS_LEVEL)  # Longer path
            # graph.add_edge("G", "O", 20, 1.00, "air",  MEDIUM_ACCESS_LEVEL)

            graph.add_edge("L", "O", 10, 1.00, "land", MEDIUM_ACCESS_LEVEL)  # Connects catastrophes
            # graph.add_edge("L", "O", 10, 1.00, "air",  MEDIUM_ACCESS_LEVEL)

            # Add alternate paths and loops
            graph.add_edge("H", "L", 40, 1.00, "land", MEDIUM_ACCESS_LEVEL)  # Loop for BFS/DFS variance
            # graph.add_edge("H", "L", 40, 1.00, "air",  MEDIUM_ACCESS_LEVEL)

            graph.add_edge("I", "G", 10, 1.00, "land", MEDIUM_ACCESS_LEVEL)  # Shortcut for UCS
            # graph.add_edge("I", "G", 10, 1.00, "air",  MEDIUM_ACCESS_LEVEL)

            graph.add_edge("J", "M", 20, 1.00, "land", MEDIUM_ACCESS_LEVEL)
            # graph.add_edge("J", "M", 20, 1.00, "air",  MEDIUM_ACCESS_LEVEL)

            graph.add_edge("K", "N", 50, 1.00, "land", MEDIUM_ACCESS_LEVEL)
            # graph.add_edge("K", "N", 50, 1.00, "air",  MEDIUM_ACCESS_LEVEL)

            graph.add_edge("M", "O",  5, 1.00, "land", MEDIUM_ACCESS_LEVEL)  # Low-cost alternate path
            # graph.add_edge("M", "O",  5, 1.00, "air",  MEDIUM_ACCESS_LEVEL)

            # Add heuristics values to nodes
            heuristic_option = 2
            heuristic_fn2({
                "graph":        graph,
                "catastrophes": catastrophes,
                "vehicles":     sum(fleet.values(), [])
            })

            # No destructive nodes
            graph.destructive_nodes = {}

            # No destructive edges
            graph.destructive_edges = {}

            # return the MissionPlanner object
            return MissionPlanner(graph, catastrophes, fleet, supplies), heuristic_option

        case _:
            raise ValueError("Invalid option")
