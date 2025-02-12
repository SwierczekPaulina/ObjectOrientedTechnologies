import random
from unit import Unit
from constants import *
from incident import Incident
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from strategy import NearestUnitStrategy
from context import IncidentDispatcher, UnitObserver

def random_incident():
    lat = random.uniform(MIN_LAT, MAX_LAT)
    lon = random.uniform(MIN_LON, MAX_LON)
    itype = "MZ" if random.random() < 0.7 else "PZ"
    return Incident(itype, (lat, lon))

units = [Unit(name, lat, lon) for name, (lat, lon) in UNIT_COORDS.items()]

dispatcher = IncidentDispatcher(NearestUnitStrategy())
for u in units:
    dispatcher.add_observer(UnitObserver(u))

# Wizualizacja
fig, ax = plt.subplots()
ax.set_xlim(MIN_LAT, MAX_LAT)
ax.set_ylim(MIN_LON, MAX_LON)
ax.set_title("PSP Dispatch Simulation in Kraków")
ax.set_xlabel("Latitude")
ax.set_ylabel("Longitude")

unit_scatter = ax.scatter([u.lat for u in units],
                          [u.lon for u in units],
                          c='red', marker='^', s=100, label='Units')

vehicle_scatter = ax.scatter([], [], c='blue', s=50, label='Vehicles')
incident_scatter = ax.scatter([], [], c='green', s=50, label='Incidents')

ax.legend()

vehicle_positions = []
active_incidents = []

ticks = 0
incident_interval = 50

def update(frame):
    global ticks, active_incidents

    # Generuj co jakiś czas nowy incydent
    if ticks % incident_interval == 0:
        inc = random_incident()
        dispatcher.new_incident(inc)
        active_incidents.append(inc)

    # Aktualizuj pojazdy
    for u in units:
        for v in u.vehicles:
            v.update(timestep=1)

    # Usuń wszystkie incydenty które zostały rozwiązane
    active_incidents = [inc for inc in active_incidents if not inc.is_resolved()]

    # Aktualizuj GUI
    vlat = []
    vlon = []
    for u in units:
        for v in u.vehicles:
            vlat.append(v.lat)
            vlon.append(v.lon)
    vehicle_scatter.set_offsets(list(zip(vlat, vlon)))

    ilat = [inc.coordinates[0] for inc in active_incidents]
    ilon = [inc.coordinates[1] for inc in active_incidents]
    incident_scatter.set_offsets(list(zip(ilat, ilon)))

    ticks += 1
    return vehicle_scatter, incident_scatter

ani = animation.FuncAnimation(fig, update, frames=2000, interval=100, blit=False, repeat=False)
plt.show()
