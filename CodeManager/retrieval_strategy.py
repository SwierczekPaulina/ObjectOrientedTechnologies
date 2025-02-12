from abc import ABC, abstractmethod
from typing import List
from snippet_factory import Snippet
from snippet_manager import SnippetManager


class SnippetRetrievalStrategy(ABC):
    """
    Abstrakcyjna klasa bazowa dla strategii wyszukiwania fragmentów kodu.
    Demonstruje wzorzec projektowy 'Strategia'.
    """

    @abstractmethod
    def search(self, query: str) -> List[Snippet]:
        """
        Wyszukiwanie fragmentów kodu na podstawie podanego zapytania.
        """
        pass


class LanguageRetrievalStrategy(SnippetRetrievalStrategy):
    """
    Konkretna strategia wyszukiwania fragmentów kodu według języka programowania.
    """

    def search(self, query: str) -> List[Snippet]:
        manager = SnippetManager()
        all_snippets = manager.list_snippets().values()
        return [
            snippet for snippet in all_snippets
            if snippet.get_language().lower() == query.lower()
        ]


class TagRetrievalStrategy(SnippetRetrievalStrategy):
    """
    Konkretna strategia wyszukiwania fragmentów kodu na podstawie pojedynczego tagu.
    """

    def search(self, query: str) -> List[Snippet]:
        manager = SnippetManager()
        all_snippets = manager.list_snippets().values()
        return [
            snippet for snippet in all_snippets
            if hasattr(snippet, 'tags') and query in snippet.tags
        ]


class FullTextRetrievalStrategy(SnippetRetrievalStrategy):
    """
    Konkretna strategia wyszukiwania fragmentów kodu w pełnym tekście:
    sprawdza zarówno tytuł, jak i kod.
    """

    def search(self, query: str) -> List[Snippet]:
        manager = SnippetManager()
        all_snippets = manager.list_snippets().values()
        query_lower = query.lower()
        return [
            snippet for snippet in all_snippets
            if (query_lower in snippet.title.lower()
                or query_lower in snippet.code.lower())
        ]


class SnippetSearcher:
    """
    Klasa kontekstowa używająca SnippetRetrievalStrategy.
    Umożliwia zmianę strategii w czasie działania programu.
    """

    def __init__(self, strategy: SnippetRetrievalStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SnippetRetrievalStrategy):
        """
        Zmiana strategii wyszukiwania w trakcie działania programu.
        """
        self._strategy = strategy

    def search(self, query: str) -> List[Snippet]:
        """
        Deleguje operację wyszukiwania do wybranej strategii.
        """
        return self._strategy.search(query)
