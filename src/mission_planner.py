# The class MissionPlanner is responsible for planning the mission.
# Calls the search algorithms and returns the best path for each vehicle,
# considering the supplies and catastrophes in the environment.
# It holds the following camps:
# - graph:        graph of the environment
# - catastrophes: dictionary of catastrophes where the key is the node name
# - fleet:        dictionary of vehicles     where the key is the node name
# - supplies:     dictionary of supplies     where the key is the node name

from graph.graph import Graph


class MissionPlanner:
    def __init__(self, graph: Graph, catastrophes: dict,
                 fleet: dict, supplies: dict):
        self.graph = graph
        self.catastrophes = catastrophes
        self.fleet = fleet
        self.supplies = supplies

    def __str__(self):
        return (
            "MissionPlanner: {\n"
            f"  graph: {self.graph},\n"
            f"  catastrophes: {self.catastrophes},\n"
            f"  fleet: {self.fleet},\n"
            f"  supplies: {self.supplies}\n"
            "}"
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (
            self.graph == other.graph
            and self.catastrophes == other.catastrophes
            and self.fleet == other.fleet
            and self.supplies == other.supplies
        )

    def __hash__(self):
        return hash((self.graph, self.catastrophes, self.fleet, self.supplies))

    ###
    # Serialize methods for pretty printing
    ###

    def serialize_catastrophes(self):
        return {
            node: catastrophe.serialize()
            for node, catastrophe in self.catastrophes.items()
        }

    def serialize_fleet(self):
        return {
            node: [vehicle.serialize() for vehicle in vehicles]
            for node, vehicles in self.fleet.items()
        }

    def serialize_supplies(self):
        return {
            node: {
                supply_kind: supply.serialize()
                for supply_kind, supply in supplies.items()
            }
            for node, supplies in self.supplies.items()
        }
