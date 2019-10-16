#! /usr/bin/env python3
import socket
from tkinter import *
import threading
from Parser import packet_parser
import time
# import sys

username = "hem1t"
user_list = {}


def remove_user(user):
    user_list.pop(user)


def add_user(user, address):
    user_list[user] = address


def process_request_dict(data, method):
    global c_app
    if method == "chat":
        c_app.input_chat(data['u'], data['t'])
    elif method == "remove":
        remove_user(data['u'])


def listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", 5555))
    sock.listen(20)
    while True:
        data = " "
        try:
            time.sleep(1)
            sock_client, address = sock.accept()
            while data[-1] != ";":
                data += sock_client.recv(1).decode()
            print(data)
            data_d, methods = packet_parser(data)
            add_user(data_d['u'], address[0])
            process_request_dict(data_d, methods)
        except (KeyboardInterrupt, SystemExit):
            break
        except Exception as e:
            print(e)


def get_size(wroot):
    print(wroot.winfo_width())
    print(wroot.winfo_height())


class ConnectApp:
    def __init__(self, master, other_self):
        self.other_self = other_self
        self.master = master
        self.user_value = StringVar()
        self.user_label = Label(master, text="username :")
        self.user_entry = Entry(master, textvariable=self.user_value)
        self.user_label.grid(row=0, pady=1, sticky=E)
        self.user_entry.grid(row=0, column=1, pady=1)
        self.ip_value = StringVar()
        self.ip_label = Label(master, text="IP Address :")
        self.ip_entry = Entry(master, textvariable=self.ip_value)
        self.connect_button = Button(master, text="Add user", command=lambda: self.connect_user(self.user_entry.get(), self.ip_entry.get()))
        self.ip_label.grid(row=1, pady=1)
        self.ip_entry.grid(row=1, column=1, pady=1)
        self.connect_button.grid(row=3, columnspan=2, pady=4)

    def connect_user(self, username, address):
        self.other_self.add_user_in_list(username)
        print(username+address)
        print("lsjdf")
        add_user(username, address)
        self.master.destroy()


class ClientApp:
    def __init__(self, root):
        self.master = root
        self.frame_list = Frame(root, height=20, width=15)
        self.label_list = Text(self.frame_list, bg="white", width=15)
        self.label_list.pack(side=LEFT, fill=Y)
        self.scroll_list = Scrollbar(self.frame_list)
        self.scroll_list.pack(side=RIGHT, fill=Y)
        self.scroll_list.config(command=self.label_list.yview)
        self.label_list.config(yscrollcommand=self.scroll_list.set)
        self.label_list.config(state=DISABLED)
        self.frame_list.pack(side=LEFT)
        # Frame CHAT
        self.frame_chat = Frame(root)
        self.chat_label = Text(self.frame_chat, bg="white", height=22)
        self.chat_label.pack(side=LEFT)
        self.chat_label.insert(END, "Welcome!")
        self.chat_label.config(state=DISABLED)
        self.scroll_chat = Scrollbar(self.frame_chat)
        self.scroll_chat.pack(side=RIGHT, fill=Y)
        self.scroll_chat.config(command=self.chat_label.yview)
        self.chat_label.config(yscrollcommand=self.scroll_chat.set)
        self.frame_chat.pack()
        # Frame INPUT
        self.frame_input = Frame(root)
        self.frame_input.pack(side=BOTTOM, fill=X)
        self.label = Label(self.frame_input, text="Your message:")
        self.label.pack(side=LEFT)
        self.chat_text = StringVar()
        self.chat_input = Entry(self.frame_input, textvariable=self.chat_text)
        self.chat_input.focus_set()
        self.chat_input.bind("<Return>", self.insert_chat)
        self.chat_input.pack(fill=X)
        menu = Menu()
        root.config(menu=menu)
        menu.add_command(label="connect", command=self.open_connect)
        menu.add_command(label="getsize", command=lambda: get_size(root))

    def open_connect(self):
        connect_wn = Tk()
        connect_app_wn = ConnectApp(connect_wn, self)
        connect_wn.mainloop()

    def input_chat(self, other_username, text):
        self.chat_label.config(state=NORMAL)
        self.chat_label.insert(END, "\n" + other_username + " o: " + text)
        self.chat_label.config(state=DISABLED)

    def insert_chat(self, event):
        global username
        text = self.chat_text.get()
        if text[0] == "@":
            user = text[1:text.index(" ")]
            global user_list
            address = user_list[user]
            self.send(text, address)
        else:
            self.sendall(text)
            
        self.chat_label.config(state=NORMAL)
        self.chat_label.insert(END, "\n" + username + ": " + text)
        self.chat_label.config(state=DISABLED)
        self.chat_text.set("")

    def send(self, text, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((address, 5555))
        sock.send(bytes("chat{t:" + text + ",u:" + username + ",}", 'utf-8'))
        sock.close()

    def sendall(self, text):
        global user_list
        for user in user_list.keys():
            print("sending... "+user)
            self.send(text, user_list[user])

    def add_user_in_list(self, user_name):
        self.label_list.config(state=NORMAL)
        self.label_list.insert(END, user_name+"\n")
        self.label_list.config(state=DISABLED)


if __name__ == "__main__":
    root = Tk()
    root.title("ToTalk")
    root.minsize(800, 405)
    root.maxsize(805, 437)
    c_app = ClientApp(root)
    threading.Thread(target=listener).start()
    root.mainloop()
