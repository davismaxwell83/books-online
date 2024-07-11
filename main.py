import requests
import datetime
import csv
from bs4 import BeautifulSoup
import re

# Phase 3
# Visit the Books to Scrape home page and extract the links to all the available book categories.
def home_page():
    page = requests.get('https://books.toscrape.com/index.html')

    soup = BeautifulSoup(page.content, 'html.parser')

    category_urls = []
    category_names = []
    category_elements = soup.select('a[href*=category]')

    # Skip 1st element, which corresponds to "Books" category header, not an individual category
    for i in range(1,
                   len(category_elements)):
        category_url = "https://books.toscrape.com/" + category_elements[i]['href']
        category_name = category_elements[i].get_text().strip('\n            ')
        category_urls.append(category_url)
        category_names.append(category_name)

    categories = {"category_url": category_urls, "category_name": category_names}
    # print("Dictionary of category URLS and names: ", categories)
    return categories

# Phase 2
# Extract the product page URLs for all books in a single category.
def category(category_page_url):

    is_next = 1
    page_num = 1
    category_book_urls = []
    category_book_titles = []
    while is_next == 1:
        page = requests.get(category_page_url)

        soup = BeautifulSoup(page.content, 'html.parser')

        category_name = soup.find('ul').find_all('li')[2].get_text().strip('\n')
        category_title_elements = soup.find_all('h3')

        for i in range(len(category_title_elements)):
            book_url = "https://books.toscrape.com/catalogue/" + category_title_elements[i].find('a')['href'].strip(
                '../../../')
            # print(f"URL of book #{i + 1}:", book_url)
            book_title = category_title_elements[i].find('a')['title']
            # print(f"Title of book #{i + 1}:", book_title)
            category_book_urls.append(book_url)
            category_book_titles.append(book_title)
        is_next = len(soup.select('li[class*=next]'))
        # If there is a 'next' page, then update the page URL accordingly
        if is_next == 1:
            print(category_name + ", " +
                  soup.select('li[class*=current]')[0].get_text().strip('\n            '))
            page_num += 1
            if category_page_url.endswith('index.html'):
                category_page_url = category_page_url.replace('index.html', 'page-'+str(page_num)+'.html')
            else:
                category_page_url = category_page_url.replace('page-'+str(page_num-1)+'.html', 'page-'+str(page_num)+'.html')
                # page_num = int(re.findall(r'\d+', soup.select('li[class*=next]')[0].find('a')['href'])[0])
        elif page_num == 1:
            print(category_name + ", Page 1 of 1")
        elif page_num > 1:
            print(category_name + ", " +
                  soup.select('li[class*=current]')[0].get_text().strip('\n            '))

    # print("List of book URLS: ", category_book_urls)
    # print("List of book titles: ", category_book_titles)
    category_books = {"product_page_url": category_book_urls, "book_title": category_book_titles}
    # print("Dictionary of book URLS and titles: ", category_books)
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
    if soup.find('h2', string=lambda s: 'Product Description' in s) is None:
        product_description = ''
    else:
       product_description = soup.find('h2', string=lambda s: 'Product Description' in s).find_next('p').string.replace(
        '…', '...').replace(' ', '').replace(u"\u203D", '')
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


def load(data_to_load, category_name):
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
    with open(category_name + '.csv', mode='w', newline='', encoding='utf-8') as file:
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

    # category_page_url = input(
    #     "Enter the URL for a single category: ")  # "https://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html"
    # print("Now extracting product information from:")
    print("Visiting the Books to Scrape homepage and extracting all available book categories.")
    categories = home_page()
    for h in range(len(categories['category_url'])):
        category_url = categories['category_url'][h]
        category_name = categories['category_name'][h]
        category_books = category(category_url)
        data_to_load = []
        for i in range(len(category_books['product_page_url'])):
            product_page_url = category_books['product_page_url'][i]
            # print(f"URL of book #{i + 1}:", product_page_url)
            # print(f"Title of book #{i + 1}:", category_books['book_title'][i])
            product_info = product(product_page_url)
            data_to_load.append(product_info)
        load(data_to_load, category_name)
        print("Extracted product information has now been written to a CSV file.")

if __name__ == "__main__":
    main()
