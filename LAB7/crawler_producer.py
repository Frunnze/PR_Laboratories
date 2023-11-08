from bs4 import BeautifulSoup
import requests
import pika


def in_class(url, page=1, max_pages=1):
    """Adds each link to rabbitmq (in butches)."""

    # Gets the web page and parses it.
    response = requests.get(url)
    soup_main = BeautifulSoup(response.text, 'html.parser')

    # Takes only the products which are not boosted.
    soup = soup_main.find_all("ul", class_="ads-list-photo large-photo")
    if not soup: return

    # Filters hidden (in the middle) boosted products.
    soup = soup[0]
    lis = soup.select('li.ads-list-photo-item:not([class*=" "])')
    if not lis: return

    # Gets the links.
    url_list = []
    for li in lis:
        a = li.find("a")
        absolute_url = "https://999.md" + a.get("href")
        url_list.append(absolute_url)
    
    # Publish the list to the queue
    for link in url_list:
        channel.basic_publish(
            exchange='',
            routing_key='links_queue',
            body=link,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )

    # Goes to another page and does the same thing by recursion.
    if page == 1: url += "?page=1"
    page += 1
    if page <= max_pages:
        new_url = url[:-1] + str(page)
        in_class(new_url, page, max_pages)


if __name__ == '__main__':
    # Initialize rabbitmq
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='links_queue', durable=True)

    url = "https://999.md/ro/list/phone-and-communication/fitness-trackers"
    in_class(url=url, max_pages=5)

    connection.close()