class Observer:
    def update(self, incident):
        pass

class UnitObserver(Observer):
    def __init__(self, unit):
        self.unit = unit

    def update(self, incident):
        pass

class ObservedSubject:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer: Observer):
        self.observers.append(observer)

    def remove_observer(self, observer: Observer):
        self.observers.remove(observer)

    def notify_all(self, data):
        for observer in self.observers:
            observer.update(data)
