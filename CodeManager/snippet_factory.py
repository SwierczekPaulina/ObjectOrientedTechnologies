from abc import ABC, abstractmethod
from snippet_state import DraftState

class Snippet(ABC):
    """
    Abstrakcyjna klasa bazowa dla wszystkich typów fragmentów kodu.
    Demonstruje podstawową funkcjonalność, w tym odniesienie do obiektu stanu.
    """

    def __init__(self, title: str, code: str):
        self.title = title
        self.code = code
        self._state = DraftState()  # Wszystkie nowe fragmenty kodu zaczynają jako 'Szkic'

    def set_state(self, new_state):
        self._state = new_state

    def publish(self):
        self._state.publish(self)

    def deprecate(self):
        self._state.deprecate(self)

    def edit(self):
        self._state.edit(self)

    @abstractmethod
    def get_language(self) -> str:
        """
        Zwraca język tego fragmentu kodu.
        """
        pass


class PythonSnippet(Snippet):
    def get_language(self) -> str:
        return "Python"


class JavaScriptSnippet(Snippet):
    def get_language(self) -> str:
        return "JavaScript"


class ShellSnippet(Snippet):
    def get_language(self) -> str:
        return "Shell"


class SnippetFactory:
    """
    Demonstruje wzorzec projektowy 'Fabryka'.
    Odpowiada za tworzenie obiektów fragmentów kodu na podstawie określonego języka.
    """

    @staticmethod
    def create_snippet(language: str, title: str, code: str) -> Snippet:
        language = language.lower()
        if language == "python":
            return PythonSnippet(title, code)
        elif language == "javascript":
            return JavaScriptSnippet(title, code)
        elif language == "shell":
            return ShellSnippet(title, code)
        else:
            raise ValueError(f"Nieobsługiwany język fragmentu kodu: {language}")
