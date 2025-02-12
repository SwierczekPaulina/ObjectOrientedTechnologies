from ICurrencyExchanger import ICurrencyExchanger
from Currency import Currency

class CurrencyExchanger(ICurrencyExchanger):
    __instance = None

    def __init__(self) -> None:
        if not CurrencyExchanger.__instance:
            CurrencyExchanger.__instance = self
        else:
            raise Exception("Ta klasa to singleton.")
        
    @staticmethod
    def get_instance() -> "CurrencyExchanger":
        if not CurrencyExchanger.__instance:
            CurrencyExchanger.__instance = CurrencyExchanger()
        return CurrencyExchanger.__instance
    
    def exchange(self, source_currency: Currency, destination_currency: Currency, amount: float) -> float:
        if source_currency.get_rate() and destination_currency.get_rate() and amount > 0:
            return amount * (source_currency.get_rate() / destination_currency.get_rate())
        else:
            raise ValueError("Przynajmniej jedna z podanych walut lub podana wartość nie jest poprawna.")
