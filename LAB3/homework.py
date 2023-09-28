from bs4 import BeautifulSoup
import requests
import json
from unidecode import unidecode


def extract_details(url):
    """Extracts all the relevant to the product data."""

    # Defines a dictionary wich will hold the data.
    data = {}

    # Gets the web page and parses it.
    respone = requests.get(url)
    soup = BeautifulSoup(respone.text, "html.parser")

    # Gets the title of the product.
    data['Titlu'] = unidecode(soup.title.text)

    # Find the box with details.
    details = soup.find("div", class_="adPage__content__inner")
    
    # Find the properties.
    properties = details.find("div", class_="adPage__content__features")
    lis = properties.find_all("li")
    for li in lis:
        value = li.find("span", class_="adPage__content__features__value")
        if value:
            key = li.find("span", class_="adPage__content__features__key").text
            formatted_key = unidecode(key.strip())
            formatted_value = unidecode(value.text.strip())
            data[formatted_key] = formatted_value
        else:
            key = li.find("span", class_="adPage__content__features__key").text
            formatted_key = unidecode(key.strip())
            data[formatted_key] = "Prezent"

    # Gets the category.
    category = details.find("div", class_="adPage__content__features adPage__content__features__category")
    category = category.find("div").find("div")
    formatted_category = unidecode(category.text).strip()
    data['Categorie'] = formatted_category

    # Get the price.
    price = details.find("ul", class_="adPage__content__price-feature__prices")
    if price:
        price = price.find("li")
        formatted_price = unidecode(price.text).strip()
        data['Pret'] = formatted_price

    return json.dumps(data, indent=4)


url = "https://999.md/ro/84348852"
print(extract_details(url))