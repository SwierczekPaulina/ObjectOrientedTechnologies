from abc import ABC, abstractmethod

class SnippetState(ABC):
    """
    Abstrakcyjna klasa bazowa dla stanu fragmentu kodu.
    Demonstruje wzorzec projektowy 'Stan'.
    """

    @abstractmethod
    def publish(self, snippet):
        """
        Przejście do stanu 'Końcowy' lub obsługa logiki publikacji.
        """
        pass

    @abstractmethod
    def deprecate(self, snippet):
        """
        Przejście do stanu 'Przestarzały' lub obsługa logiki oznaczenia jako przestarzałe.
        """
        pass

    @abstractmethod
    def edit(self, snippet):
        """
        Przejście do stanu 'Szkic' lub obsługa logiki edycji.
        """
        pass


class DraftState(SnippetState):
    def publish(self, snippet):
        # Przejście ze Szkicu do Końcowego
        print("Fragment kodu został opublikowany jako Końcowy.")
        snippet.set_state(FinalState())

    def deprecate(self, snippet):
        # Zazwyczaj nie można oznaczyć jako przestarzałe bezpośrednio ze szkicu,
        # ale dla przykładu można to uniemożliwić lub zgłosić wyjątek.
        print("Nie można oznaczyć szkicu fragmentu kodu jako przestarzały bezpośrednio.")
        # Lub: raise ValueError("Nie można oznaczyć fragmentu kodu w stanie Szkic jako przestarzały.")

    def edit(self, snippet):
        # Już w stanie Szkic, więc nic nie robimy lub obsługujemy odpowiednio.
        print("Fragment kodu jest już w stanie Szkic.")


class FinalState(SnippetState):
    def publish(self, snippet):
        print("Fragment kodu jest już w stanie Końcowym. Nie wprowadzono zmian.")

    def deprecate(self, snippet):
        # Przejście ze stanu Końcowego do Przestarzałego
        print("Fragment kodu został oznaczony jako Przestarzały.")
        snippet.set_state(DeprecatedState())

    def edit(self, snippet):
        # Przejście ze stanu Końcowego z powrotem do Szkicu
        print("Fragment kodu został przywrócony do stanu Szkic w celu edycji.")
        snippet.set_state(DraftState())


class DeprecatedState(SnippetState):
    def publish(self, snippet):
        print("Nie można opublikować przestarzałego fragmentu kodu.")
        # Lub: raise ValueError("Nie można opublikować fragmentu kodu w stanie Przestarzałym.")

    def deprecate(self, snippet):
        print("Fragment kodu jest już w stanie Przestarzałym. Nie wprowadzono zmian.")

    def edit(self, snippet):
        print("Nie można edytować przestarzałego fragmentu kodu.")
        # Lub: raise ValueError("Nie można edytować fragmentu kodu w stanie Przestarzałym.")
