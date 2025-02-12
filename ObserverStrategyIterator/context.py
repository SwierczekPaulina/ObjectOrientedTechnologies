from strategy import IStrategy
from observer import ObservedSubject, UnitObserver

class Context:
    def __init__(self, strategy: IStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: IStrategy):
        self.strategy = strategy

    def execute(self, incident, units):
        return self.strategy.execute(incident, units)

class IncidentDispatcher(ObservedSubject):
    def __init__(self, strategy: IStrategy):
        super().__init__()
        self.strategy_context = Context(strategy)

    def new_incident(self, incident):
        self.notify_all(incident)
        units = [obs.unit for obs in self.observers if isinstance(obs, UnitObserver)]
        assignments = self.strategy_context.execute(incident, units)
        for (unit, vehicles) in assignments:
            for v in vehicles:
                v.dispatch_to(incident.coordinates[0], incident.coordinates[1], incident)
                incident.assigned_vehicles.append(v)