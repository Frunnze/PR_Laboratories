"""
Module with 2 functions for sending and receiving data.
Otherwise, I have to write both in client.py and server.py.
"""

def send_data(sock, data_in_bytes):
    data_length = len(data_in_bytes)
    data_length_bytes = data_length.to_bytes(4, byteorder='big')
    sock.send(data_length_bytes)
    sock.send(data_in_bytes)

def receive_data(sock):
    data_length_bytes = sock.recv(4)
    data_length = int.from_bytes(data_length_bytes, byteorder='big')
    received_data = sock.recv(data_length)
    return received_data