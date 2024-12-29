# The class Catastrophe is used to store the information of a catastrophe such as:
# - time: sensitive time of response
# - supplies_demand: dictionary with the supplies type and the amount needed

class Catastrophe:
    def __init__(self, time, supplies_demand):
        self.time = time
        self.supplies_demand = supplies_demand

    def __str__(self):
        return (
            "Time: "            + str(self.time)            + " " +
            "Supplies demand: " + str(self.supplies_demand)
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

    def decrease_time(self, time_passed):
        self.time -= time_passed

    def supply(self, supplies):
        for supply in supplies:
            if supply in self.supplies_demand.keys():
                self.supplies_demand[supply] -= supplies[supply]
                if self.supplies_demand[supply] == 0:
                    self.supplies_demand.pop(supply)
