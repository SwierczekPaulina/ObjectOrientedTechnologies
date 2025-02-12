from abc import ABC, abstractmethod

class IPolar2D(ABC):
    @abstractmethod
    def getAngle(self) -> float:
        """Oblicz kąt pomiędzy osią OX i kierunkiem wektora"""
        pass

    @abstractmethod
    def abs(self) -> float:
        """Obicz moduł wektora"""
        pass
