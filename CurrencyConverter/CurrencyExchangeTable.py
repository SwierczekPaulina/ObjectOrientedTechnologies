class CurrencyExchangeTable:
    def __init__(self) -> None:
        self.__table_name = None
        self.__timestamp = None
    
    def get_table_name(self) -> str:
        return self.__table_name
    
    def set_table_name(self, table_name: str) -> None:
        self.__table_name = table_name

    def get_timestamp(self) -> str:
        return self.__timestamp
    
    def set_timestamp(self, timestamp: str) -> None:
        self.__timestamp = timestamp