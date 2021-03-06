# Openclassroom Dev Application Python - Projet 2

## Description

This project is part of the training of Python Web Developer online course provided by OpenClassroom.
The purpose of this project is to develop a python executable that will scrape the book data from https://books.toscrape.com
The program will search the main page for all book categories, open each category catalogue main page and extract all book product data through all catalogue pages.

The following data fields will be extracted :
- product_page_url
- universal_ product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url

Data are written inside csv files (one per book category).

All image files are also downloaded and classified by book category folders.

## Requirements

- Python 3.7 or higher (developed and tested with python 3.7.1)

## Installation

1. Download the repository content.
2. From project root folder, type in vscode (or other python interpretor for Windows) or your OS terminal (Linux or Mac OS) 
    ```python -m venv .venv #Create a new environment.```
3. Type in vscode (or other python interpretor for Windows) or your OS terminal (Linux or Mac OS) 
    - For windows: ```. .venv/Scripts/activate #Activate your new environment.```
    - For MAC OS / Linux: ```. .venv/bin/activate #Activate your new environment.```
4. Type in vscode (or other python interpretor for Windows) or your OS terminal (Linux or Mac OS)
    ```pip install -r requirements.txt #Install all required librairies.```

## Operation

- Activate your environment (you may have already done it during the installation steps, but you need to re-activate it each time you close your terminal / vscode and start with a new terminal).
You can do so by typing in vscode (or other python interpretor for Windows) or your OS terminal (Linux or Mac OS):
    - For windows: ```. .venv/Scripts/activate #Activate your new environment.```
    - For MAC OS / Linux: ```. .venv/bin/activate #Activate your new environment.```

- Execute main.py from project root folder:
    - Type ```python main.py``` in terminal (vscode or other python interpretor for Windows)
    - Or type ```python3 main.py``` in terminal (Linux or Mac OS)

- The program will print in terminal:
    * The current scrapped catalogue page
    * The 1st and every 5 (this number can be changed with ```PRINT_MODULO_FREQ``` variable in config.py file) requests, the number of requests done in the current catalogue page and the average request speed (speed can be adjusted by changing the ```REQUEST_WAIT_RANGE``` variable in config.py file, which is the range in seconds used as waiting time between request).  
    * After retrieving data, the 1st and every 5 (this number can be changed with ```PRINT_MODULO_FREQ``` variable in config.py file) requests,  the number of requests done for image download and the average request speed (speed can be adjusted by changing the ```REQUEST_WAIT_RANGE``` variable in config.py file, which is the range in seconds used as waiting time between request).

- After the program ended, you can find in :
    * csv folder, all csv files (one per book category)
    * images folder, all downloaded image (classified by category folders)
