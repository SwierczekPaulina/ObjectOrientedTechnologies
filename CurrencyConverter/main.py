from NBPRestProvider import NBPRestProvider
from Decoder import Decoder
from XMLParser import XMLParser
from CurrencyExchanger import CurrencyExchanger
from Currency import Currency

def main():
    xml_data = NBPRestProvider.get("https://api.nbp.pl/api/exchangerates/tables/a/")
    xml_data = Decoder.convertToUTF(xml_data)
    _, currencies = XMLParser.parseXML(xml_data)
    print("Dostępne waluty:")
    pln_currency = Currency()
    pln_currency.set_code("PLN")
    pln_currency.set_name("Polski złoty")
    pln_currency.set_rate(1.0)
    currencies.add(pln_currency)

    currencies.print_currencies()

    source_code = input("Podaj kod waluty, z której chcesz przeliczyć: ").upper()
    destination_code = input("Podaj kod waluty, na którą chcesz przeliczyć: ").upper()
    while True:
        try:
            amount_input = input("Podaj kwotę do przeliczenia: ")
            amount = float(amount_input)
            if amount > 0:
                break
            else:
                print("Kwota musi być większa od 0. Spróbuj ponownie.")
        except ValueError:
            print(f"Nieprawidłowa wartość '{amount_input}'. Proszę wpisać liczbę większą od 0.")

    source_currency = currencies.get(source_code)
    destination_currency = currencies.get(destination_code)

    if source_currency and destination_currency and not source_currency.equals(destination_currency):
        exchanger = CurrencyExchanger.get_instance()
        exchanged_value = exchanger.exchange(source_currency, destination_currency, amount)
        print(f"{amount} {source_code} jest równe {exchanged_value:.2f} {destination_code}")
    else:
        print("Podano niepoprawny kod.")

if __name__ == "__main__":
    main()