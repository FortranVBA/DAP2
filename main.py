"""Project OC DAP 2 main file."""

from parsers import WebHandler


class Application:
    """Project application class."""

    def __init__(self):
        self.web_handler = WebHandler()

    def run(self):
        self.web_handler.load("http://books.toscrape.com")
        self.web_handler.extract_products()


def main():
    """Program entry point."""
    app = Application()
    app.run()


if __name__ == "__main__":
    main()