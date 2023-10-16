import requests
from bs4 import BeautifulSoup
import csv

def get_product_details(product_url):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extracting ASIN
    try:
        asin = soup.find("th", text="ASIN").find_next("td").text.strip()
    except AttributeError:
        asin = "Not available"

    # Extracting Description
    try:
        description = soup.find("span", {"id": "productTitle"}).text.strip()
    except AttributeError:
        description = "Not available"

    # Extracting Product Description
    try:
        product_description = soup.find("div", {"id": "productDescription"}).text.strip()
    except AttributeError:
        product_description = "Not available"

    # Extracting Manufacturer
    try:
        manufacturer = soup.find("th", text="Manufacturer").find_next("td").text.strip()
    except AttributeError:
        manufacturer = "Not available"

    return [description, asin, product_description, manufacturer]

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
            additional_info = get_product_details(product_url)
            product_data.append([product_url] + additional_info)
        else:
            product_data.append(["Not available"] * 5)  # URL not found

# Save data to CSV file
csv_file = "amazon_products_details.csv"
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Product URL", "Description", "ASIN", "Product Description", "Manufacturer"])
    writer.writerows(product_data)

print(f"Data has been saved to {csv_file}.")
