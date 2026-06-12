def print_menu():
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


def get_book_details():
    """Prompt for book details; require a non-empty title.

    Returns a tuple (title, author, year).
    """
    while True:
        title = input("Enter book title: ").strip()
        if not title:
            print("Title cannot be empty. Please enter a valid title.")
            continue
        break

    author = input("Enter author: ").strip()

    year_input = input("Enter publication year: ").strip()
    try:
        year = int(year_input)
    except ValueError:
        print("Invalid year. Defaulting to 0.")
        year = 0

    return title, author, year


def print_books(books):
    if not books:
        print("No books in your collection.")
        return

    print("\nYour Books:")
    for index, book in enumerate(books, start=1):
        status = "✅ Read" if book.read else "📖 Unread"
        print(f"{index}. {book.title} by {book.author} ({book.year}) - {status}")
