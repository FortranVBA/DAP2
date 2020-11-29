"""Project OC DAP 2 main file."""

from requests import get
from bs4 import BeautifulSoup


class WebGetter:
    """Get a server response from an url string."""

    def __init__(self):
        self.response = None

    def get(self, url):
        self.response = get(url)


class Parser:
    """Get a parsed page from a server response."""

    def __init__(self):
        self.parsed_url = None

    def parse(self, response):
        self.parsed_url = BeautifulSoup(response.text, "html.parser")


class DataExtractor:
    """Handle data extraction from a parsed url."""

    def __init__(self):
        self.url = ""
        self.parsed_url = None
        self.books_links = []

    def load_data(self, url):

        webgetter = WebGetter()
        parser = Parser()

        webgetter.get(url)
        parser.parse(webgetter.response)

        self.url = url
        self.parsed_url = parser.parsed_url

    def getbooklinks(self):
        parsed_books_data = self.parsed_url.find_all("article", class_="product_pod")
        self.books_links = []

        for tag in parsed_books_data:
            self.books_links.append(
                tag.find("a")["href"].replace(
                    "../..", "http://books.toscrape.com/catalogue"
                )
            )

        return self.books_links

    def getproductdata(self):
        product = {}

        product["url"] = self.url

        rawtable = self.parsed_url.find("table", class_="table table-striped")
        product.update(self.cleanrawtable(rawtable))
        print(product)

    def cleanrawtable(self, rawtable):
        cleantable = {}

        tablerow = rawtable.find_all("tr")
        for row in tablerow:
            propertyname = row.th.text.replace("</th>", "").replace("<th>", "")
            propertyvalue = row.td.text.replace("</td>", "").replace("<td>", "")
            cleantable[propertyname] = propertyvalue

        return cleantable


class WebHandler:
    """Handle data conversion and extraction from an url string."""

    def __init__(self):
        self.data_extractor = DataExtractor()
        self.books_links = []

    def load(self, url):
        self.data_extractor.load_data(url)

    def extract_products(self):
        """Get all product properties inside parsed url with several product links."""
        self.books_links = self.data_extractor.getbooklinks()
        # For loop
        self.load(
            "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
        )
        self.data_extractor.getproductdata()

    def extract_categories(self):
        pass
