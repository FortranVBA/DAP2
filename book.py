"""Project OC DAP 2 main file."""


class Book:
    """Book characteristics extracted from booktoscrape.com."""

    def __init__(self, dict_book):
        self.url = "Unknown"
        self.upc = "Unknown"
        self.title = "Unknown"
        self.price_with_tax = -1
        self.price_without_tax = -1
        self.nb_available = -1
        self.description = "Unknown"
        self.category = "Unknown"
        self.rating = -1
        self.img = "Unknown"

        self.set_from_dict(dict_book)

    def set_from_dict(self, dict_book):
        self.url = dict_book["url"]
        self.upc = dict_book["UPC"]
        self.title = dict_book["title"]
        self.price_with_tax = self.get_number(dict_book["Price (incl. tax)"])
        self.price_without_tax = self.get_number(dict_book["Price (excl. tax)"])
        self.nb_available = self.get_number(dict_book["Availability"])
        self.description = dict_book["description"]
        self.category = dict_book["category"]
        self.rating = dict_book["rating"]
        self.img = dict_book["img"]

    def get_number(self, str_number):
        number = -1

        number_str = "".join(
            charact for charact in str_number if charact.isdigit() or charact == "."
        )

        number = float(number_str)

        return number


class BookData:
    """Data storage of all scraped books."""

    def __init__(self):
        self.books = []

    def import_dict(self, book_raw_data):

        for book in book_raw_data:
            self.books.append(Book(book))

        print(self.books[0].upc)
