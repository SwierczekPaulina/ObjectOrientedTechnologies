from snippet_manager import SnippetManager
from retrieval_strategy import (
    SnippetSearcher,
    LanguageRetrievalStrategy,
    TagRetrievalStrategy,
    FullTextRetrievalStrategy
)

def clear_terminal():
    """
    Czyści ekran terminala, działa niezależnie od systemu operacyjnego.
    \033[2J: Sekwencja ucieczki ANSI, która czyści cały ekran.
    \033[H: Przesuwa kursor do lewego górnego rogu ekranu.
    end="": Zapewnia, że po poleceniu nie zostanie dodana nowa linia.
    """
    print("\033[2J\033[H", end="")

def main():
    manager = SnippetManager()
    clear_terminal()
    while True:
        print("\n==== Menedżer Fragmentów Kodu ====")
        print("1) Utwórz fragment kodu")
        print("2) Wyświetl fragmenty kodu")
        print("3) Usuń fragment kodu")
        print("4) Zmień stan fragmentu kodu (opublikuj, oznacz jako przestarzały, edytuj)")
        print("5) Dodaj tag do fragmentu kodu")
        print("6) Usuń tag z fragmentu kodu")
        print("7) Wyszukaj fragmenty kodu")
        print("8) Wyjdź")
        choice = input("Wybierz opcję (1-8): ").strip()

        clear_terminal()
        if choice == "1":
            create_snippet(manager)
        elif choice == "2":
            list_snippets(manager)
        elif choice == "3":
            remove_snippet(manager)
        elif choice == "4":
            update_state(manager)
        elif choice == "5":
            tag_snippet(manager)
        elif choice == "6":
            untag_snippet(manager)
        elif choice == "7":
            search_snippets(manager)
        elif choice == "8":
            manager.save_to_file()
            print("Zamykanie aplikacji, dane zostały zapisane. Do widzenia!")
            break
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

def create_snippet(manager: SnippetManager):
    """Pobierz dane fragmentu kodu od użytkownika, utwórz nowy fragment kodu."""
    language = input("Podaj język fragmentu kodu (Python, JavaScript, Shell): ").strip()
    title = input("Podaj tytuł fragmentu kodu: ").strip()
    code = input("Podaj kod fragmentu (jednolinijkowy lub mały blok): ").strip()
    try:
        snippet_id = manager.add_snippet(language, title, code)
        print(f"Fragment kodu utworzony z ID: {snippet_id}")
    except ValueError as e:
        print(f"Błąd: {e}")

def list_snippets(manager: SnippetManager):
    """Wyświetl wszystkie przechowywane fragmenty kodu."""
    snippets = manager.list_snippets()
    if snippets:
        for sid, snippet in snippets.items():
            lang = snippet.get_language()
            tags = getattr(snippet, 'tags', set())
            state_name = snippet._state.__class__.__name__.replace("State", "")
            tag_str = ",".join(tags) if tags else "(brak tagów)"
            print(f"[ID={sid}] '{snippet.title}' ({lang}, {state_name}) | Tagi: {tag_str}")
    else:
        print("Brak zapisanych fragmentów kodu.")

def remove_snippet(manager: SnippetManager):
    """Usuń fragment kodu na podstawie jego ID."""
    try:
        snippet_id = int(input("Podaj ID fragmentu kodu do usunięcia: ").strip())
    except ValueError:
        print("Nieprawidłowe ID. Podaj wartość liczbową.")
        return

    success = manager.remove_snippet(snippet_id)
    print("Fragment kodu usunięty." if success else "Nie znaleziono fragmentu kodu.")

def update_state(manager: SnippetManager):
    """Opublikuj, oznacz jako przestarzały lub edytuj istniejący fragment kodu."""
    try:
        snippet_id = int(input("Podaj ID fragmentu kodu: ").strip())
    except ValueError:
        print("Nieprawidłowe ID. Podaj wartość liczbową.")
        return

    snippet = manager.get_snippet(snippet_id)
    if not snippet:
        print("Nie znaleziono fragmentu kodu.")
        return

    print("Wybierz akcję: ")
    print("1) Opublikuj")
    print("2) Oznacz jako przestarzały")
    print("3) Edytuj (przywróć do stanu Szkic)")
    action = input("Wybierz opcję (1-3): ").strip()

    if action == "1":
        snippet.publish()
    elif action == "2":
        snippet.deprecate()
    elif action == "3":
        snippet.edit()
    else:
        print("Nieprawidłowa akcja.")

def tag_snippet(manager: SnippetManager):
    """Dodaj tag do fragmentu kodu."""
    try:
        snippet_id = int(input("Podaj ID fragmentu kodu: ").strip())
    except ValueError:
        print("Nieprawidłowe ID. Podaj wartość liczbową.")
        return

    tag_value = input("Podaj tag do dodania: ").strip()
    success = manager.add_tag(snippet_id, tag_value)
    print("Tag dodany." if success else "Nie znaleziono fragmentu kodu.")

def untag_snippet(manager: SnippetManager):
    """Usuń tag z fragmentu kodu."""
    try:
        snippet_id = int(input("Podaj ID fragmentu kodu: ").strip())
    except ValueError:
        print("Nieprawidłowe ID. Podaj wartość liczbową.")
        return

    tag_value = input("Podaj tag do usunięcia: ").strip()
    success = manager.remove_tag(snippet_id, tag_value)
    print("Tag usunięty." if success else "Nie znaleziono fragmentu kodu lub tagu.")

def search_snippets(manager: SnippetManager):
    """Wyszukaj fragmenty kodu według języka, tagu lub tekstu."""
    print("Wybierz strategię wyszukiwania:")
    print("1) Język")
    print("2) Tag")
    print("3) Tekst (tytuł/kod)")
    strat_choice = input("Wybierz opcję (1-3): ").strip()

    query = input("Podaj wyszukiwaną frazę: ").strip()

    if strat_choice == "1":
        searcher = SnippetSearcher(LanguageRetrievalStrategy())
    elif strat_choice == "2":
        searcher = SnippetSearcher(TagRetrievalStrategy())
    elif strat_choice == "3":
        searcher = SnippetSearcher(FullTextRetrievalStrategy())
    else:
        print("Nieprawidłowa opcja wyszukiwania.")
        return

    results = searcher.search(query)
    if results:
        all_snippets = manager.list_snippets()  # słownik {id: snippet}
        for snippet in results:
            for sid, s in all_snippets.items():
                if s == snippet:
                    lang = snippet.get_language()
                    state_name = snippet._state.__class__.__name__.replace("State", "")
                    print(f"[ID={sid}] '{snippet.title}' ({lang}, {state_name})")
    else:
        print("Nie znaleziono pasujących fragmentów kodu.")

if __name__ == "__main__":
    main()
