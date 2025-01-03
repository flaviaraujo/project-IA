# The class Catastrophe is used to store the information of a catastrophe such as:
# - time: sensitive time of response
# - supplies_demand: dictionary with the supplies type and the amount needed
# - accessible_vehicles: list of vehicles that can respond to the catastrophe

from supply import Supply

import copy


class Catastrophe:
    def __init__(self, time, supplies_demand):
        self.time = time
        self.supplies_demand = supplies_demand
        self.accessible_vehicles = []  # List of tuples (vehicle name, path, fuel consumption)

    def __str__(self):
        return (
            "{\n"
            f"  time_to_respond: {self.time},\n"
            f"  supplies_demand: {self.supplies_demand},\n"
            f"  accessible_vehicles: {self.accessible_vehicles}\n"
            "}"
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (
            self.time == other.time and
            self.supplies_demand == other.supplies_demand
        )

    def __hash__(self):
        return hash((self.time, self.supplies_demand))

    def copy(self):
        return copy.deepcopy(self)

    def serialize(self):
        return {
            "time_to_respond": self.time,
            "supplies_demand": self.supplies_demand,
            "accessible_vehicles": self.accessible_vehicles
        }

    def decrease_time(self, time_passed):
        self.time -= time_passed

    def supply(self, cargo_contents: dict[str, Supply]) -> (dict[str, int], dict[str, Supply]):
        """
        Provides the demanded supplies and returns the remaining supplies in the vehicle
        and the amount of supplies provided to the catastrophe.

        Args:
        - cargo_contents (dict): A dictionary of the vehicle's supplies with their kinds as keys
          and `Supply` objects as values.

        Returns:
        - tuple:
            - dict: The updated cargo contents after fulfilling the demands.
            - dict: The amount of each supply kind that was provided.
        """
        remaining_cargo = cargo_contents.copy()  # Clone the input cargo contents
        cargo_supplied = {}  # Track what was supplied to the catastrophe

        for supply_kind, demand in self.supplies_demand.copy().items():
            if supply_kind in remaining_cargo:
                supply = remaining_cargo[supply_kind]
                provided = min(supply.amount, demand)

                # Update the catastrophe's demand
                self.supplies_demand[supply_kind] -= provided
                if self.supplies_demand[supply_kind] <= 0:
                    del self.supplies_demand[supply_kind]

                # Update the vehicle's supply amount
                supply.amount -= provided
                if supply.amount <= 0:
                    del remaining_cargo[supply_kind]

                # Track what was supplied
                cargo_supplied[supply_kind] = provided

        return cargo_supplied, remaining_cargo
