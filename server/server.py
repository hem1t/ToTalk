#! /usr/bin/env python3

# This script will just start a port(listener) for others to connect to the server.
# Server will only have tcp communication.

# imports
from socket import socket, AF_INET, SOCK_STREAM
from multiprocessing import Process
from .request import Request

IP = "0.0.0.0"
PORT = 1234
port = (IP, PORT)

if __name__ == "__main__":
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(port)
    sock.listen(5)

    while True:
        client_socket, address = sock.accept()
        Process(target=Request, args=(client_socket, address)).start()
