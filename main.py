import requests
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

# Step 1 : Extraction of desired information with Beautiful Soup
product_page_url = "https://books.toscrape.com/catalogue/ready-player-one_209/index.html"
page = requests.get(product_page_url)

soup = BeautifulSoup(page.content, 'html.parser')

# Extraction of the required information above
full_title = soup.title.string
book_title = full_title.split('\n    ')[1].split(' |')[0]

# table_elements = soup.find_all('td')
# universal_product_code = table_elements[0]
# price_including_tax = table_elements[3] # try float(table_elements[3].replace("£","")) if this needs to be numeric
# price_excluding_tax = table_elements[2] # try float(table_elements[2].replace("£","")) if this needs to be numeric
# quantity_available = table_elements[5].string.split()[2].strip('(')
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


end
# Write to CSV
#Create list for the headers
headers = ["title", "description"]

#Open a new file to write to called ‘data.csv’
with open('data.csv', 'w', newline='') as csvfile:
    #Create a writer object with that file
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(headers)
    #Loop through each element in titles and descriptions lists
    for i in range(len(titles)):
        #Create a new row with the title and description at that point in the loop
        row = [titles[i], descriptions[i]]
        writer.writerow(row)