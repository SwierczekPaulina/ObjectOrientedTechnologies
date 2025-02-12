from abc import ABC, abstractmethod
from Currency import Currency

class ICurrencyExchanger(ABC):
    @abstractmethod
    def exchange(self, source_currency: Currency, destination_currency: Currency, amount: float) -> float:
        """Przelicz jedną walutę na drugą, podając kwotę."""
        pass
