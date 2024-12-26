class Node:
    # TODO import Catastrophe
    # def __init__(self, name: str, catastrophe: Catastrophe = None):
    def __init__(self, name: str, catastrophe=None):
        self.name = name
        self.catastrophe = catastrophe
        # self.fuel = 0  # TODO

    def __str__(self):
        return (
            "{"
            f"name: {self.name}"
            f"{', catastrophe: ' + str(self.catastrophe) if self.catastrophe is not None else ''}"
            "}"
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
