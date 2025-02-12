class Currency:
    def __init__(self) -> None:
        self.__code = None
        self.__name = None
        self.__rate = None
    
    def get_code(self) -> str:
        return self.__code
    
    def set_code(self, code: str) -> None:
        self.__code = code

    def get_name(self) -> str:
        return self.__name
    
    def set_name(self, name: str) -> None:
        self.__name = name

    def get_rate(self) -> float:
        return self.__rate
    
    def set_rate(self, rate: float) -> None:
        self.__rate = rate

    def equals(self, currency: "Currency") -> bool:
        same_code = self.__code == currency.get_code()
        same_name = self.__name == currency.get_name()
        same_rate = self.__rate == currency.get_rate()
        return same_code and same_name and same_rate