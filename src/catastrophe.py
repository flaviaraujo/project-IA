# The class Catastrophe is used to store the information of a catastrophe such as:
# - time: sensitive time of response
# - supplies_demand: dictionary with the supplies type and the amount needed

from supply import Supply

import copy


class Catastrophe:
    def __init__(self, time, supplies_demand):
        self.time = time
        self.supplies_demand = supplies_demand

    def __str__(self):
        return (
            "{\n"
            f"  time_to_respond: {self.time},\n"
            f"  supplies_demand: {self.supplies_demand}\n"
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

    def supply_amount(self, cargo_amounts: dict[str, int]) -> None:
        # Decrements the catastrophe's demand
        for supply_kind, demand in self.supplies_demand.copy().items():
            if supply_kind in cargo_amounts:
                provided = min(cargo_amounts[supply_kind], demand)
                self.supplies_demand[supply_kind] -= provided
                if self.supplies_demand[supply_kind] <= 0:
                    del self.supplies_demand[supply_kind]

    def get_supplies_demand_amount(self):
        return sum(self.supplies_demand.values())

    def is_resolved(self):
        return (not self.supplies_demand) or sum(self.supplies_demand.values()) == 0

    def has_time_expired(self, time_passed):
        return self.time <= time_passed
