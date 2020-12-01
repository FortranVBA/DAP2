"""Project OC DAP 2 main file."""

from requests import get
from bs4 import BeautifulSoup
from time import sleep
from random import randint


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

        product["title"] = self.get_title()

        product["description"] = self.get_description()

        product["category"] = self.get_category()

        product["rating"] = self.get_rating()

        product["img"] = self.get_img()

        rawtable = self.parsed_url.find("table", class_="table table-striped")
        product.update(self.cleanrawtable(rawtable))

        return product

    def cleanrawtable(self, rawtable):
        cleantable = {}

        tablerow = rawtable.find_all("tr")
        for row in tablerow:
            propertyname = row.th.text.replace("</th>", "").replace("<th>", "")
            propertyvalue = row.td.text.replace("</td>", "").replace("<td>", "")
            cleantable[propertyname] = propertyvalue

        return cleantable

    def get_description(self):
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
        category = ""

        parse_tags_li = self.parsed_url.find("ul", class_="breadcrumb").find_all("li")

        if parse_tags_li is not None:
            category = parse_tags_li[2].text.strip("\r\n")

        return category

    def get_rating(self):
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
        img_src = ""

        parsed_img = self.parsed_url.find("div", class_="item active").find("img")[
            "src"
        ]
        img_src = parsed_img.replace("../..", "http://books.toscrape.com/catalogue")

        return img_src

    def get_title(self):
        title = ""

        parsed_title = self.parsed_url.find("div", class_="col-sm-6 product_main").find(
            "h1"
        )
        title = parsed_title.text

        return title


class WebHandler:
    """Handle data conversion and extraction from an url string."""

    def __init__(self):
        self.data_extractor = DataExtractor()
        self.books_links = []
        self.books_data = []

    def load(self, url):
        self.data_extractor.load_data(url)

    def extract_products(self):
        """Get all product properties inside parsed url with several product links."""
        self.books_links = self.data_extractor.getbooklinks()

        self.books_data = []

        # For loop
        self.load(
            "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"
        )
        self.books_data.append(self.data_extractor.getproductdata())
        # sleep(randint(2, 7))

        return self.books_data

    def extract_categories(self):
        pass
