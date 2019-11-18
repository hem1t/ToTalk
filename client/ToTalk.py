#! /usr/bin/env python3
import threading
try:
    from App import *
except ImportError:
    from .App import *
import os


def get_size(wroot):
    print(wroot.winfo_width())
    print(wroot.winfo_height())


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
        self.chat_label.insert(END, "\n" + other_username + text)
        self.chat_label.config(state=DISABLED)

    def insert_chat(self, event):
        global username, user_list
        try:
            text = self.chat_text.get()
            self.chat_label.config(state=NORMAL)
            if text[0] == "@":
                user = text[1:text.index(" ")]
                text = text[text.index(" "):]
                address = user_list[user]
                threading.Thread(target=self.send_one, args=(text, address)).start()
                self.chat_label.insert(END, "\n"+username+" -> "+user+":"+text)
            else:
                threading.Thread(target=self.sendall, args=(text,)).start()
                self.chat_label.insert(END, "\n" + username + ":" + text)
        except ValueError:
            pass
        except Exception as e:
            print(e)
        finally:
            self.chat_label.config(state=DISABLED)
            self.chat_text.set("")

    def send_one(self, text, address):
        global username
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((address, 5555))
        message="chat{t:"+text.strip()+",u:"+username.strip()+",};"
        print("msg: "+message)
        sock.send(bytes(message, 'utf-8'))
        print("Sended to: "+ address)
        del sock

    def sendall(self, text):
        global user_list
        for user in user_list.keys():
            print("sending... "+user)
            self.send_one(text, user_list[user])

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
    thread = threading.Thread(target=listener)
    thread.start()
    root.mainloop()
    # Thread doesn't closes by itself, so program needs this line, to kill itself.
    os.kill(os.getpid(), 1)
