try:
    from Tkinter import *
    from Tkinter import messagebox
except ImportError:
    from tkinter import *
    from tkinter import messagebox
import socket
try:
    from Parser import *
except ImportError:
    from .Parser import *

class ConnectApp:
    def __init__(self, master, other_self):
        self.other_self = other_self
        self.master = master
        self.user_value = StringVar()
        self.user_label = Label(self.master, text="username :")
        self.user_entry = Entry(self.master, textvariable=self.user_value)
        self.user_label.grid(row=1, pady=1, sticky=E)
        self.user_entry.grid(row=1, column=1, pady=1)
        self.ip_value = StringVar()
        self.ip_label = Label(self.master, text="IP Address :")
        self.ip_entry = Entry(self.master, textvariable=self.ip_value)
        self.connect_button = Button(self.master, text="Add user", command=lambda: self.connect_user(self.user_entry.get(), self.ip_entry.get()))
        self.error_label = Label(self.master, text="put user info",fg='green')
        self.error_label.grid(row=0, columnspan=2)
        self.ip_label.grid(row=2, pady=1)
        self.ip_entry.grid(row=2, column=1, pady=1)
        self.connect_button.grid(row=4, columnspan=2, pady=4)

    def connect_user(self, username, address):
        global add_user
        if username == "" or address == "":
            self.error_label.config(fg="orange")
        elif address != "":
            if not is_valid_ip(address):
                self.error_label.config(text="Invalid IP", fg="red")
            else:
                self.other_self.add_user_in_list(username, address)
                print(username+address + ": From ConnectApp.connect_user.")
                self.master.destroy()

class VoiceApp:
    def __init__(self, master, other_self, user_list):
        self.other_self = other_self
        self.master = master
        self.user_list = user_list

class ServerApp:
    def __init__(self, master, other_self, username):
        self.other_self = other_self
        self.master = master
        self.username = username
        self.IP_value = StringVar()
        self.user_label = Label(master, text="Server IP :")
        self.user_entry = Entry(master, textvariable=self.IP_value)
        self.user_label.grid(row=0, pady=1, sticky=E)
        self.user_entry.grid(row=0, column=1, pady=1)
        self.PORT_value = StringVar()
        self.ip_label = Label(master, text="Server PORT :")
        self.ip_entry = Entry(master, textvariable=self.PORT_value)
        self.connect_button = Button(master, text="Join Server", command=lambda: self.join_server())
        self.connect_button.bind('<Return>')
        self.ip_label.grid(row=1, pady=1)
        self.ip_entry.grid(row=1, column=1, pady=1)
        self.connect_button.grid(row=3, columnspan=2, pady=4)
    
    def join_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.IP_value.get(), int(self.PORT_value.get())))
        sock.send(bytes("join{u:"+self.username+",}", "utf-8"))
        data = sock.recv(1024).decode('utf-8')
        print(data)
        data, headers = packet_parser(data)
        print(data)
        print(headers)
        if "error" in headers:
            messagebox.showerror("server-side-error", data['message'])
        else:
            self.other_self.reset_for_server(data, headers)
            self.master.destroy()
