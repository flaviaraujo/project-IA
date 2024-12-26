from functools import lru_cache

# TODO: Limitações geográficas que impedem certos veículos de aceder
# a determinadas zonas (e.g., terrenos inacessíveis para camiões).
# OPTION: Implement limits by vehicle category
# OR add a variable to indicate the level of access to certain terrains

# Vehicle class
# - name             : str   (unique identifier)
# - category         : str
# - speed            : float (km/h)
# - cargo            : float (kg) (current cargo weight)
# - cargo_capacity   : float (kg)
# - tank             : float (l)  (current fuel level)
# - tank_capacity    : float (l)
# - fuel_consumption : float (l/100km)
# - travel_method    : str   {land, air, water}

# vehicle specs by category: travel_method, speed, cargo_capacity, tank_capacity, fuel_consumption
vehicle_specs = {
    "motorcycle": ("land",  120,    10,    15,    4),
    "car":        ("land",  160,   500,    50,    8),
    "truck":      ("land",  100,  2000,   300,   30),
    "drone":      ("air",   100,     5,     5,    2),
    "helicopter": ("air",   250,   700,   300,   70),
    "airplane":   ("air",   250,   800,   200,   40),
    "boat":       ("water",  50,  5000,  1000,   50),
}


class Vehicle:
    def __init__(self, name: str, category: str,
                 initial_cargo: float, initial_tank: float):

        if category not in vehicle_specs.keys():
            raise ValueError(f"Invalid category: {category}")

        self.name             = name
        self.category         = category
        self.cargo            = initial_cargo
        self.tank             = initial_tank
        self.travel_method    = vehicle_specs[category][0]
        self.speed            = vehicle_specs[category][1]
        self.cargo_capacity   = vehicle_specs[category][2]
        self.tank_capacity    = vehicle_specs[category][3]
        self.fuel_consumption = vehicle_specs[category][4]

    def __str__(self):
        return (
            "Vehicle: {"
            f"  name: {self.name}, "
            f"  category: {self.category}, "
            f"  speed: {self.speed}, "
            f"  cargo: {self.cargo}, "
            f"  cargo_capacity: {self.cargo_capacity}, "
            f"  tank: {self.tank}, "
            f"  tank_capacity: {self.tank_capacity}, "
            f"  fuel_consumption: {self.fuel_consumption}, "
            f"  travel_method: {self.travel_method}"
            "}"
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    ########################
    # Fuel related methods #
    ########################

    def refuel(self, liters: float) -> float:
        self.tank = min(self.tank + liters, self.tank_capacity)
        return max(0, self.tank + liters - self.tank_capacity)

    @lru_cache(maxsize=None)
    def calculate_fuel_needed(self, distance: float) -> float:
        return distance * self.fuel_consumption / 100

    def is_travel_possible(self, method: str, distance: float) -> bool:
        return (
            method == self.travel_method
            and self.tank_capacity >= self.calculate_fuel_needed(distance)
        )

    def travel(self, method: str, distance: float) -> bool:
        if self.is_travel_possible(method, distance):
            self.tank_capacity -= self.calculate_fuel_needed(distance)
            return True
        return False

    #########################
    # Cargo related methods #
    #########################

    def load_cargo(self, weight: float) -> float:
        self.cargo = min(self.cargo + weight, self.cargo_capacity)
        return max(0, self.cargo + weight - self.cargo_capacity)

    def unload_cargo(self, weight: float) -> None:
        # if weight > self.cargo:
        #     raise ValueError("Cargo weight to unload exceeds the current cargo weight")
        self.cargo -= weight
