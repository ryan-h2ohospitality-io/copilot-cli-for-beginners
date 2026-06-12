import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False

def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    assert result is False


def test_list_by_year_normal():
    collection = BookCollection()
    collection.add_book("Old Book", "Author A", 1990)
    collection.add_book("Millennium Book", "Author B", 2000)
    collection.add_book("Modern Book", "Author C", 2010)

    results = collection.list_by_year(1995, 2005)
    titles = [b.title for b in results]
    assert titles == ["Millennium Book"]


def test_list_by_year_empty():
    collection = BookCollection()
    collection.add_book("Ancient", "A", 1800)

    results = collection.list_by_year(1900, 1950)
    assert results == []


def test_list_by_year_single_year():
    collection = BookCollection()
    collection.add_book("Single", "A", 2001)

    results = collection.list_by_year(2001, 2001)
    assert len(results) == 1
    assert results[0].title == "Single"


def test_list_by_year_swapped():
    collection = BookCollection()
    collection.add_book("StartYear", "A", 1995)
    collection.add_book("EndYear", "B", 2005)

    # pass end first; function should swap and still return both if in range
    results = collection.list_by_year(2005, 1990)
    titles = [b.title for b in results]
    assert "StartYear" in titles and "EndYear" in titles


def test_list_by_year_invalid_inputs():
    collection = BookCollection()
    with pytest.raises(TypeError):
        collection.list_by_year("2000", 2010)
