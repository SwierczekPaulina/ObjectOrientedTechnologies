import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
from matplotlib.widgets import Button, Slider

from constants import *
from Vector2D import Vector2D
from Polar2DAdapter import Polar2DAdapter
from State import HealthyState, InfectedState, ImmuneState
from Person import Person
from Memento import Originator, Caretaker

def add_new_individual(people):
    side = random.choice(['left', 'right', 'top', 'bottom'])
    if side == 'left':
        x = 0
        y = random.uniform(0, SPACE_HEIGHT)
        vx = random.uniform(0, MAX_SPEED)
        vy = random.uniform(-MAX_SPEED, MAX_SPEED)
    elif side == 'right':
        x = SPACE_WIDTH
        y = random.uniform(0, SPACE_HEIGHT)
        vx = -random.uniform(0, MAX_SPEED)
        vy = random.uniform(-MAX_SPEED, MAX_SPEED)
    elif side == 'top':
        x = random.uniform(0, SPACE_WIDTH)
        y = SPACE_HEIGHT
        vx = random.uniform(-MAX_SPEED, MAX_SPEED)
        vy = -random.uniform(0, MAX_SPEED)
    else:
        x = random.uniform(0, SPACE_WIDTH)
        y = 0
        vx = random.uniform(-MAX_SPEED, MAX_SPEED)
        vy = random.uniform(0, MAX_SPEED)
    position = Vector2D(x, y)
    velocity = Vector2D(vx, vy)

    if random.random() < SPAWN_INFECTED_PROBABILITY:
        state = InfectedState()
        person = Person(position, velocity, state)
        person.susceptible = True
        person.set_state(state)
    else:
        r = random.random()
        if r < INITIAL_SUSCEPTIBLE_PROBABILITY:
            state = HealthyState()
            person = Person(position, velocity, state)
        else:
            state = ImmuneState()
            person = Person(position, velocity, state)
            person.susceptible = False
            person.immune = True
    people.append(person)

people = []

for _ in range(INITIAL_POPULATION):
    x = random.uniform(0, SPACE_WIDTH)
    y = random.uniform(0, SPACE_HEIGHT)
    speed = random.uniform(0, MAX_SPEED)
    angle = random.uniform(0, 2 * math.pi)

    velocity = Vector2D(0, 0)
    polar_velocity = Polar2DAdapter(velocity)
    polar_velocity.setPolarCoordinates(speed, angle)
    position = Vector2D(x, y)

    r = random.random()
    if r < INITIAL_SUSCEPTIBLE_PROBABILITY:
        state = HealthyState()
        person = Person(position, velocity, state)
    else:
        state = ImmuneState()
        person = Person(position, velocity, state)
        person.susceptible = False
        person.immune = True
    people.append(person)

originator = Originator(people)
caretaker = Caretaker(originator)
current_frame = 0
close_contacts = {}
caretaker.create(current_frame, close_contacts)

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, SPACE_WIDTH)
ax.set_ylim(0, SPACE_HEIGHT)
ax.set_aspect('equal')
scatter = ax.scatter([], [], c=[])

infection_circles = []

def init():
    scatter.set_offsets(np.empty((0, 2)))
    return scatter,

def update(frame):
    global people, infection_circles, current_frame, close_contacts
    current_frame = frame
    xdata = []
    ydata = []
    colors = []

    for i, person in enumerate(people):
        person.update_position()
        person.request()

    people = [person for person in people if person.position is not None]

    for circle in infection_circles:
        circle.remove()
    infection_circles.clear()

    total_population = len(people)
    population_difference = INITIAL_POPULATION - total_population
    if population_difference > 0:
        spawn_probability = min(population_difference * 0.01, 1.0)
        if random.random() < spawn_probability:
            add_new_individual(people)
    else:
        pass

    new_close_contacts = {}
    for i, person in enumerate(people):
        if person.susceptible and isinstance(person.state, HealthyState):
            for j, other in enumerate(people):
                if isinstance(other.state, InfectedState):
                    if person.position is None or other.position is None:
                        continue
                    dx = person.position.x - other.position.x
                    dy = person.position.y - other.position.y
                    distance = math.hypot(dx, dy)
                    if distance <= 2:
                        key = (i, j)
                        new_close_contacts[key] = close_contacts.get(key, 0) + 1
                        if new_close_contacts[key] >= 75:
                            infection_prob = 1.0 if other.symptomatic else 0.5
                            if random.random() < infection_prob:
                                person.set_state(InfectedState())
                                person.susceptible = True
                                break
                    else:
                        pass
    close_contacts = new_close_contacts

    caretaker.create(frame, close_contacts)

    for person in people:
        xdata.append(person.position.x)
        ydata.append(person.position.y)
        if isinstance(person.state, HealthyState):
            if person.immune:
                colors.append('blue')
            else:
                colors.append('green')
        elif isinstance(person.state, InfectedState):
            if person.symptomatic:
                colors.append('red')
            else:
                colors.append('orange')
            circle_color = 'red' if person.symptomatic else 'orange'
            circle = Circle((person.position.x, person.position.y), 2, color=circle_color, alpha=0.2)
            ax.add_patch(circle)
            infection_circles.append(circle)
        elif isinstance(person.state, ImmuneState):
            colors.append('blue')
        else:
            colors.append('grey')
    scatter.set_offsets(np.c_[xdata, ydata])
    scatter.set_color(colors)

    num_susceptible = sum(1 for person in people if isinstance(person.state, HealthyState) and not person.immune)
    num_infected_symptomatic = sum(1 for person in people if isinstance(person.state, InfectedState) and person.symptomatic)
    num_infected_asymptomatic = sum(1 for person in people if isinstance(person.state, InfectedState) and not person.symptomatic)
    num_immune = sum(1 for person in people if person.immune)
    total_population = len(people)
    ax.set_title(f"Step {frame} | Total: {total_population} | Susceptible: {num_susceptible} | Infected (Symptomatic): {num_infected_symptomatic} | Infected (Asymptomatic): {num_infected_asymptomatic} | Immune: {num_immune}")

    if num_susceptible == 0 and num_infected_symptomatic == 0 and num_infected_asymptomatic == 0:
        print("Simulation ends: Everyone is immune.")
        ani.event_source.stop()

    update_slider_range()

    return scatter,

legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Susceptible', markerfacecolor='green', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Infected (Symptomatic)', markerfacecolor='red', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Infected (Asymptomatic)', markerfacecolor='orange', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Immune', markerfacecolor='blue', markersize=10),
]
ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2)

plt.subplots_adjust(bottom=0.25)

widget_width = 0.1
widget_height = 0.04
widget_spacing = 0.02
total_widgets_width = widget_width * 4 + widget_spacing * 3
start_x = 0.5 - total_widgets_width / 2

pause_ax = plt.axes([start_x, 0.05, widget_width, widget_height])
resume_ax = plt.axes([start_x + (widget_width + widget_spacing), 0.05, widget_width, widget_height])
reset_ax = plt.axes([start_x + 2 * (widget_width + widget_spacing), 0.05, widget_width, widget_height])
restore_ax = plt.axes([start_x + 3 * (widget_width + widget_spacing), 0.05, widget_width, widget_height])

slider_ax = plt.axes([0.2, 0.01, 0.6, 0.03])

pause_button = Button(pause_ax, 'Pause')
resume_button = Button(resume_ax, 'Resume')
reset_button = Button(reset_ax, 'Reset')
restore_button = Button(restore_ax, 'Restore')

max_saved_frames = 0
slider = Slider(slider_ax, 'Time Step', 0, max_saved_frames, valinit=0, valstep=1)

def update_slider_range():
    global max_saved_frames
    max_saved_frames = current_frame
    if max_saved_frames < 1:
        max_saved_frames = 1
    slider.valmax = max_saved_frames
    slider.ax.set_xlim(slider.valmin, slider.valmax)
    if slider.val > max_saved_frames:
        slider.set_val(max_saved_frames)
    slider.ax.figure.canvas.draw_idle()

def pause(event):
    ani.event_source.stop()

def resume(event):
    ani.event_source.start()

def reset(event):
    global current_frame, infection_circles, close_contacts, people
    ani.event_source.stop()
    success, restored_frame, restored_close_contacts = caretaker.restore(0)
    if success:
        print("Simulation reset to initial state.")
        current_frame = restored_frame
        for circle in infection_circles:
            circle.remove()
        infection_circles.clear()
        close_contacts = restored_close_contacts
        people = originator.people
        ani.frame_seq = iter(range(restored_frame, MAX_STEPS))

        update_slider_range()
        slider.set_val(restored_frame)
        fig.canvas.draw_idle()
    ani.event_source.start()

def restore(event):
    global current_frame, infection_circles, close_contacts, people
    ani.event_source.stop()
    selected_frame = int(slider.val)
    success, restored_frame, restored_close_contacts = caretaker.restore(selected_frame)
    if success:
        print(f"Restored to time step {restored_frame}")
        current_frame = restored_frame

        for circle in infection_circles:
            circle.remove()
        infection_circles.clear()
        close_contacts = restored_close_contacts
        people = originator.people
        ani.frame_seq = iter(range(restored_frame, MAX_STEPS))
        update_slider_range()
        slider.set_val(restored_frame)
        fig.canvas.draw_idle()
    else:
        print("Failed to restore to the selected time step.")
    ani.event_source.start()

pause_button.on_clicked(pause)
resume_button.on_clicked(resume)
reset_button.on_clicked(reset)
restore_button.on_clicked(restore)

ani = FuncAnimation(fig, update, frames=range(current_frame, MAX_STEPS), init_func=init, blit=False, interval=10)

mng = plt.get_current_fig_manager()
try:
    mng.window.state('zoomed')
except AttributeError:
    try:
        mng.window.showMaximized()
    except AttributeError:
        mng.resize(*mng.window.maxsize())

plt.show()