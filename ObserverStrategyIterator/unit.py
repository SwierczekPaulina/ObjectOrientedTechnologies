import math
from vehicle import Vehicle
from vehicle_states import FreeState

class Unit:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.vehicles = [Vehicle(self) for _ in range(5)]

    def distance_to(self, coordinates):
        dlat = self.lat - coordinates[0]
        dlon = self.lon - coordinates[1]
        return math.sqrt(dlat*dlat + dlon*dlon)

    def has_free_vehicles(self, count):
        free_count = sum(1 for v in self.vehicles if isinstance(v.state, FreeState))
        return free_count >= count

    def get_free_vehicles(self, count):
        chosen = []
        for v in self.vehicles:
            if isinstance(v.state, FreeState):
                chosen.append(v)
                if len(chosen) == count:
                    return chosen
        return chosen