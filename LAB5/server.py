import socket
import threading
import json
from collections import defaultdict
import os
import re

from send_receive import send_data, receive_data


# Function to handle a client's messages
def handle_client(client_socket, client_address):
    """Handles the interaction between and with the clients."""

    print(f"Accepted connection from {client_address}")
    while True:
        # Get the message from the client and decode it.
        response = receive_data(client_socket)
        message = json.loads(response.decode("utf-8"))

        if message["type"] == "download":
            # Check if the file exists in the SERVER_MEDIA and then download it.
            regex_check = re.match(r'(.+\.(txt|png|jpg|jpeg))$', message['file'])
            if regex_check and os.path.exists(f"LAB5/SERVER_MEDIA/{message['file']}"):
                # Get the file from the server media folder.
                with open(f"LAB5/SERVER_MEDIA/{message['file']}", "rb") as file:
                    file_data = file.read()

                # Write the file to client's media folder.
                with open(f"LAB5/{message['room']}/{message['client']}_media/{message['file']}", "wb") as file:
                    file.write(file_data)
            else:
                # Notify the client if the file does not exist.
                notify = {
                    "type": "not existing file",
                    "message": f"File {message['file']} doesn't exist."
                }
                send_data(client_socket, json.dumps(notify).encode())
        elif message["type"] == "upload":
            # Upload the received below binary file in the SERVER_MEDIA.
            file_data = receive_data(client_socket)
            with open(f"LAB5/SERVER_MEDIA/{message['payload']['filename']}", "wb") as file:
                file.write(file_data)

            # Notify other users from the room about the upload.
            notify = {
                "type": "upload notifcation",
                "message": message["payload"]["message"]
            }
            message_string = json.dumps(notify)
            for socket in rooms[message["payload"]["room"]]:
                if socket != client_socket:
                    send_data(socket, message_string.encode('utf-8'))

        elif message["type"] == "connect":
            # Add and save the client to the right room.
            room_name = message["payload"]["room"]
            user_name = message["payload"]["name"]
            print(user_name + " is connected.")
            rooms[room_name].append(client_socket)

            # Implement the server notification of a new connection.
            notify = {
                "type": "notification",
                "payload": {
                    "message": f"{user_name} has joined the room."
                }
            }

            # Broadcast notification to the clients in the mentioned room.
            notify_json = json.dumps(notify)
            for socket in rooms[room_name]:
                if socket != client_socket:
                    send_data(socket, notify_json.encode('utf-8'))

        elif message["type"] == "message":
            # Broadcast the message to all clients.
            message_string = json.dumps(message)
            for socket in rooms[message["payload"]["room"]]:
                if socket != client_socket:
                    send_data(socket, message_string.encode())

    client_socket.close()


# Server configuration
HOST, PORT = '127.0.0.1', 12345

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the specified address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()
print(f"Server is listening on {HOST}:{PORT}")

rooms = defaultdict(list)
while True:
    client_socket, client_address = server_socket.accept()

    # Acknowledgment of successful connection sent to the new client.
    ack = {
        "type": "connect_ack",
        "payload": {
            "message": "Connected to the room."
        }
    }
    send_data(client_socket, json.dumps(ack).encode())

    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()