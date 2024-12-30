from mission_planner import MissionPlanner
from catastrophe     import Catastrophe
from vehicle         import Vehicle
from supply          import Supply
from graph.graph     import Graph

from vehicle import LOW_ACCESS_LEVEL, MEDIUM_ACCESS_LEVEL, HIGH_ACCESS_LEVEL


def init_simulation(option: int) -> MissionPlanner:
    match option:
        case 1:
            # TODO add simulation description

            ###
            # Create catastrophes
            ###

            catastrophes = {
                "B": Catastrophe(600, {"food": 300, "water": 100}),
                "F": Catastrophe(300, {"food": 300, "water": 500, "soskit": 50})
            }

            ###
            # Create the vehicles
            ###

            fleet = {
                "A": [
                    Vehicle("Bike1",       "motorcycle"),
                    Vehicle("Car1",        "car"),
                    Vehicle("Truck1",      "truck")
                ],
                "D": [
                    Vehicle("Drone1",      "drone"),
                    Vehicle("Helicopter1", "helicopter"),
                    Vehicle("Airplane1",   "airplane"),
                    Vehicle("Boat1",       "small_boat"),
                    Vehicle("Boat2",       "medium_boat"),
                    Vehicle("Boat3",       "large_boat")
                ]
            }

            ###
            # Create the supplies
            ###

            supplies = {
                "A": {
                    "food":   Supply("food",    600, perishable_time=600),
                    "water":  Supply("water",  1000),
                    "soskit": Supply("soskit",  100)
                },
                "D": {
                    "food":   Supply("food",    300, perishable_time=300),
                    "water":  Supply("water",   500),
                    "soskit": Supply("soskit",   50)
                }
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
                ("F", 0)
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
            graph.add_edge("A", "B", 2, 1.00, "air",   HIGH_ACCESS_LEVEL)
            graph.add_edge("A", "B", 3, 1.00, "land",  HIGH_ACCESS_LEVEL)
            graph.add_edge("A", "B", 3, 1.00, "water", HIGH_ACCESS_LEVEL)
            graph.add_edge("A", "C", 3, 0.85, "land",  MEDIUM_ACCESS_LEVEL)
            graph.add_edge("B", "D", 4, 0.75, "water", MEDIUM_ACCESS_LEVEL)
            graph.add_edge("B", "E", 5, 1.00, "air",   MEDIUM_ACCESS_LEVEL)
            graph.add_edge("B", "E", 6, 1.00, "land",  MEDIUM_ACCESS_LEVEL)
            graph.add_edge("C", "F", 6, 0.90, "land",  LOW_ACCESS_LEVEL)
            graph.add_edge("D", "E", 7, 0.60, "land",  LOW_ACCESS_LEVEL)
            graph.add_edge("E", "F", 8, 0.70, "land",  LOW_ACCESS_LEVEL)

            # Add heuristics values to nodes TODO
            # graph.update_heuristics(heuristic_fn: function, params: dict)

            # Create destructible nodes conditions
            destructible_nodes = {
                "C": 300
            }
            graph.destructible_nodes = destructible_nodes

            # Create destructible edges conditions
            destructible_edges = {
                ("A", "B"): 350,
                ("B", "E"): 200
            }
            graph.destructible_edges = destructible_edges

            # return the MissionPlanner object
            return MissionPlanner(graph, catastrophes, fleet, supplies)
        case 2:
            return None
        case 3:
            return None
        case _:
            raise ValueError("Invalid option")
