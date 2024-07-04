import requests
import datetime
import csv
from bs4 import BeautifulSoup


# Phase 2
# Extract the product page URLs for all books in a single category
def category(category_page_url):
    page = requests.get(category_page_url)

    soup = BeautifulSoup(page.content, 'html.parser')

    category_name = soup.find('ul').find_all('li')[2].get_text().strip('\n')
    print("Category of the entered URL:", category_name)
    category_title_elements = soup.find_all('h3')
    category_book_urls = []
    category_book_titles = []
    for i in range(len(category_title_elements)):
        book_url = "https://books.toscrape.com/catalogue/" + category_title_elements[i].find('a')['href'].strip(
            '../../../')
        # print(f"URL of book #{i + 1}:", book_url)
        book_title = category_title_elements[i].find('a')['title']
        # print(f"Title of book #{i + 1}:", book_title)
        category_book_urls.append(book_url)
        category_book_titles.append(book_title)
    # print("List of book URLS: ", category_book_urls)
    # print("List of book titles: ", category_book_titles)
    category_books = {"product_page_url": category_book_urls, "book_title": category_book_titles}
    print("Dictionary of book URLS and titles: ", category_books)
    return category_books


# Phase 1
# Pick any single product page (i.e., a single book) on Books to Scrape, and write a
# Python script that visits this page and extracts the following information:
# ● product_page_url
# ● universal_product_code (upc)
# ● book_title
# ● price_including_tax
# ● price_excluding_tax
# ● quantity_available
# ● product_description
# ● category
# ● review_rating
# ● image_url
# Write the data to a CSV file using the above fields as column headings.

# Phase 1, Step 1 : Extract required information with Beautiful Soup
def product(product_page_url):
    page = requests.get(product_page_url)

    soup = BeautifulSoup(page.content.decode("utf-8"), 'html.parser')

    full_title = soup.title.string
    book_title = full_title.split('\n    ')[1].split(' |')[0]

    table_elements = soup.find_all('tr')
    table_elements_list = []
    for element in table_elements:
        match element.find('th').get_text():
            case 'UPC':
                universal_product_code = element.find('td').get_text()
            case 'Price (incl. tax)':
                price_including_tax = element.find('td').get_text()
            case 'Price (excl. tax)':
                price_excluding_tax = element.find('td').get_text()
            case 'Availability':
                quantity_available = element.find('td').get_text().split()[2].strip('(')
        # table_elements_list.append(price_including_tax)
    product_description = soup.find('h2', string=lambda s: 'Product Description' in s).find_next('p').string.replace('…', '...').replace(' ', '')
    category = soup.find('ul').find_all('li')[2].get_text().strip('\n')
    review_rating = soup.select('p[class*=star-rating]')[0]['class'][1]
    image_url = soup.find('img')['src']

    # Save extracted information to lists of strings
    # product_page_urls = [product_page_url]
    # universal_product_code = [universal_product_code]
    # book_titles = [book_title]
    # prices_including_tax = [price_including_tax]
    # prices_excluding_tax = [price_excluding_tax]
    # quantities_available = [quantity_available]
    # product_descriptions = [product_description]
    # categories = [category]
    # review_ratings = [review_rating]
    # image_urls = [image_url]

    # Save extracted information to a dictionary instead
    product_info = {"product_page_url": product_page_url, "universal_product_code": universal_product_code,
                    "book_title": book_title, "price_including_tax": price_including_tax,
                    "price_excluding_tax": price_excluding_tax, "quantity_available": quantity_available,
                    "product_description": product_description, "category": category, "review_rating": review_rating,
                    "image_url": image_url}

    return product_info


def load(data_to_load):
    # Create list for the headers
    headers = ["product_page_url",
               "universal_product_code",
               "book_title",
               "price_including_tax",
               "price_excluding_tax",
               "quantity_available",
               "product_description",
               "category",
               "review_rating",
               "image_url"]

    # Open a new file to write to and select a name which describes the output (e.g., name, output type, timestamps)
    # with open(category + ' - Product Information ' + datetime.datetime.now().strftime('%m.%d.%y %H.%M.%S') + '.csv',
    #           'w', newline='') as csvfile:
    with open('output.csv', mode='w', newline='') as file:
        # Create a writer object with that file
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for data in data_to_load:
            writer.writerow(data)


def main():
    # product_page_url = input(
    #     "Enter the URL for a single book: ")  # "https://books.toscrape.com/catalogue/ready-player-one_209/index.html"
    #
    # product(product_page_url)

    category_page_url = input(
        "Enter the URL for a single category: ")  # "https://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html"
    category_books = category(category_page_url)
    data_to_load = []
    for i in range(len(category_books['product_page_url'])):
        product_page_url = category_books['product_page_url'][i]
        print(f"URL of book #{i + 1}:", product_page_url)
        print(f"Title of book #{i + 1}:", category_books['book_title'][i])
        product_info = product(product_page_url)
        data_to_load.append(product_info)
    load(data_to_load)


if __name__ == "__main__":
    main()
