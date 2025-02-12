import random
from abc import ABC, abstractmethod

class VehicleState(ABC):
    @abstractmethod
    def handle(self, vehicle, timestep):
        pass

class FreeState(VehicleState):
    def handle(self, vehicle, timestep):
        # Nic się tu nie dzieje, pojazd czeka na incydent
        pass

class DispatchedState(VehicleState):
    def handle(self, vehicle, timestep):
        # Ruch w stronę incydentu
        vehicle.move_towards_target(timestep)
        if vehicle.at_target():
            # Pojazd dojechał
            if random.random() < 0.05:
                # Fałszywy alarm
                vehicle.set_state(ReturningState())
                vehicle.set_return_target()
            else:
                # Incident
                vehicle.set_state(BusyState())
                vehicle.operation_duration = random.randint(5, 25)
                vehicle.time_in_operation = 0

class BusyState(VehicleState):
    def handle(self, vehicle, timestep):
        vehicle.time_in_operation += timestep
        if vehicle.time_in_operation >= vehicle.operation_duration:
            # Po incydencie, powrót do jednostki
            vehicle.set_state(ReturningState())
            vehicle.set_return_target()

class ReturningState(VehicleState):
    def handle(self, vehicle, timestep):
        vehicle.move_towards_target(timestep)
        if vehicle.at_target():
            # Losowo od 0 do 3 sekund po incydencie
            if vehicle.return_delay is None:
                vehicle.return_delay = random.randint(0, 3)
            else:
                vehicle.return_delay -= timestep
                if vehicle.return_delay <= 0:
                    # Pojazd jest teraz wolny
                    vehicle.set_state(FreeState())
                    vehicle.return_delay = None
                    # Pojazd nie ma już referencji do incydentu
                    vehicle.current_incident = None
