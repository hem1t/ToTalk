#! /usr/bin/env python3
import threading
import os
from time import sleep
import socket

try:
    from cli import *
    from App import *
except ImportError:
    from .cli import *
    from .Parser import packet_parser

### User.py ###
user_list = {}
address_list = []
def remove_user(user):
    user_list.pop(user)
def add_user(user, address):
    user_list[user] = address
    address_list.append(address)
### User.py ###

### server.py ###
def joinserver(app, server_IP, server_PORT, username):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    sock.connect((server_IP, server_PORT))
    sock.send(bytes("join{u:"+username+",}", "utf-8"))
    length = int(sock.recv(1024).decode('utf-8'))
    data = sock.recv(length).decode('utf-8')
    data, headers = packet_parser(data)
    print(data)
    print(headers)
    if "error" in headers:
        messagebox.showerror("wasn't able to connect default server.", data['message'])
    else:
        app.reset_for_server(data, headers)
### server.py ###

def process_request_dict(data, method, app, sock_client, address):
    if method == "chat":
        app.input_chat(data['u'], data['t'])
    elif method == "remove":
        remove_user(data['u'])
    elif method == "file":
        app.recieveFilePermission(data['u'], data['f'], address, sock_client)
    elif method == "new-user":
        app.add_user_in_list(data['u'], data['add'])
        print("new-user")
    elif method == "voice":
        pass

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
        data = ""
        try:
            sleep(1)
            sock_client, address = sock.accept()
            print("Got connection from "+str(address))
            data = sock_client.recv(1024).decode()
            print(data)
            data_d, method = packet_parser(data)
            process_request_dict(data_d, method, c_app, sock_client, address)
        except (KeyboardInterrupt, SystemExit):
            break

