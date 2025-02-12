import requests

class NBPRestProvider:
    @staticmethod
    def get(url: str) -> bytearray: 
        response = requests.get(url, headers={'Accept': 'application/xml'})
        if response.status_code == 200:
            return response.content
        else:
            raise Exception("API nie zwróciło danych.")
