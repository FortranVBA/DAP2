"""Project OC DAP 2 main file."""

from parsers import WebHandler
from book import BookData


class Application:
    """Project application class."""

    def __init__(self):
        """Init Application class."""
        self.web_handler = WebHandler()
        self.book_data = BookData()

    def run(self):
        """Run  Application class."""
        self.web_handler.load("http://books.toscrape.com")
        category_links = self.web_handler.extract_categories()
        raw_extract_books = []

        for link in category_links:
            print(link)
            self.web_handler.load(link)
            next_page = self.web_handler.get_next_page()
            raw_extract_books = raw_extract_books + self.web_handler.extract_products()

            while next_page != "None":
                print(next_page)
                self.web_handler.load(next_page)
                next_page = self.web_handler.get_next_page()
                raw_extract_books = (
                    raw_extract_books + self.web_handler.extract_products()
                )

        self.book_data.import_dict(raw_extract_books)

        self.book_data.print_category_csv()
        self.book_data.download_all_img()


def main():
    """Program entry point."""
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
