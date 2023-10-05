import socket
from bs4 import BeautifulSoup
import json

# Define the server address and port
HOST, PORT = '127.0.0.1', 8080
server_address = (HOST, PORT)


# Get the products data for finding the number of products.
with open("LAB4/products.txt", "r") as file:
    file_content = file.read()
products = json.loads(file_content)

# Get all the webserver's pages.
pages = ["/", "/about", "/contacts", "/products"]
pages.extend([f"/product/{i}" for i in range(1, len(products) + 1)])


# Go through all the pages and save the html data.
raw_pages = []
for page in pages:

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect(server_address)

    # Send the request
    request = f"GET {page} HTTP/1.1\r\nHost: {HOST}\r\n\r\n"
    client_socket.send(request.encode())

    # Receive and print the response
    response = b""
    while True:
        data = client_socket.recv(1024)
        if not data: break
        response += data

    # Format the data.
    decoded_response = response.decode()
    split_index = decoded_response.find("<")
    formatted_response = decoded_response[split_index:].strip()
    raw_pages.append(formatted_response)

# Close the socket
client_socket.close()


# Get data from pages and save it to the .txt file.
with open("LAB4/saved_data.txt", "a") as file:
    # Get the content of the simple pages and save it.
    for i in range(4):
        soup_main = BeautifulSoup(raw_pages[i], "html.parser")
        file.write("----Content of the simple page----" + "\n")
        file.write(soup_main.text.strip() + "\n"*2)
        file.write("----HTML of the simple page----" + "\n")
        file.write(str(soup_main.prettify()) + "\n"*3)

    # Get routes from the products listing page.
    file.write("----Routes from above----" + "\n")
    soup = soup_main.find_all("a")
    for a in soup: file.write(str(a.get("href") + "\n"))
    file.write("\n"*3)

    # Get data from products pages and save it.
    products = []
    for i in range(4, len(raw_pages)):
        d = {}
        soup = BeautifulSoup(raw_pages[i], "html.parser")
        d['name'] = soup.title.string
        soup = soup.find_all("p")
        d['author'] = soup[0].string
        d['price'] = float(soup[1].string[7:])
        d['description'] = soup[2].string
        products.append(d)

    file.write("----Product details----" + "\n")
    prettified_list = json.dumps(products, indent=4)
    file.write(prettified_list)