# Main Client App
class ClientApp:
    def __init__(self, root):
        self.master = root
        # Frame for list of users.
        self.frame_list = Frame(root, height=20, width=15)
        # list of users
        self.label_list = Text(self.frame_list, bg="white", width=15)
        self.label_list.pack(side=LEFT, fill=Y)
        self.label_list.config(state=DISABLED)
        # scrollbar for user's list.
        self.scroll_list = Scrollbar(self.frame_list)
        self.scroll_list.pack(side=RIGHT, fill=Y)
        self.scroll_list.config(command=self.label_list.yview)
        self.label_list.config(yscrollcommand=self.scroll_list.set)
        self.frame_list.pack(side=LEFT)
        ### Frame for CHAT box.
        self.frame_chat = Frame(root)
        # chat box where chat will be displayed.
        self.chat_label = Text(self.frame_chat, bg="white", height=22)
        self.chat_label.pack(side=LEFT)
        self.chat_label.insert(END, f"Welcome!, {username} type /help for more info.")
        self.chat_label.config(state=DISABLED)
        self.scroll_chat = Scrollbar(self.frame_chat)
        self.chat_label.config(yscrollcommand=self.scroll_chat.set)
        self.scroll_chat.pack(side=RIGHT, fill=Y)
        self.scroll_chat.config(command=self.chat_label.yview)
        self.frame_chat.pack()
        #### Frame for INPUT field of sending message.
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
        menu.add_command(label="Peer-to-Peer", command=self.open_connect)
        menu.add_command(label="Server", command=self.join_server)
        menu.add_command(label="Voice Call", command=self.open_voice_call)

    def join_server(self):
        # join server window
        server_wn = Toplevel(self.master)
        server_wn.bind("<Destroy>", lambda a:self.master.deiconify())
        self.master.withdraw()
        server_app_wn = ServerApp(server_wn, self, username)
        server_wn.mainloop()
    
    def open_voice_call(self):
        # voice call window
        voice_wn = Toplevel(self.master)
        voice_wn.bind("<Destroy>", lambda a:self.master.deiconify())
        self.master.withdraw()
        voice_app_wn = VoiceApp(voice_wn, self)
        voice_wn.mainloop()

    def open_connect(self):
        connect_wn = Toplevel(self.master)
        connect_wn.bind("<Destroy>", lambda a:self.master.deiconify())
        self.master.withdraw()
        connect_app_wn = ConnectApp(connect_wn, self)
        connect_wn.mainloop()

    def input_chat(self, other_username, text):
        self.chat_label.config(state=NORMAL)
        self.chat_label.insert(END, "\n" + other_username + text)
        self.chat_label.config(state=DISABLED)

    def insert_chat(self, event):
        global username, user_list
        text = self.chat_text.get()
        self.chat_label.config(state=NORMAL)
        try:
            print("try in ToTalk.py at 135")
            if text[0] == "/":
                result_value = self.command(text)
                self.chat_label.insert(END, "\n" + result_value)
            elif text[0] == "@":
                temp_text = text[1:].split(" ")
                user = temp_text[0]
                if user == "":
                    self.chat_label.insert(END, "\nuser name cannot be empty")
                    assert 1==0
                try:
                    print("try in ToTalk.py at 149")
                    text = temp_text[1]
                except IndexError:
                    text = ""
                try:
                    print("try in ToTalk.py at 154")
                    address = user_list[user]
                    threading.Thread(target=self.send_one, args=(text, address)).start()
                    self.chat_label.insert(END, "\n"+username+" -> "+user+":"+text)
                except KeyError:
                    self.chat_label.insert(END, "\n"+user+": Not Found")
            else:
                threading.Thread(target=self.sendall, args=(text,)).start()
                self.chat_label.insert(END, "\n" + username + ":" + text)
        except ValueError:
            pass
        except IndexError:
            pass
        except Exception as e:
            print(e)
        finally:
            self.chat_label.config(state=DISABLED)
            self.chat_text.set("")
            self.chat_label.see("end")

    def send_one(self, text, address):
        global username
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((address, 5555))
        message="chat{t:"+text.strip()+",u:"+username.strip()+",};"
        print("msg: "+message+": from ClientApp.send_one.")
        sock.send(bytes(message, 'utf-8'))
        print("Sended to: "+ address)
        del sock

    def sendall(self, text):
        global user_list
        for user in user_list.keys():
            print("sending... "+user)
            self.send_one(text, user_list[user])

    def add_user_in_list(self, user_name, address):
        global username
        print('adding user')
        if user_name in user_list.keys():
            messagebox.showinfo("", f"{user_name} is already in list.")
        elif user_name == username:
            pass
        else:
            add_user(user_name, address)
            print(user_list)
            self.label_list.config(state=NORMAL)
            self.label_list.insert(END, user_name+"\n")
            self.label_list.config(state=DISABLED)
    
    def command(self, text):
        print("passing to cli")
        return cli_run(text, self, user_list)
    
    def recieveFilePermission(self, user, file_info, address):
        answer = messagebox.askyesno("File Transfer", f"{user}, wants to send you {file_info}")
        if answer:
            sock_client.send("")
    
    def reset_for_server(self, data, headers):
        # After joining any other server App would need to reset whole user list according to server.
        print(str(data) + "reset_for_server")
        global user_list
        user_list = {}
        self.delete_label_list()
        for user in data.keys():
            self.add_user_in_list(user, data[user])
    
    def delete_label_list(self):
        self.label_list.config(state=NORMAL)
        self.label_list.delete('1.0', END)
        self.label_list.config(state=DISABLED)

if __name__ == "__main__":
    root = Tk()
    root.title("ToTalk")
    root.minsize(804, 436)
    root.maxsize(805, 437)
    c_app = ClientApp(root)
    # Settings up default server.
    if is_valid_ip(server_IP) and server_PORT > 0:
        try:
            joinserver(c_app, server_IP, server_PORT, username)
        except Exception as e:
            messagebox.showerror("Error while connecting to default server", e)
    # thread for listener.
    thread = threading.Thread(target=listener)
    thread.start()
    root.mainloop()
    # Thread doesn't closes by itself, so program needs this line, to kill itself.
    os.kill(os.getpid(), 1)
