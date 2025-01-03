from supply    import Supply
from supply    import perishable_kinds

from math      import ceil
import copy

# Vehicle class
# - name             : str   (unique identifier)
# - category         : str
# - travel_method    : str   {land, air, water}
# - speed            : float (km/h)
# - cargo            : int   (kg) (current cargo weight)
# - cargo_contents   : list  (dict with supply and key as the type of supply)
# - cargo_capacity   : int   (kg)
# - tank             : float (l)  (current fuel level)
# - tank_capacity    : float (l)
# - fuel_consumption : float (l/100km)
# - access_level     : int   (level of access to certain terrains)

###
# Constants
###

# time, in minutes, to refuel 1 liter [default: 0.1 min = 6 sec]
REFUEL_TIME = 0.1

# The access_level variable determines the level of access to certain terrains
# of a vehicle. The higher the access_level, the more terrains the vehicle can
# access. The access_level is a value between 1 and 3, where:
LOW_ACCESS_LEVEL    = 1
MEDIUM_ACCESS_LEVEL = 2
HIGH_ACCESS_LEVEL   = 3

# Vehicle specs by category:
# - travel_method
# - speed
# - cargo_capacity
# - tank_capacity
# - fuel_consumption
# - access_level
VEHICLE_SPECS = {
    "motorcycle":  ("land",  120,  100,   30,   4, HIGH_ACCESS_LEVEL  ),
    "car":         ("land",  160,  500,   50,   8, MEDIUM_ACCESS_LEVEL),
    "truck":       ("land",  100, 2000,  300,  30, LOW_ACCESS_LEVEL   ),
    "drone":       ("air",   100,    5,    5,   1, HIGH_ACCESS_LEVEL  ),
    "helicopter":  ("air",   250,  700,  300,  70, MEDIUM_ACCESS_LEVEL),
    "airplane":    ("air",   250,  800,  200,  40, LOW_ACCESS_LEVEL   ),
    "small_boat":  ("water",  50,  700,  500,  50, HIGH_ACCESS_LEVEL  ),
    "medium_boat": ("water",  30, 1000,  800,  80, MEDIUM_ACCESS_LEVEL),
    "large_boat":  ("water",  20, 2000, 1000, 100, LOW_ACCESS_LEVEL   ),
}


###
# Utility functions
###

def convert_access_level_to_str(access_level: int) -> str:
    access_level_str = "Unknown"

    if access_level == LOW_ACCESS_LEVEL:
        access_level_str = "Low"
    elif access_level == MEDIUM_ACCESS_LEVEL:
        access_level_str = "Medium"
    elif access_level == HIGH_ACCESS_LEVEL:
        access_level_str = "High"

    return access_level_str


###
# Vehicle class
###

