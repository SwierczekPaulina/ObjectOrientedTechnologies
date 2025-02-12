from typing import Dict, List, Optional
import json
from snippet_factory import Snippet, SnippetFactory
from snippet_state import DraftState, FinalState, DeprecatedState  # Stany

class SnippetManager:
    """
    Demonstruje wzorzec projektowy 'Singleton'.
    Odpowiada za centralne przechowywanie fragmentów kodu i zarządzanie ich tagami,
    z możliwością zapisu i odczytu stanu do/z pliku.
    """

    _instance = None
    _file_path = "snippets.json"  # Ścieżka do pliku z danymi

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SnippetManager, cls).__new__(cls)
            # Inicjalizuje atrybuty potrzebne dla instancji singletonu
            cls._instance._snippets = {}  # klucz: snippet_id, wartość: obiekt Snippet
            cls._instance._next_id = 1    # proste, inkrementalne ID
            cls._instance.load_from_file()  # Załaduj dane przy uruchomieniu programu
        return cls._instance

    def add_snippet(self, language: str, title: str, code: str) -> int:
        """
        Tworzy nowy fragment kodu za pomocą fabryki, przechowuje go i zwraca jego ID.
        """
        snippet = SnippetFactory.create_snippet(language, title, code)
        snippet_id = self._next_id
        self._snippets[snippet_id] = snippet
        self._next_id += 1
        self.save_to_file()  # Zapisz dane po każdej zmianie
        return snippet_id

    def get_snippet(self, snippet_id: int) -> Optional[Snippet]:
        """
        Pobiera fragment kodu według ID lub zwraca None, jeśli nie znaleziono.
        """
        return self._snippets.get(snippet_id)

    def list_snippets(self) -> Dict[int, Snippet]:
        """
        Zwraca słownik {snippet_id: Snippet} dla wszystkich przechowywanych fragmentów kodu.
        """
        return dict(self._snippets)

    def remove_snippet(self, snippet_id: int) -> bool:
        """
        Usuwa fragment kodu według ID. Zwraca True, jeśli usunięcie było udane.
        """
        if snippet_id in self._snippets:
            del self._snippets[snippet_id]
            self.save_to_file()  # Zapisz dane po każdej zmianie
            return True
        return False

    def add_tag(self, snippet_id: int, tag: str) -> bool:
        """
        Dodaje tag do istniejącego fragmentu kodu. Zwraca True w przypadku powodzenia.
        """
        snippet = self.get_snippet(snippet_id)
        if snippet:
            # Dla prostoty tagi są przechowywane jako zbiór w obiekcie fragmentu kodu
            if not hasattr(snippet, 'tags'):
                snippet.tags = set()
            snippet.tags.add(tag)
            self.save_to_file()  # Zapisz dane po każdej zmianie
            return True
        return False

    def remove_tag(self, snippet_id: int, tag: str) -> bool:
        """
        Usuwa tag z fragmentu kodu. Zwraca True w przypadku powodzenia.
        """
        snippet = self.get_snippet(snippet_id)
        if snippet and hasattr(snippet, 'tags') and tag in snippet.tags:
            snippet.tags.remove(tag)
            self.save_to_file()  # Zapisz dane po każdej zmianie
            return True
        return False

    def save_to_file(self):
        """
        Zapisuje aktualny stan fragmentów kodu do pliku JSON.
        Dane obejmują:
        - ID fragmentu kodu
        - Język
        - Tytuł
        - Kod
        - Tagi
        - Stan (np. Draft, Final, Deprecated)
        """
        data = {
            "next_id": self._next_id,
            "snippets": [
                {
                    "id": snippet_id,
                    "language": snippet.get_language(),
                    "title": snippet.title,
                    "code": snippet.code,
                    "tags": list(getattr(snippet, 'tags', [])),
                    "state": snippet._state.__class__.__name__
                }
                for snippet_id, snippet in self._snippets.items()
            ]
        }
        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load_from_file(self):
        """
        Odczytuje dane fragmentów kodu z pliku JSON.
        Jeśli plik nie istnieje, tworzy pustą bazę danych.
        """
        try:
            with open(self._file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                self._next_id = data["next_id"]
                self._snippets = {}
                for snippet_data in data["snippets"]:
                    snippet = SnippetFactory.create_snippet(
                        snippet_data["language"],
                        snippet_data["title"],
                        snippet_data["code"]
                    )
                    snippet.tags = set(snippet_data["tags"])
                    # Ustawienie stanu na podstawie nazwy klasy
                    state_class = globals().get(snippet_data["state"], DraftState)
                    snippet.set_state(state_class())
                    self._snippets[snippet_data["id"]] = snippet
        except FileNotFoundError:
            print("Brak pliku z zapisanymi danymi. Tworzenie nowej bazy danych.")
        except Exception as e:
            print(f"Wystąpił błąd podczas ładowania danych: {e}")