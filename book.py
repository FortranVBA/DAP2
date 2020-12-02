"""Project OC DAP 2 file with book related class."""

import csv


class Book:
    """Book characteristics extracted from booktoscrape.com."""

    def __init__(self, dict_book):
        """Init Book class."""
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
        """Set book class from a dictionnary."""
        self.set_url_from_dict(dict_book)
        self.set_UPC_from_dict(dict_book)
        self.set_title_from_dict(dict_book)
        self.set_price_with_tax_from_dict(dict_book)
        self.set_price_without_tax_from_dict(dict_book)
        self.set_availability_from_dict(dict_book)
        self.set_description_from_dict(dict_book)
        self.set_category_from_dict(dict_book)
        self.set_rating_from_dict(dict_book)
        self.set_img_from_dict(dict_book)

    def set_url_from_dict(self, dict_book):
        """Set book class from a dictionnary."""
        if "url" in dict_book:
            self.url = dict_book["url"]

    def set_UPC_from_dict(self, dict_book):
        """Set book class from a dictionnary."""
        if "UPC" in dict_book:
            self.upc = dict_book["UPC"]

    def set_title_from_dict(self, dict_book):
        """Set book class from a dictionnary."""
        if "title" in dict_book:
            self.title = dict_book["title"]

    def set_price_with_tax_from_dict(self, dict_book):
        """Set book class from a dictionnary."""
        if "Price (incl. tax)" in dict_book:
            price = self.get_number(dict_book["Price (incl. tax)"])
            if price >= 0:
                self.price_with_tax = price

    def set_price_without_tax_from_dict(self, dict_book):
        """Set book class from a dictionnary."""
        if "Price (excl. tax)" in dict_book:
            price = self.get_number(dict_book["Price (excl. tax)"])
            if price >= 0:
                self.price_without_tax = price

    def set_availability_from_dict(self, dict_book):
        """Set book class from a dictionnary."""
        if "Availability" in dict_book:
            avail_number = self.get_number(dict_book["Availability"])
            if avail_number >= 0 and self.is_integer(avail_number):
                self.nb_available = int(avail_number)

    def set_description_from_dict(self, dict_book):
        """Set book class from a dictionnary."""
        if "description" in dict_book:
            self.description = dict_book["description"]

    def set_category_from_dict(self, dict_book):
        """Set book class from a dictionnary."""
        if "category" in dict_book:
            self.category = dict_book["category"]

    def set_rating_from_dict(self, dict_book):
        """Set book class from a dictionnary."""
        if "rating" in dict_book:
            valid_rating = [1, 2, 3, 4, 5]
            rating = dict_book["rating"]
            if rating in valid_rating:
                self.rating = rating

    def set_img_from_dict(self, dict_book):
        """Set book class from a dictionnary."""
        if "img" in dict_book:
            self.img = dict_book["img"]

    def get_number(self, str_number):
        """Extract numbers (including '.' character) from a string."""
        number = -1

        number_str = "".join(
            charact for charact in str_number if charact.isdigit() or charact == "."
        )

        number = float(number_str)

        return number

    def is_integer(self, n):
        """Check if numeric string is interger."""
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()


class BookData:
    """Data storage of all scraped books."""

    def __init__(self):
        """Init BookData class."""
        self.books = []

    def import_dict(self, book_raw_data):
        """Create list of Book objects from list of dictionnaries."""
        for book in book_raw_data:
            self.books.append(Book(book))

    def print_csv(self, filename):
        """Create csv file from BookData."""
        with open(filename, "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "product_page_url",
                    "universal_ product_code (upc)",
                    "title",
                    "price_including_tax",
                    "price_excluding_tax",
                    "number_available",
                    "product_description",
                    "category",
                    "review_rating",
                    "image_url",
                ]
            )

            for book in self.books:
                writer.writerow(
                    [
                        book.url,
                        book.upc,
                        book.title,
                        str(book.price_with_tax),
                        str(book.price_without_tax),
                        str(book.nb_available),
                        book.description,
                        book.category,
                        str(book.rating),
                        book.img,
                    ]
                )