class Vehicle:
    def __init__(self, name: str, category: str):

        if category not in VEHICLE_SPECS.keys():
            raise ValueError(f"Invalid category: {category}")

        self.name             = name
        self.category         = category
        self.travel_method    = VEHICLE_SPECS[category][0]
        self.speed            = VEHICLE_SPECS[category][1]
        self.cargo            = 0                           # cargo starts empty
        self.cargo_contents   = {}                          # list of supplies
        self.cargo_capacity   = VEHICLE_SPECS[category][2]
        self.tank             = VEHICLE_SPECS[category][3]  # tank starts full
        self.tank_capacity    = VEHICLE_SPECS[category][3]
        self.fuel_consumption = VEHICLE_SPECS[category][4]
        self.access_level     = VEHICLE_SPECS[category][5]

    def __str__(self):
        return (
            "Vehicle: {"
            f"  name: {self.name}, "
            f"  category: {self.category}, "
            f"  travel_method: {self.travel_method}"
            f"  speed: {self.speed}, "
            f"  cargo: {self.cargo}, "
            f"  cargo_contents: {self.cargo_contents}, "
            f"  cargo_capacity: {self.cargo_capacity}, "
            f"  tank: {self.tank}, "
            f"  tank_capacity: {self.tank_capacity}, "
            f"  fuel_consumption: {self.fuel_consumption}, "
            "}"
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def copy(self):
        return copy.deepcopy(self)

    def serialize(self):
        return {
            "name": self.name,
            "category": self.category,
            "travel_method": self.travel_method,
            "speed": self.speed,
            "cargo": self.cargo,
            "cargo_contents": [supply.serialize() for supply in self.cargo_contents],
            "cargo_capacity": self.cargo_capacity,
            "tank": self.tank,
            "tank_capacity": self.tank_capacity,
            "fuel_consumption": self.fuel_consumption,
        }

    ###
    # Fuel related methods
    ###

    # Returns a tuple with:
    # - the amount of fuel remaining from the argument
    # - the time, in minutes, it took to refuel
    def refuel(self, liters: float) -> (float, int):
        self.tank = min(self.tank + liters, self.tank_capacity)
        return (
            max(0, self.tank + liters - self.tank_capacity),
            ceil(liters * REFUEL_TIME)
        )

    def calculate_fuel_needed(self, distance: int) -> float:
        fuel_needed = distance * self.fuel_consumption / 100
        additional_fuel_needed = max(0, fuel_needed - self.tank)
        # round up the result to 2 decimal places
        return ceil(additional_fuel_needed * 100) / 100

    def is_travel_possible(self, travel_method: str, access_level: int) -> bool:
        return (
            self.travel_method == travel_method
            and self.access_level >= access_level
        )

    def has_enough_fuel(self, distance: int) -> bool:
        return self.tank >= self.calculate_fuel_needed(distance)

    def can_travel(self, travel_method: str, access_level: int, distance: int) -> bool:
        return (
            self.is_travel_possible(travel_method, access_level)
            and self.has_enough_fuel(distance)
        )

    # TODO pass speed multiplier as parameter
    # returns the time in minutes and the fuel consumed
    def travel(self, distance: int) -> (int, float):
        fuel_consumed = distance * self.fuel_consumption / 100
        # round the fuel consumed to 2 decimal places
        fuel_consumed = ceil(fuel_consumed * 100) / 100
        self.tank -= fuel_consumed
        return (distance / self.speed) * 60, fuel_consumed  # time in minutes
        # return (distance / self.speed * speed_mult) * 60, fuel_consumed  # time in minutes (TODO)

    ###
    # Cargo related methods
    ###

    def load_cargo(self, supply: Supply, weight: int) -> Supply:
        # Calculate the amount of cargo that can be loaded
        amount_to_load = min(weight, self.cargo_capacity - self.cargo)

        # Divide the supply in two parts
        supply_loaded, supply_remaining = supply.divide(amount_to_load)

        # Check if the supply is already in the cargo and update it
        # Otherwise, add the new type of supply to the cargo
        if supply in self.cargo_contents:
            self.cargo_contents[supply.kind].load(supply_loaded)
        else:
            self.cargo_contents[supply.kind] = supply_loaded

        # Update the current cargo weight
        self.cargo += amount_to_load

        return supply_remaining

    def unload_cargo(self, supply_kind: str, weight: int) -> None:
        # Check if the supply is in the cargo
        if supply_kind not in self.cargo_contents:
            raise ValueError("Supply not found in the cargo")

        # Unload the supply
        supply = self.cargo_contents[supply_kind]
        try:
            supply.supply(weight)
        except ValueError:
            error_msg = (
                f"Cargo weight of {supply_kind} to unload exceeds the current weight. "
                f"Current weight: {supply.amount}, requested weight: {weight}"
            )
            raise ValueError(error_msg)

        # If the supply is empty, remove it from the cargo
        if supply.amount == 0:
            self.cargo_contents.pop(supply_kind)

        # Update the current cargo weight
        self.cargo -= weight

    def load_supplies_for_catastrophe(
        self, supplies: dict[str, int]
    ) -> (dict[str, int], dict[str, Supply]):

        supplies_loaded = {}
        supplies_left = {}

        # Remove unnecessary supplies from cargo
        for supply_kind in list(self.cargo_contents.keys()):
            if supply_kind not in supplies:
                # Remove supply to save space for needed ones
                self.cargo -= self.cargo_contents[supply_kind].amount
                del self.cargo_contents[supply_kind]

        # Sort supplies by perishability: prioritize perishable items (True > False)
        sorted_supplies = sorted(
            supplies.items(),
            key=lambda item: not perishable_kinds.get(item[0], False)
        )

        for supply_kind, demand in sorted_supplies:
            # Check if the supply exists in the vehicle's cargo contents
            if supply_kind not in self.cargo_contents:
                self.cargo_contents[supply_kind] = Supply(kind=supply_kind, amount=0)

            # Get the supply object
            supply = self.cargo_contents[supply_kind]

            # Calculate how much can be loaded based on demand and current cargo space
            loadable_amount = min(demand, self.cargo_capacity - self.cargo)
            supplies_loaded[supply_kind] = loadable_amount

            # Update the supply's amount in the vehicle and total cargo weight
            supply.amount += loadable_amount
            self.cargo += loadable_amount

            # Track leftover supplies
            leftover_amount = demand - loadable_amount
            if leftover_amount > 0:
                supplies_left[supply_kind] = Supply(
                    kind=supply_kind, amount=leftover_amount
                )

        # Cleanup empty supplies
        self.cargo_contents = {
            kind: supply for kind, supply in self.cargo_contents.items() if supply.amount > 0
        }

        supplies_loaded = {
            kind: amount for kind, amount in supplies_loaded.items() if amount > 0
        }

        supplies_left = {
            kind: supply for kind, supply in supplies_left.items() if supply.amount > 0
        }

        return supplies_loaded, supplies_left
