from catastrophe import Catastrophe


class Node:
    def __init__(self,
                 name:        str,
                 fuel:        int         = 0,
                 catastrophe: Catastrophe = None,
                 vehicles:    list        = [],
                 supplies:    dict        = {}):
        self.name = name
        self.fuel = fuel
        self.catastrophe = catastrophe
        self.vehicles = vehicles
        self.supplies = supplies

    def __str__(self):
        return (
            "{"
            f"  name: {self.name},\n"
            f"  fuel: {self.fuel},\n"
            f"  catastrophe: {self.catastrophe},\n"
            f"  vehicles: {self.vehicles},\n"
            f"  supplies: {self.supplies}\n"
            "}"
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def serialize(self):
        return {
            "name": self.name,
            "fuel": self.fuel,
            "catastrophe": self.catastrophe.serialize() if self.catastrophe is not None else None,
            "vehicles": [vehicle.serialize() for vehicle in self.vehicles],
            "supplies": {
                supply_kind: supply.serialize()
                for supply_kind, supply in self.supplies.items()
            }
        }
