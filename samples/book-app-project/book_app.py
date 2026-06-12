import sys
from typing import List
from books import BookCollection, Book
from utils import get_book_details


# Global collection instance
collection: BookCollection = BookCollection()


def show_books(books: List[Book]) -> None:
    """Display books in a user-friendly format."""
    if not books:
        print("No books found.")
        return

    print("\nYour Book Collection:\n")

    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        print(f"{index}. [{status}] {book.title} by {book.author} ({book.year})")

    print()


def handle_list() -> None:
    books = collection.list_books()
    show_books(books)


def handle_add() -> None:
    print("\nAdd a New Book\n")

    try:
        title, author, year = get_book_details()
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError as e:
        print(f"\nInvalid input: {e}\n")
    except IOError as e:
        print(f"\nFailed to save book: {e}\n")


def handle_remove() -> None:
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    if not title:
        print("Title is required to remove a book.")
        return
    try:
        removed = collection.remove_book(title)
        if removed:
            print("\nBook removed.\n")
        else:
            print("\nBook not found.\n")
    except IOError as e:
        print(f"\nFailed to update data file: {e}\n")


def handle_find() -> None:
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    if not author:
        print("Author name required.")
        return
    books = collection.find_by_author(author)

    show_books(books)


def handle_mark_as_read() -> None:
    print("\nMark Book as Read\n")
    title = input("Enter the title of the book to mark as read: ").strip()
    if not title:
        print("Title is required.")
        return
    try:
        success = collection.mark_as_read(title)
        if success:
            print(f'\nMarked "{title}" as read.\n')
        else:
            print(f'\nBook titled "{title}" was not found.\n')
    except IOError as e:
        print(f"\nFailed to update data file: {e}\n")


def show_help() -> None:
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
  help     - Show this help message
""")


def main() -> None:
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "list":
        handle_list()
    elif command == "add":
        handle_add()
    elif command == "remove":
        handle_remove()
    elif command == "find":
        handle_find()
    elif command == "mark-as-read":
        handle_mark_as_read()
    elif command == "help":
        show_help()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
