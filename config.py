"""Project OC DAP 2 file with config related variables and class."""
from pathlib import Path

path = Path()
PRINT_MODULO_FREQ = 5
REQUEST_WAIT_RANGE = [1, 3]


class Field:
    """Object with field string names matchings."""

    url = "url"
    title = "title"
    description = "description"
    category = "category"
    rating = "rating"
    img = "img"
    price_with_tax = "Price (incl. tax)"
    price_without_tax = "Price (excl. tax)"
    availability = "Availability"
    UPC = "UPC"
