# Raport projektu

## Wzorce projektowe

1. **Singleton**  
   - **`SnippetManager`** jest zaimplementowany jako Singleton. Tworzymy tylko jedną instancję w całej aplikacji (metoda `__new__` przechowuje statyczne pole `_instance`).  
   - Umożliwia to zarządzanie centralnym repozytorium fragmentów kodu w jednym miejscu i uniknięcie konfliktów związanych z wielokrotnym tworzeniem menedżera.

2. **Factory**  
   - **`SnippetFactory`** odpowiada za tworzenie konkretnych obiektów typu `Snippet` (np. `PythonSnippet`, `JavaScriptSnippet`, `ShellSnippet`) w zależności od podanego języka.  
   - Dzięki temu kod wywołujący nie musi wiedzieć o szczegółach implementacji poszczególnych klas fragmentów, tylko korzysta z fabryki.

3. **Strategy**  
   - W module **`retrieval_strategy.py`** mamy zestaw strategii wyszukiwania fragmentów kodu:  
     - `LanguageRetrievalStrategy`  
     - `TagRetrievalStrategy`  
     - `FullTextRetrievalStrategy`  
   - Każda strategia implementuje wspólny interfejs `SnippetRetrievalStrategy`. Klasa `SnippetSearcher` pełni rolę kontekstu i pozwala na zmianę strategii w trakcie działania programu.

4. **State**  
   - Każdy `Snippet` przechowuje obiekt stanu (`_state`), który implementuje metody `publish()`, `deprecate()`, `edit()`.  
   - Wzorzec **Stan** jest zaimplementowany w module **`snippet_state.py`**. Dostępne są stany `DraftState`, `FinalState`, `DeprecatedState`.  
   - Wywołanie np. `snippet.publish()` deleguje do konkretnego stanu, zmieniając zachowanie w zależności od tego, w jakim stanie aktualnie jest dany snippet.

---

## Zasady SOLID

1. **Single Responsibility Principle (SRP)**  
   - Klasy i moduły są w dużej mierze odpowiedzialne za pojedyncze aspekty:  
     - `SnippetManager` zarządza przechowywaniem i obsługą fragmentów kodu.  
     - `SnippetFactory` odpowiada tylko za tworzenie obiektów.  
     - `snippet_state.py` zawiera wyłącznie logikę stanu snippetów.  
     - `retrieval_strategy.py` odpowiada za wyszukiwanie zgodnie z daną strategią.  
     - Główne funkcje w `main.py` zajmują się interakcją użytkownika i wywołują logikę biznesową z menedżera.  
   - Dzięki temu kody są klarownie rozdzielone.

2. **Open/Closed Principle (OCP)**  
   - System jest otwarty na rozszerzenia, a zamknięty na modyfikacje.  
   - Dodanie nowej strategii wyszukiwania wymaga utworzenia nowej klasy strategii, bez modyfikowania istniejących.  
   - Stany snippetów można rozszerzać, dopisując nową klasę stanu i w minimalnym stopniu modyfikując jedynie miejsca, gdzie ten stan jest wybierany (np. w logice menu).

3. **Liskov Substitution Principle (LSP)**  
   - Strategie (`SnippetRetrievalStrategy`) mogą być dowolnie wymieniane w `SnippetSearcher` i zawsze będą działać poprawnie w kontekście wyszukiwania.  
   - Klasy stanu (`DraftState`, `FinalState`, `DeprecatedState`) dziedziczą po bazowej `SnippetState` i każda z nich realizuje wymagane metody w sposób zgodny z oczekiwaniami systemu.  
   - Nie naruszamy LSP, ponieważ obiekty potomne mogą być używane zamiennie tam, gdzie oczekuje się obiektu bazowego.

4. **Interface Segregation Principle (ISP)**  
   - Każda strategia w `retrieval_strategy.py` implementuje interfejs `SnippetRetrievalStrategy` z jedną metodą `search()`.  
   - Nie ma tu jednego dużego interfejsu, a poszczególne klasy stanów snippetów również mają wąski, ściśle sprecyzowany interfejs (`publish`, `deprecate`, `edit`).  
   - Moduły są podzielone na małe, wyspecjalizowane części.

5. **Dependency Inversion Principle (DIP)**  
   - `SnippetSearcher` zależy od abstrakcji (`SnippetRetrievalStrategy`), a nie od konkretnych implementacji strategii, co spełnia założenia DIP.  
   - W małym projekcie nie ma rozbudowanego wstrzykiwania zależności, jednak kluczowe miejsca (wyszukiwanie, stany) opierają się na abstrakcjach, nie na implementacjach.

---

Podsumowując, projekt demonstruje skuteczne wykorzystanie wzorców projektowych (Singleton, Factory, Strategy, State) oraz w dużym stopniu zachowuje zasady SOLID. Kod jest podzielony na moduły, klasy pełnią jasno określone zadania, a interfejsy są wykorzystywane w sposób umożliwiający rozbudowę w przyszłości.
