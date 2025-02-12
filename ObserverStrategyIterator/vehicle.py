import math
from vehicle_states import *

class Vehicle:
    def __init__(self, unit):
        self.unit = unit
        self.state = FreeState()
        self.lat, self.lon = unit.lat, unit.lon
        self.target_lat = None
        self.target_lon = None
        self.speed = 0.0005
        self.operation_duration = 0
        self.time_in_operation = 0
        self.return_delay = None
        self.current_incident = None  # Sprawdzaj do jakiego incydentu został przydzielony ten pojazd

    def set_state(self, new_state):
        self.state = new_state

    def dispatch_to(self, lat, lon, incident):
        self.current_incident = incident
        self.target_lat = lat
        self.target_lon = lon
        self.set_state(DispatchedState())

    def set_return_target(self):
        # Powrót do jednostki
        self.target_lat = self.unit.lat
        self.target_lon = self.unit.lon

    def update(self, timestep=1):
        self.state.handle(self, timestep)

    def at_target(self):
        if self.target_lat is None or self.target_lon is None:
            return True
        dist = math.sqrt((self.lat - self.target_lat)**2 + (self.lon - self.target_lon)**2)
        return dist < 0.00001

    def move_towards_target(self, timestep):
        if self.target_lat is None or self.target_lon is None:
            return
        dist_lat = self.target_lat - self.lat
        dist_lon = self.target_lon - self.lon
        dist = math.sqrt(dist_lat**2 + dist_lon**2)
        if dist == 0:
            return
        step = self.speed * timestep
        if step > dist:
            step = dist
        self.lat += (dist_lat/dist)*step
        self.lon += (dist_lon/dist)*step