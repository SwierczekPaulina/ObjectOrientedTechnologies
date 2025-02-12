from abc import ABC, abstractmethod

class IVector(ABC):
    @abstractmethod
    def abs(self):
        pass

    @abstractmethod
    def cdot(self, param):
        pass

    @abstractmethod
    def getComponents(self):
        pass
