import requests
import datetime
import csv
from bs4 import BeautifulSoup

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
product_page_url = "https://books.toscrape.com/catalogue/ready-player-one_209/index.html"
page = requests.get(product_page_url)

soup = BeautifulSoup(page.content, 'html.parser')

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
product_description = soup.find('h2', string=lambda s: 'Product Description' in s).find_next('p').string
category = soup.find('ul').find_all('li')[2].get_text().strip('\n')
review_rating = soup.select('p[class*=star-rating]')[0]['class'][1]
image_url = soup.find('img')['src']

# Save extracted information to lists of strings
product_page_urls = [product_page_url]
universal_product_code = [universal_product_code]
book_titles = [book_title]
prices_including_tax = [price_including_tax]
prices_excluding_tax = [price_excluding_tax]
quantities_available = [quantity_available]
product_descriptions = [product_description]
categories = [category]
review_ratings = [review_rating]
image_urls = [image_url]

# Phase 1, Step 2 : Write data to CSV file
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


# Open a new file to write to and select a name which describes the output (e.g., the item's name, the output type,
# timestamps)
with open(book_title + ' - Product Information ' + datetime.datetime.now().strftime('%m.%d.%y %H.%M.%S') + '.csv', 'w', newline='') as csvfile:
    # Create a writer object with that file
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(headers)
    # Loop through each element in extracted information lists
    for i in range(len(product_page_urls)):
        # Create a new row with the extracted information at that point in the loop
        row = [product_page_urls[i], universal_product_code[i], book_titles[i], prices_including_tax[i], prices_excluding_tax[i], quantities_available[i], product_descriptions[i], categories[i], review_ratings[i], image_urls[i]]
        writer.writerow(row)