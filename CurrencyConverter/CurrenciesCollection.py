from ICurrenciesCollection import ICurrenciesCollection
from Currency import Currency

class CurrenciesCollection(ICurrenciesCollection):
    def __init__(self) -> None:
        self.__currencies = []
        
    def add(self, currency: Currency) -> None:
        self.__currencies.append(currency)

    def remove(self, currency: Currency) -> None:
        self.__currencies = [c for c in self.__currencies if c.get_code() != currency.get_code()]

    def update(self, currency: Currency) -> None:
        for i, c in enumerate(self.__currencies):
            if c.get_code() == currency.get_code():
                self.__currencies[i] = currency

    def get(self, code: str) -> None | Currency:
        for currency in self.__currencies:
            if currency.get_code() == code:
                return currency
        return None
    
    def print_currencies(self) -> None:
        for currency in self.__currencies:
            print(f"{currency.get_code()} - {currency.get_name()}")
