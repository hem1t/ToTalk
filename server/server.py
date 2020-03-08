#! /usr/bin/env python3

# This script will just start a port(listener) for others to connect to the server.
# Server will only have tcp communication.

# imports
from socket import socket, AF_INET, SOCK_STREAM
from multiprocessing import Process
try:
    from .request import Request
except:
    from request import Request

user_list = {}
def add_user(user, address):
    user_list[user] = address
def get_users():
    try:
        with open("users", "r") as data:
            file_data = data.read().split("\n")

        for line in file_data:
            try:
                lst = line.split(":")
                user_list[lst[0].strip()] = lst[1].strip()
            except ValueError:
                pass

    except FileNotFoundError:
        with open("users", "w") as data:
            data.write("")
    except Exception as e:
        print(e)
        exit()

    print(user_list)
get_users()

IP = "0.0.0.0"
PORT = 1234
port = (IP, PORT)

if __name__ == "__main__":
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(port)
    sock.listen(5)

    while True:
        client_socket, address = sock.accept()
        print(address)
        Request(client_socket, address, user_list, add_user)
        get_users()
