from Vector2D import Vector2D
from Polar2DAdapter import Polar2DAdapter
from State import InfectedState
import random
import math
from constants import MAX_SPEED, TIME_STEP, SPACE_WIDTH, SPACE_HEIGHT

class Person:
    def __init__(self, position, velocity, state):
        self.position = position
        self.velocity = velocity
        self.state = state
        self.time_in_state = 0
        self.infection_duration = 0
        self.symptomatic = False
        self.susceptible = True
        self.immune = False
        self.steps_since_direction_change = 0
        self.direction_change_interval = random.randint(1, 25)

    def request(self):
        self.state.handle(self)

    def set_state(self, state):
        self.state = state
        self.time_in_state = 0
        if isinstance(state, InfectedState):
            self.infection_duration = random.randint(20 * 25, 30 * 25)
            self.symptomatic = random.choice([True, False])
        else:
            self.infection_duration = 0
            self.symptomatic = False

    def update_position(self):
        self.position.x += self.velocity.x * TIME_STEP
        self.position.y += self.velocity.y * TIME_STEP

        left_boundary = 0
        right_boundary = SPACE_WIDTH
        bottom_boundary = 0
        top_boundary = SPACE_HEIGHT

        if self.position.x < left_boundary or self.position.x > right_boundary:
            if random.choice([True, False]):
                self.velocity.x = -self.velocity.x
                self.position.x = max(left_boundary, min(self.position.x, right_boundary))
            else:
                self.position = None

        if self.position and (self.position.y < bottom_boundary or self.position.y > top_boundary):
            if random.choice([True, False]):
                self.velocity.y = -self.velocity.y
                self.position.y = max(bottom_boundary, min(self.position.y, top_boundary))
            else:
                self.position = None

        self.steps_since_direction_change += 1
        if self.steps_since_direction_change >= self.direction_change_interval:
            self.update_velocity()
            self.steps_since_direction_change = 0
            self.direction_change_interval = random.randint(1, 25)

        self.time_in_state += 1

    def update_velocity(self):
        polar_velocity = Polar2DAdapter(self.velocity)

        new_speed = random.uniform(0, MAX_SPEED)
        new_angle = random.uniform(0, 2 * math.pi)
        polar_velocity.setPolarCoordinates(new_speed, new_angle)