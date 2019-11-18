try:
    from Tkinter import *
except ImportError:
    from tkinter import *
try:
    from Listener import *
except ImportError:
    from .Listener import *


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
        self.connect_button.bind('<Return>', lambda: self.connect_user(self.user_entry.get(), self.ip_entry.get()))
        self.ip_label.grid(row=1, pady=1)
        self.ip_entry.grid(row=1, column=1, pady=1)
        self.connect_button.grid(row=3, columnspan=2, pady=4)

    def connect_user(self, username, address):
        self.other_self.add_user_in_list(username)
        print(username+address)
        print("lsjdf")
        add_user(username, address)
        self.master.destroy()
