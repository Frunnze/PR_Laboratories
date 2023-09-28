from bs4 import BeautifulSoup
import requests


def in_class(url, page=1, url_list=[], max_pages=1):
    """Finds all the product links and returns a list with them."""

    # Gets the web page and parses it.
    response = requests.get(url)
    soup_main = BeautifulSoup(response.text, 'html.parser')

    # Takes only the products which are not boosted.
    soup = soup_main.find_all("ul", class_="ads-list-photo large-photo")

    # Returns the list of links if it got to the limit of pages.
    if not soup: return url_list

    # Filters hidden (in the middle) boosted products.
    soup = soup[0]
    lis = soup.select('li.ads-list-photo-item:not([class*=" "])')

    # Gets the links.
    for li in lis:
        a = li.find("a")
        absolute_url = "https://999.md" + a.get("href")
        url_list.append(absolute_url)

    # Goes to another page and does the same thing by recursion.
    if page == 1: url += "?page=1"
    page += 1
    if page <= max_pages:
        new_url = url[:-1] + str(page)
        return in_class(new_url, page, url_list, max_pages)
    
    return url_list


url = "https://999.md/ro/list/phone-and-communication/fitness-trackers"
urls = in_class(url)
print(urls)
print(len(urls))