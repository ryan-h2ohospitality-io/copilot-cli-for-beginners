# Book Collection App

*(This README is intentionally rough so you can improve it with GitHub Copilot CLI)*

A Python app for managing books you have or want to read.
It can add, remove, and list books. Also mark them as read.

---

## Current Features

* Reads books from a JSON file (our database)
* Input checking is weak in some areas
* Some tests exist but probably not enough

---

## Files

* `book_app.py` - Main CLI entry point
* `books.py` - BookCollection class with data logic
  * Developer API: BookCollection.list_by_year(start, end) — returns books whose publication year is within the inclusive range [start, end].
* `utils.py` - Helper functions for UI and input
* `data.json` - Sample book data
* `tests/test_books.py` - Starter pytest tests

---

## Running the App

```bash
python book_app.py list
python book_app.py add
python book_app.py mark-as-read
python book_app.py find
python book_app.py remove
python book_app.py help
```

## Running Tests

```bash
python -m pytest tests/
```

---

## Notes

* Not production-ready (obviously)
* Some code could be improved
* Could add more commands later

## Year validation

* Programmatic/API: BookCollection.add_book(title, author, year) accepts year == 0 to denote an unknown publication year. It rejects negative values and any year greater than the current year (i.e., future years).
* CLI behavior: The interactive "add" flow requires entering a numeric publication year between 1 and the current year (inclusive). The prompt will re-ask on invalid input. To record an unknown year (0), edit `data.json` directly or use the programmatic API.
* Rationale: This preserves existing sample data that uses 0 for unknown while preventing accidental future-year entries. Tests cover these cases.
