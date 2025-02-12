from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def handle(self, person):
        pass

class HealthyState(State):
    def handle(self, person):
        # No specific action required for healthy individuals
        pass

class ImmuneState(State):
    def handle(self, person):
        # No specific action required for immune individuals
        pass

class InfectedState(State):
    def handle(self, person):
        if person.time_in_state >= person.infection_duration:
            person.set_state(ImmuneState())
            person.immune = True
            person.susceptible = False
