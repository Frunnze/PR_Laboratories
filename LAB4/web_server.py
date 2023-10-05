import socket
import re
import json 

# Listening.
HOST, PORT = '127.0.0.1', 8080
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

server_socket.listen(5)
print(f"Server is listening on {HOST}: {PORT}")


def handle_request(client_socket, products):
    # Receive and print the client's request data
    request_data = client_socket.recv(1024).decode('utf-8')
    print(f"Received Request:\n{request_data}")

    # Parse the request to get the HTTP method and path
    request_lines = request_data.split('\n')
    request_line = request_lines[0].strip().split()
    method = request_line[0]
    path = request_line[1]

    # Initialize the response content and status code
    response_content = ''
    status_code = 200

    # Define a simple routing mechanism
    if path == '/':
        template = """
            <!DOCTYPE html>
            <html>
                <body>
                    <h3>This is Home page.</h3>
                    <a href=/about>About</a><br>
                    <a href=/contacts>Contacts</a><br>
                    <a href=/products>Products</a><br>
                </body>
            </html>
        """
        response_content = template
    elif path == '/about':
        response_content = '<html><body><p>This is About page.</p></body></html>'
    elif path == '/contacts':
        response_content = '<html><body><p>This is Contacts page.</p></body></html>'
    elif path == '/products':
        template = """
            <!DOCTYPE html>
            <html>
                <body>
        """

        for index, product in enumerate(products):
            name = product['name']
            url = f"/product/{index+1}"
            to_add = f"<a href={url}>{name}</a><br>\n"
            template += to_add

        template += "</body></html>"
        response_content = template
    elif re.match("/product/" + r"[1-9]\d*", path):
        last_slash = path.rfind("/")
        product_id = int(path[last_slash+1:])

        if product_id <= len(products) and product_id > 0:
            product_index = product_id - 1
            name = products[product_index]['name']
            author = products[product_index]['author']
            price = products[product_index]['price']
            description = products[product_index]['description']
            template = f"""
                <!DOCTYPE html>
                <html>
                    <head>
                        <title>{name}</title>
                    </head>
                    <body>
                        <h1>{name}</h1>
                        <p>{author}</p>
                        <p>Price: {price}</p>
                        <p>{description}</p>
                    </body>
                </html>
            """
            response_content = template
        else:
            response_content = '404 Not Found'
            status_code = 404
    else:
        response_content = '404 Not Found'
        status_code = 404

    # Prepare the HTTP response
    response = f'HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_content}'
    client_socket.send(response.encode('utf-8'))

    # Close the client socket
    client_socket.close()


while True:
    # Accept incoming client connections
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
    try:
        # Get the data.
        with open("LAB4/products.txt", "r") as file:
            file_content = file.read()
        products = json.loads(file_content)

        # Handle the client's request in a separate thread
        handle_request(client_socket, products)
    except KeyboardInterrupt:
        # Handle Ctrl+C interruption here (if needed)
        pass