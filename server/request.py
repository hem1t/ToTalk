from Parser import packet_parser

class Channel:
    def __init__(self):
        channel_name = ""
        channel_description = ""
        channel_pass = ""
        channel_admin_names_and_pass = {}
        channel_user_list = {}

class Request:
    def __init__(self, sock, address, user_list, adduser):
        self.sock = sock
        self.address = address[0]
        self.user_list = user_list
        try:
            print("recieving")
            self.data, self.headers = packet_parser(sock.recv(1024).decode('utf-8'))
            print("recieved")
        except UnicodeDecodeError:
            sock.send(bytes("error{message:Packets were broken.,};", 'utf-8'))
        # call request_handler in last.
        try:
            self.request_handler(adduser)
        except Exception as e:
            print(e)
        finally:
            sock.send(bytes("error{message:Something unknown happened.,}", 'utf-8'))

    def request_handler(self, adduser):
        # if self.address is in database for being this address alive then proceed
        # else:
        #   check the packet for valid information and add it in database.
        headers = self.headers
        print(headers)
        if "chat" in headers:
            self.chat_handler()
        elif "file-transfer" in headers:
            self.file_transfer()
        elif "scan" in headers:
            self.send_details()
        elif "join" in headers:
            print("command join")
            self.send_user_list()
            self.add_user(adduser)
        else:
            sock.send(bytes("error{message:command not available.,}", 'utf-8'))
            print("command not available.")

    def chat_handler(self):
        if self.data['to'] == "some" or self.data['to'] == "except":
            lst_of_address_to_send = tuple(self.data['aliases'].split(" "))
        elif self.data['to'] == "world":
            self.send_message(EVERYONE)
        else:
            pass

    def send_message(self, *address):
        pass

    def chat_forward(self):
        pass

    def chat_update(self):
        pass

    def add_user(self):
        pass

    def file_transfer(self):
        pass

    def create_udp(self):
        pass

    def channel_creator(self):
        # A channel for any continuous communication such as video chat or voice chat or something like that.
        # or also for groups.
        # But, I was thinking for peer to peer connection between clients.
        pass

    def send_details():
        pass

    def send_user_list(self):
        # sample packet from sender
        # join{'u':hem1t,s}
        print("sending user list")
        data = "user-list{"
        for key in self.user_list.keys():
            data += key + ":" + self.user_list[key] + "," 
        self.sock.send(bytes("user-list"+data, 'utf-8'))
    
    def add_user(self, adduser):
        print("adding user in user_list")
        if self.data['u'] in self.user_list:
            pass
        else:
            adduser(self.data['u'], self.address)
            with open('users', 'a') as data:
                data.write(f"\n{self.data['u']}:{self.address}")