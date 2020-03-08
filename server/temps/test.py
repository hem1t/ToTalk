from socket import socket, AF_INET, SOCK_STREAM

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(("127.0.0.1", 1234))

sock.send(bytes('join{u:I_am_none,}', "utf-8"))

length = int(sock.recv(1024).decode('utf-8'))
data = sock.recv(length).decode('utf-8')

print(data)