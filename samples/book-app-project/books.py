import json
from dataclasses import dataclass, asdict
from typing import List, Optional

DATA_FILE = "data.json"


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False


class BookCollection:
    def __init__(self) -> None:
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        """Load books from the JSON file if it exists."""
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self) -> None:
        """Save the current book collection to JSON."""
        try:
            with open(DATA_FILE, "w") as f:
                json.dump([asdict(b) for b in self.books], f, indent=2)
        except OSError as e:
            # Surface I/O errors so callers (CLI/tests) can handle them.
            raise IOError(f"Failed to write data file {DATA_FILE}: {e}") from e

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Add a new book to the collection after validating inputs.

        Raises ValueError for invalid title or year, IOError for file write errors.
        """
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title must be a non-empty string")
        import datetime
        current_year = datetime.date.today().year
        # Enforce a publication year between 1 and the current year (inclusive).
        if not isinstance(year, int) or year < 1:
            raise ValueError(f"year must be an integer between 1 and {current_year} (inclusive)")
        if year > current_year:
            raise ValueError(f"year cannot be in the future (max {current_year})")

        book = Book(title=title.strip(), author=author.strip(), year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        return self.books

    def list_by_year(self, start: int, end: int) -> List[Book]:
        """Return books with publication year in the inclusive range [start, end].

        Args:
            start (int): Start year (inclusive).
            end (int): End year (inclusive).

        Returns:
            List[Book]: List of books whose .year falls between start and end.

        Raises:
            TypeError: If start or end is not an int.
        """
        if not isinstance(start, int) or not isinstance(end, int):
            raise TypeError("start and end must be integers")

        # Normalize range so callers don't need to pre-order arguments.
        if start > end:
            start, end = end, start

        return [b for b in self.books if start <= b.year <= end]

    def find_book_by_title(self, title: str) -> Optional[Book]:
        """Find a book by exact title match (case-insensitive).

        Trims surrounding whitespace from the query and validates the input type.
        Returns the first matching Book or None if not found.
        """
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        query = title.strip()
        if not query:
            return None
        for book in self.books:
            if book.title.lower() == query.lower():
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title."""
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author (supports partial, case-insensitive matches).

        Args:
            author (str): Partial or full author name to search for.

        Returns:
            List[Book]: Books whose author contains the query string.
        """
        if not isinstance(author, str):
            raise TypeError("author must be a string")
        query = author.strip().lower()
        if not query:
            return []
        return [b for b in self.books if query in b.author.lower()]
