# Books Online

## **Description**
This repository is for developing a price monitoring system for Books Online. For the beta version of this system, my program scrapes the website of one retailer—[Books to Scrape](http://books.toscrape.com/)—and extracts
the important product information, including prices, as well as an image of each product.

## **Run the Code**
Please follow the below steps in order to run the program:

● Clone this repository to a folder of your choosing\
● Open the terminal and navigate to your project folder\
● Create a virtual environment using the following command:\
_py -m venv env (Windows and macOS)_\
● Activate the virtual environment using the following command:\
_env\Scripts\activate.bat (Windows), or\
env/bin/activate (macOS)_\
● Install the Python libraries documented in the requirements.txt file:\
_pip install -r requirements.txt (Windows and macOS)_\
● Finally, run main.py using the following command:\
_py main.py_

Note that the program will take a minute or two to run to completion. You can monitor its progress by the messages printed to the terminal as the program goes through all 50 categories of books on the website, starting with Travel and ending with Crime. For each category, it will display the number of pages combed (not all categories have more than one page) and then print a message confirming that product information and images have been saved for all books in that category.

## **Output**
Product information is written to a CSV file named after each category and saved to the project folder. Images are placed in their own folder with one subfolder per category and named according to the following convention: _URL - Book Title_, where the book title is shortened as necessary.
