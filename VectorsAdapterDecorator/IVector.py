from abc import ABC, abstractmethod

class IVector(ABC):
    @abstractmethod
    def abs(self) -> float:
        """Obicz moduł wektora"""
        pass

    @abstractmethod
    def cdot(self, other: "IVector") -> float:
        """Oblicz iloczyn skalarny pomiędzy dwoma wektorami"""
        pass

    @abstractmethod
    def getComponents(self) -> float:
        """Zwróć wartości składowych wektora"""
        pass