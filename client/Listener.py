import socket
import time
try:
    from Parser import packet_parser
    from User import *
except ImportError:
    from .User import *
    from .Parser import packet_parser


def process_request_dict(data, method, app):
    if method == "chat":
        app.input_chat(data['u'], data['t'])
    elif method == "remove":
        remove_user(data['u'])


def listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    while True:
        try:
            sock.bind(("0.0.0.0", 5555))
            break
        except Exception as e:
            print(e)
            quit()
    sock.listen(20)
    while True:
        data = " "
        try:
            time.sleep(1)
            sock_client, address = sock.accept()
            print("Got connection from "+str(address))
            while data[-1] != ";":
                data += sock_client.recv(1).decode()
            print(data)
            data_d, methods = packet_parser(data)
            if address[0] in address_list:
                pass
            else:
                print("Adding to user_list. "+data_d['u'])
                add_user(data_d['u'], address[0])
                c_app.add_user_in_list(data_d['u'])
            process_request_dict(data_d, methods, app)
        except (KeyboardInterrupt, SystemExit):
            break
