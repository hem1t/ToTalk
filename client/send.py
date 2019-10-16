import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.1.106", 5555))
sock.send(bytes("chat{t:"+sys.argv[2]+",u:"+sys.argv[1]+",};", 'utf-8'))
sock.close()
