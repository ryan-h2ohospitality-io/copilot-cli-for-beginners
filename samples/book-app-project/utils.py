def print_menu() -> None:
    print("\n📚 Book Collection App")
    print("1. Add a book")
    print("2. List books")
    print("3. Mark book as read")
    print("4. Remove a book")
    print("5. Exit")


def get_user_choice() -> str:
    """Prompt until a valid numeric choice (1-5) is entered and return it as a string."""
    while True:
        choice = input("Choose an option (1-5): ").strip()
        if not choice:
            print("No input provided. Please enter a number between 1 and 5.")
            continue
        if not choice.isdigit():
            print("Invalid input. Please enter a number between 1 and 5.")
            continue
        num = int(choice)
        if num < 1 or num > 5:
            print("Choice out of range. Please enter a number between 1 and 5.")
            continue
        return choice


def get_book_details() -> tuple[str, str, int]:
    """Prompt the user for book details and return them as a tuple.

    Behavior and prompts:
    - Title: required. The function will repeatedly prompt until a non-empty title
      is provided.
    - Author: optional. An empty string is accepted if the user provides no input.
    - Publication year: required. The function repeatedly prompts until the user
      enters an integer between 1 and the current year (inclusive).

    Returns:
      tuple[str, str, int]: (title, author, year)

    Side effects:
    - Prints prompt and validation messages to stdout. Does not accept invalid years.
    """
    while True:
        title = input("Enter book title: ").strip()
        if not title:
            print("Title cannot be empty. Please enter a valid title.")
            continue
        break

    author = input("Enter author: ").strip()

    import datetime
    current_year = datetime.date.today().year
    while True:
        year_input = input(f"Enter publication year (1-{current_year}): ").strip()
        if not year_input:
            print("Year is required. Please enter a valid year.")
            continue
        try:
            year = int(year_input)
        except ValueError:
            print("Invalid year. Please enter a numeric year.")
            continue
        if year < 1 or year > current_year:
            print(f"Year must be between 1 and {current_year}.")
            continue
        break

    return title, author, year


def print_books(books: list) -> None:
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
