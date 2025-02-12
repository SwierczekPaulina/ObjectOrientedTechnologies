from constants import *

class Incident:
    def __init__(self, incident_type, coordinates):
        self.type = incident_type  # "PZ" lub "MZ"
        self.coordinates = coordinates
        self.assigned_vehicles = []  # Przechowuj pojazdy przypisane do incydentu

    def is_resolved(self):
        # Incydent jest uznawany za zakończony, jeśli żadne pojazdy nie są przypisane lub wszystkie wróciły do stanu wolnego (FreeState).
        return all(v.current_incident is not self for v in self.assigned_vehicles)