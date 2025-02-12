import xml.etree.ElementTree as ET
from CurrencyExchangeTable import CurrencyExchangeTable
from CurrenciesCollection import CurrenciesCollection
from Currency import Currency
from datetime import datetime
from typing import Union

class XMLParser:
    @staticmethod
    def parseXML(xml_data: str) -> Union[CurrencyExchangeTable, CurrenciesCollection]:
        table = CurrencyExchangeTable()
        root = ET.fromstring(xml_data)
        root = root.find("ExchangeRatesTable")

        table.set_table_name(root.find("No").text)
        table.set_timestamp(datetime.strptime(root.find("EffectiveDate").text, "%Y-%m-%d").timestamp())

        currencies = CurrenciesCollection()
        for rate in root.findall("Rates/Rate"):
            currency = Currency()
            currency.set_code(rate.find("Code").text)
            currency.set_name(rate.find("Currency").text)
            currency.set_rate(float(rate.find("Mid").text))
            currencies.add(currency)
        return table, currencies