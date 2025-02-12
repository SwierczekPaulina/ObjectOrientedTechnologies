from abc import ABC, abstractmethod

class IPolar2D(ABC):
    @abstractmethod
    def getAngle(self):
        pass

    @abstractmethod
    def abs(self):
        pass