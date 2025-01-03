# operation_type : str  - Type of the operation ("move", "refuel", "drop", "load")
# vehicle        : str  - Name of the vehicle involved
# node           : str  - Node name where the operation takes place
# supplies       : dict - A dictionary with keys as supply types and values as Supply objects


from math import ceil
import copy


operation_order = {
    "start": 0,
    "move": 1,
    "refuel": 2,
    "drop": 3,
    "load": 4
}


class Operation:
    def __init__(self,
                 time:           int,
                 operation_type: str,
                 vehicle:        str  = None,
                 node:           str  = None,
                 fuel:           int  = None,
                 supplies:       dict = None,
                 fuel_consumed:  int  = None):
        valid_operations = {"start", "move", "refuel", "drop", "load"}

        if operation_type not in valid_operations:
            raise ValueError(
                f"Invalid operation type: {operation_type}. \
                Must be one of {valid_operations}."
            )

        self.time = ceil(time)
        self.operation_type = operation_type
        self.vehicle = vehicle
        self.node = node
        self.fuel = fuel
        self.fuel_consumed = fuel_consumed
        self.supplies = supplies or {}

    def __str__(self):
        time_str = f"{str(self.time).rjust(3)}"
        match self.operation_type:
            case "start":
                return f"[{time_str}] Vehicle {self.vehicle}: Start at node {self.node}"
            case "move":
                return f"[{time_str}] Vehicle {self.vehicle}: Move to node {self.node}"
            case "refuel":
                return f"[{time_str}] Vehicle {self.vehicle}: Refuel {self.fuel} liters at node {self.node}"
            case "drop":
                return f"[{time_str}] Vehicle {self.vehicle}: Drop supplies {self.supplies} at node {self.node}"
            case "load":
                return f"[{time_str}] Vehicle {self.vehicle}: Load supplies {self.supplies} at node {self.node}"
            case _:
                return "Unknown operation"

    def __repr__(self):
        return self.__str__()

    def copy(self):
        return copy.deepcopy(self)
