import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://www.amazon.in/s"
params = {
    "k": "bags",
    "crid": "2M096C61O4MLT",
    "qid": "1653308124",
    "sprefix": "ba,aps,283",
    "ref": "sr_pg_1"
}

product_data = []

for page_number in range(1, 21):  # Adjust the range if needed
    params["page"] = str(page_number)
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')
    product_listings = soup.find_all("div", {"data-component-type": "s-search-result"})

    for product in product_listings:
        product_url_element = product.find("a", {"class": "s-link-inherit"})
        if product_url_element:
            product_url = product_url_element["href"]
        else:
            product_url = "Not available"

        product_name_element = product.find("span", {"class": "a-size-medium"})
        if product_name_element:
            product_name = product_name_element.text
        else:
            product_name = "Not available"

        product_price_element = product.find("span", {"class": "a-price-whole"})
        if product_price_element:
            product_price = product_price_element.text
        else:
            product_price = "Not available"

        product_rating_element = product.find("span", {"class": "a-icon-alt"})
        if product_rating_element:
            product_rating = product_rating_element.text
        else:
            product_rating = "Not available"

        num_reviews_element = product.find("span", {"class": "a-size-base"})
        if num_reviews_element:
            num_reviews = num_reviews_element.text
        else:
            num_reviews = "Not available"

        product_data.append([product_url, product_name, product_price, product_rating, num_reviews])

# Save data to CSV file
csv_file = "C:\\React Projects\\amazon_products.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews"])
    writer.writerows(product_data)

print(f"Data has been saved to {csv_file}.")
