from Person import Person
from Vector2D import Vector2D

class Memento:
    def __init__(self, state, frame_number, close_contacts):
        self.state = state
        self.frame_number = frame_number
        self.close_contacts = close_contacts

class Originator:
    def __init__(self, people):
        self.people = people

    def create_memento(self, frame_number, close_contacts):
        state = []
        for person in self.people:
            state.append({
                'position': (person.position.x, person.position.y) if person.position else (None, None),
                'velocity': (person.velocity.x, person.velocity.y),
                'state': type(person.state),
                'time_in_state': person.time_in_state,
                'infection_duration': person.infection_duration,
                'symptomatic': person.symptomatic,
                'susceptible': person.susceptible,
                'immune': person.immune,
                'steps_since_direction_change': person.steps_since_direction_change,
                'direction_change_interval': person.direction_change_interval
            })
        close_contacts_copy = {k: v for k, v in close_contacts.items()}
        return Memento(state, frame_number, close_contacts_copy)

    def restore(self, memento):
        self.people.clear()
        for person_state in memento.state:
            if person_state['position'][0] is None or person_state['position'][1] is None:
                continue
            position = Vector2D(*person_state['position'])
            velocity = Vector2D(*person_state['velocity'])
            state_class = person_state['state']
            person = Person(position, velocity, state_class())
            person.time_in_state = person_state['time_in_state']
            person.infection_duration = person_state['infection_duration']
            person.symptomatic = person_state['symptomatic']
            person.susceptible = person_state['susceptible']
            person.immune = person_state['immune']
            person.steps_since_direction_change = person_state['steps_since_direction_change']
            person.direction_change_interval = person_state['direction_change_interval']
            self.people.append(person)

        return memento.close_contacts

class Caretaker:
    def __init__(self, originator):
        self.originator = originator
        self.mementos = []

    def create(self, frame_number, close_contacts):
        memento = self.originator.create_memento(frame_number, close_contacts)
        self.mementos.append(memento)

    def restore(self, frame_number):
        if frame_number < len(self.mementos):
            memento = self.mementos[frame_number]
            restored_close_contacts = self.originator.restore(memento)
            self.mementos = self.mementos[:frame_number + 1]
            return True, memento.frame_number, restored_close_contacts
        else:
            print("Invalid time step.")
            return False, None, None