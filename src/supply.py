# The class supply is used to store the information of a supply such as:
# - kind: kind of supply (food, water, sos_kit)
# - amount: amount of supply
# - perishable_time: time that the supply will last (if it is perishable)

import copy

perishable_kinds = {"food": True, "water": False, "sos_kit": False}


class Supply:
    def __init__(self, kind: str, amount: int, perishable_time: int = None):
        self.kind = kind
        self.amount = amount
        self.perishable_time = perishable_time

    def __str__(self):
        return (
            "Kind: "            + str(self.kind)            + " " +
            "Amount: "          + str(self.amount)          + " " +
            "Perishable time: " + str(self.perishable_time)
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (
            self.kind == other.kind and
            self.amount == other.amount and
            self.perishable_time == other.perishable_time
        )

    def __hash__(self):
        return hash((self.kind, self.amount, self.perishable_time))

    def copy(self):
        return copy.deepcopy(self)

    def serialize(self):
        return {
            "kind": self.kind,
            "amount": self.amount,
            "perishable_time": self.perishable_time
        }

    def divide(self, amount: int) -> ('Supply', 'Supply'):
        if amount > self.amount:
            raise ValueError("Cannot divide a supply into more than it has")

        if amount == self.amount:
            return self, None

        self.amount -= amount
        return Supply(self.kind, amount, self.perishable_time), self

    def load(self, supply: 'Supply') -> None:
        self.amount += supply.amount

    def supply(self, amount: int) -> int:
        if amount > self.amount:
            raise ValueError("Cannot supply more than it has")

        self.amount -= amount
        return amount

    def decrease_perisable_time(self, time_passed: int):
        if self.perishable_time is not None:
            self.perishable_time -= time_passed
