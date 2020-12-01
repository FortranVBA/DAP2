"""Project OC DAP 2 main file."""

from parsers import WebHandler
from book import BookData


class Application:
    """Project application class."""

    def __init__(self):
        self.web_handler = WebHandler()
        self.book_data = BookData()

    def run(self):
        self.web_handler.load("http://books.toscrape.com")

        raw_extract_books = self.web_handler.extract_products()
        # print(raw_extract_books[0])
        self.book_data.import_dict(raw_extract_books)

        self.book_data.print_csv("books.csv")


def main():
    """Program entry point."""
    app = Application()
    app.run()


if __name__ == "__main__":
    main()