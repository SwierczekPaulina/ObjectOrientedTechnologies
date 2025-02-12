from vehicle_states import FreeState

class IStrategy:
    def execute(self, incident, units):
        pass

class NearestUnitStrategy(IStrategy):
    def __init__(self):
        self.fallback_strategy = SplitAcrossUnitsStrategy()

    def execute(self, incident, units):
        required_vehicles = 3 if incident.type == "PZ" else 2
        closest_unit = None
        closest_dist = float('inf')
        for unit in units:
            dist = unit.distance_to(incident.coordinates)
            if dist < closest_dist and unit.has_free_vehicles(required_vehicles):
                closest_dist = dist
                closest_unit = unit

        if closest_unit:
            vehicles = closest_unit.get_free_vehicles(required_vehicles)
            return [(closest_unit, vehicles)]
        else:
            return self.fallback_strategy.execute(incident, units)

class SplitAcrossUnitsStrategy(IStrategy):
    def execute(self, incident, units):
        required_vehicles = 3 if incident.type == "PZ" else 2
        assigned = []
        vehicles_needed = required_vehicles
        units_sorted = sorted(units, key=lambda u: u.distance_to(incident.coordinates))

        for unit in units_sorted:
            if vehicles_needed <= 0:
                break
            free_in_unit = sum(1 for v in unit.vehicles if isinstance(v.state, FreeState))
            if free_in_unit > 0:
                to_take = min(vehicles_needed, free_in_unit)
                free_vs = unit.get_free_vehicles(to_take)
                if free_vs:
                    assigned.append((unit, free_vs))
                    vehicles_needed -= len(free_vs)

        if vehicles_needed > 0:
            return []
        return assigned