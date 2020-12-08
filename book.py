"""Project OC DAP 2 file with book related class."""

import csv
import time
from time import sleep
from parsers import WebGetter
from random import uniform
from pathlib import Path
from config import PRINT_MODULO_FREQ
from config import REQUEST_WAIT_RANGE
from config import Field
from config import path


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
        if Field.url in dict_book:
            self.url = dict_book[Field.url]

    def set_UPC_from_dict(self, dict_book):
        """Set book class from a dictionnary."""
        if Field.UPC in dict_book:
            self.upc = dict_book[Field.UPC]

    def set_title_from_dict(self, dict_book):
        """Set book class from a dictionnary."""
        if Field.title in dict_book:
            self.title = dict_book[Field.title]

    def set_price_with_tax_from_dict(self, dict_book):
        """Set book class from a dictionnary."""
        if Field.price_with_tax in dict_book:
            price = self.get_number(dict_book[Field.price_with_tax])
            if price >= 0:
                self.price_with_tax = price

    def set_price_without_tax_from_dict(self, dict_book):
        """Set book class from a dictionnary."""
        if Field.price_without_tax in dict_book:
            price = self.get_number(dict_book[Field.price_without_tax])
            if price >= 0:
                self.price_without_tax = price

    def set_availability_from_dict(self, dict_book):
        """Set book class from a dictionnary."""
        if Field.availability in dict_book:
            avail_number = self.get_number(dict_book[Field.availability])
            if avail_number >= 0 and self.is_integer(avail_number):
                self.nb_available = int(avail_number)

    def set_description_from_dict(self, dict_book):
        """Set book class from a dictionnary."""
        if Field.description in dict_book:
            self.description = dict_book[Field.description]

    def set_category_from_dict(self, dict_book):
        """Set book class from a dictionnary."""
        if Field.category in dict_book:
            self.category = dict_book[Field.category]

    def set_rating_from_dict(self, dict_book):
        """Set book class from a dictionnary."""
        if Field.rating in dict_book:
            valid_rating = [1, 2, 3, 4, 5]
            rating = dict_book[Field.rating]
            if rating in valid_rating:
                self.rating = rating

    def set_img_from_dict(self, dict_book):
        """Set book class from a dictionnary."""
        if Field.img in dict_book:
            self.img = dict_book[Field.img]

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
        self.categories = []

    def import_dict(self, book_raw_data):
        """Create list of Book objects from list of dictionnaries."""
        for book in book_raw_data:
            self.books.append(Book(book))
            self.update_categories(self.books[-1].category)

    def update_categories(self, category):
        """Update the list of book categories included in BookData."""
        if category not in self.categories:
            self.categories.append(category)

    def print_global_csv(self, filename):
        """Create csv file from BookData."""
        path_csv = Path()

        path_csv = path.absolute() / filename
        with path_csv.open(mode="w", encoding="utf-8") as file:
            writer = csv.writer(file)
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

    def print_category_csv(self):
        """Create one csv files per category from BookData."""
        path_csv = Path()
        for category in self.categories:
            path_csv = path.absolute() / "csv"
            path_csv.mkdir(parents=True, exist_ok=True)

            file_name = self.get_valid_file_name(category) + ".csv"

            path_csv = path_csv / file_name

            with path_csv.open(mode="w", encoding="utf-8") as file:
                writer = csv.writer(file)
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
                    if book.category == category:
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

    def download_all_img(self):
        """Download all img files from BookData."""
        # Preparing the monitoring of the loop
        start_time = time.time()
        requests = 0

        for book in self.books:

            # Monitor the requests
            sleep(uniform(REQUEST_WAIT_RANGE[0], REQUEST_WAIT_RANGE[1]))
            requests += 1
            elapsed_time = time.time() - start_time
            self.print_request_status(requests, elapsed_time, PRINT_MODULO_FREQ)

            self.download_img(book.category, book.title, book.img)

    def download_img(self, category, title, img):
        """Download img file from one book data."""
        web_getter = WebGetter()

        web_getter.get(img)
        file_name = self.get_valid_file_name(title) + ".jpg"

        path_file = Path()
        path_download = Path()

        path_file = path.absolute() / "images" / category
        path_file.mkdir(parents=True, exist_ok=True)

        path_download = path.absolute() / "images" / category / file_name

        with path_download.open(mode="wb") as file:
            file.write(web_getter.response.content)

    def get_valid_file_name(self, title):
        """Truncate file name if too big and remove forbidden characters."""
        valid_name = title[:20]

        forbidden_char = ["/", '""', ":", "*", "?", '"', ">", "<"]

        for char in forbidden_char:
            valid_name = valid_name.replace(char, "-")

        return valid_name

    def print_request_status(self, requests, elapsed_time, print_modulo):
        """Print the request status progression every print_modulo requests."""
        if requests % print_modulo == 0 or requests == 1:
            print(
                "Download request:{}; Frequency: {} requests/s".format(
                    requests, requests / elapsed_time
                )
            )
