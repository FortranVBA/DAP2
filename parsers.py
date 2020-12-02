"""Project OC DAP 2 file with web handler, parsing and data extraction related class."""

import time
from time import sleep
from requests import get
from bs4 import BeautifulSoup
from random import uniform


class WebGetter:
    """Get a server response from an url string."""

    def __init__(self):
        """Init WebGetter class."""
        self.response = None

    def get(self, url):
        """Get server response from url string."""
        response = get(url)

        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            print(
                "Warning for url: {}; Status code: {}".format(url, response.status_code)
            )

        self.response = response


class Parser:
    """Get a parsed page from a server response."""

    def __init__(self):
        """Init Parser class."""
        self.parsed_url = None

    def parse(self, response):
        """Parse server response with Beautiful Soup."""
        self.parsed_url = BeautifulSoup(response.text, "html.parser")


class DataExtractor:
    """Handle data extraction from a parsed url."""

    def __init__(self):
        """Init DataExtractor class."""
        self.url = ""
        self.parsed_url = None
        self.books_links = []

    def load_data(self, url):
        """Load parsed data from url string."""
        webgetter = WebGetter()
        parser = Parser()

        webgetter.get(url)
        parser.parse(webgetter.response)

        self.url = url
        self.parsed_url = parser.parsed_url

    def get_book_links(self):
        """Get list of book url links from loaded parsed web page."""
        parsed_books_data = self.parsed_url.find_all("article", class_="product_pod")
        self.books_links = []

        for tag in parsed_books_data:
            link_parsed = tag.find("a")["href"]
            if "catalogue" in link_parsed:
                link_parsed = "http://books.toscrape.com/" + link_parsed
            elif "../" in link_parsed:
                link_parsed = link_parsed.replace("../", "")
                link_parsed = "http://books.toscrape.com/catalogue/" + link_parsed

            self.books_links.append(link_parsed)

        return self.books_links

    def get_product_data(self):
        """Return product properties from loaded parsed web page."""
        product = {}

        product["url"] = self.url

        product["title"] = self.get_title()

        product["description"] = self.get_description()

        product["category"] = self.get_category()

        product["rating"] = self.get_rating()

        product["img"] = self.get_img()

        rawtable = self.parsed_url.find("table", class_="table table-striped")
        product.update(self.table_to_dict(rawtable))

        return product

    def table_to_dict(self, rawtable):
        """Transform parsed table into dictionnary."""
        cleantable = {}

        tablerow = rawtable.find_all("tr")
        for row in tablerow:
            propertyname = row.th.text.replace("</th>", "").replace("<th>", "")
            propertyvalue = row.td.text.replace("</td>", "").replace("<td>", "")
            cleantable[propertyname] = propertyvalue

        return cleantable

    def get_description(self):
        """Get book description from loaded parsed page."""
        match_count = 0
        description = ""

        parse_tags_p = self.parsed_url.find("article", class_="product_page").find_all(
            "p"
        )

        for tag in parse_tags_p:
            if "<p>" in str(tag):
                description = tag.prettify("latin-1")
                match_count += 1

        if match_count == 0:
            description = "No description found."
        elif match_count > 1:
            description = "Error : several tags p found for product description."

        return description

    def get_category(self):
        """Get book category from loaded parsed page."""
        category = ""

        parse_tags_li = self.parsed_url.find("ul", class_="breadcrumb").find_all("li")

        if parse_tags_li is not None:
            category = parse_tags_li[2].text.strip("\r\n")

        return category

    def get_rating(self):
        """Get book rating from loaded parsed page."""
        rating = -1

        parsed_rating = self.parsed_url.find("div", class_="col-sm-6 product_main")
        if parsed_rating.find("p", class_="star-rating One") is not None:
            rating = 1
        elif parsed_rating.find("p", class_="star-rating Two") is not None:
            rating = 2
        elif parsed_rating.find("p", class_="star-rating Three") is not None:
            rating = 3
        elif parsed_rating.find("p", class_="star-rating Four") is not None:
            rating = 4
        elif parsed_rating.find("p", class_="star-rating Five") is not None:
            rating = 5

        return rating

    def get_img(self):
        """Get book image url from loaded parsed page."""
        img_src = ""

        parsed_img = self.parsed_url.find("div", class_="item active").find("img")[
            "src"
        ]
        img_src = parsed_img.replace("../..", "http://books.toscrape.com/catalogue")

        return img_src

    def get_title(self):
        """Get book title from loaded parsed page."""
        title = ""

        parsed_title = self.parsed_url.find("div", class_="col-sm-6 product_main").find(
            "h1"
        )
        title = parsed_title.text

        return title


class WebHandler:
    """Handle data conversion and extraction from an url string."""

    def __init__(self):
        """Init WebHandler class."""
        self.data_extractor = DataExtractor()
        self.books_links = []
        self.books_data = []
        self.PRINT_MODULO_FREQ = 5
        self.REQUEST_WAIT_RANGE = [1, 3]

    def load(self, url):
        """Load url for future parsing and data extraction."""
        self.data_extractor.load_data(url)

    def extract_products(self):
        """Get all product properties in loaded parsed url."""
        self.books_links = self.data_extractor.get_book_links()

        self.books_data = []

        # Preparing the monitoring of the loop
        start_time = time.time()
        requests = 0

        for link_book in self.books_links:
            # Monitor the requests
            sleep(uniform(self.REQUEST_WAIT_RANGE[0], self.REQUEST_WAIT_RANGE[1]))
            requests += 1
            elapsed_time = time.time() - start_time
            self.print_request_status(requests, elapsed_time, self.PRINT_MODULO_FREQ)

            self.load(link_book)
            self.books_data.append(self.data_extractor.get_product_data())

        return self.books_data

    def extract_categories(self):
        """Get all category urls from loaded parsed url."""
        pass

    def print_request_status(self, requests, elapsed_time, print_modulo):
        """Print the request status progression every print_modulo requests."""
        if requests % print_modulo == 0 or requests == 1:
            print(
                "Request:{}; Frequency: {} requests/s".format(
                    requests, requests / elapsed_time
                )
            )
