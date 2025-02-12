from abc import ABC, abstractmethod
from Currency import Currency

class ICurrenciesCollection(ABC):
    @abstractmethod
    def add(self, currency: Currency) -> None:
        """Dodaj walutę do listy"""
        pass

    @abstractmethod
    def remove(self, currency: Currency) -> None:
        """Usuń walutę z listy"""
        pass

    @abstractmethod
    def update(self, currency: Currency) -> None:
        """Zaktualizuj walutę z listy"""
        pass

    @abstractmethod
    def get(self, code: str) -> None | Currency:
        """Zwróć walutę z listy"""
        pass

    @abstractmethod
    def print_currencies(self) -> None:
        """Wyświetl waluty z listy"""