import socket
import threading
import json
import os
from send_receive import send_data, receive_data

# Server configuration
HOST, PORT = '127.0.0.1', 12345

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")


# Add client-to-Server message structure
name = input("Enter your name: ")
room = input("Enter the room: ")
response_to_server = {
    "type": "connect",
    "payload": {
        "name": name,
        "room": room,
    }
}

# Convert the dictionary to a json string and send it to the server.
response = json.dumps(response_to_server)
send_data(client_socket, response.encode('utf-8'))


# Create the media directory for the client.
path = f"LAB5/{room}/{name}_media"
os.makedirs(path)


def receive_messages():
    """Function to receive and display messages"""

    while True:
        response = receive_data(client_socket).decode()
        message = json.loads(response)

        if message["type"] == "connect_ack":
            print(message["payload"]["message"])
        elif message["type"] == "message":
            print(message["payload"]["sender"] + ": " + message["payload"]["text"])
        elif message["type"] == "notification":
            print(message["payload"]["message"])
        elif message["type"] == "upload notifcation":
            print(message["message"])
        elif message["type"] == "not existing file":
            print(message["message"])

# Start the message reception thread
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True # Thread will exit when the main program exits
receive_thread.start()


# Executes the main part of the program.
while True:
    message_input = input()
    if message_input.lower() == 'exit': break

    # Add the options for uploading.
    if message_input.startswith("upload: "):
        # Get the path to the file.
        path = message_input[8:]

        # Get the name of the file.
        if "/" in path:
            name_of_file = path[path.rfind("/")+1:]
        else:
            name_of_file = path

        # Check if the file exists.
        if os.path.exists(path):

            # Check if the file is of a valid extension.
            if path.endswith(".txt") or path.endswith(".png") or \
                path.endswith(".jpg") or path.endswith(".jpeg"):

                # Prepare the header and send it.
                header = {
                    "type": "upload",
                    "payload": {
                        "filename": name_of_file,
                        "message": f"User {name} uploaded the {name_of_file} file.",
                        "room": room
                    }
                }
                header_data = json.dumps(header).encode("utf-8")
                send_data(client_socket, header_data)

                # Get the binary data of the file and send it.
                with open(path, 'rb') as file:
                    file_data = file.read()
                send_data(client_socket, file_data)
            else:
                print(f"File {name_of_file} doesn't exist.")
        else:
            print(f"File {name_of_file} doesn't exist.")

    elif message_input.startswith("download: "):
        # Add option for downloading files on the server, 
        # by sending the request to the server.
        
        name_of_file = message_input[10:]
        request = {
            "type": "download",
            "file": name_of_file,
            "client": name,
            "room": room
        }
        send_data(client_socket, json.dumps(request).encode("utf-8"))

    else:
        # Broadcast message to room.
        message_data = {
            "type": "message",
            "payload": {
                "sender": name,
                "room": room,
                "text": message_input
            }
        }
        send_data(client_socket, json.dumps(message_data).encode('utf-8'))

# Close the client socket
client_socket.close()