from Parser import packet_parser


class Request:
    def __init__(self, sock, address):
        self.sock = sock
        self.address = address
        try:
            self.data, self.headers = packet_parser(sock.recv(1024*1024).decode('utf-8'))
        except UnicodeDecodeError:
            sock.send(bytes("error{message:Packets were broken.}", 'utf-8'))
        self.request_handler()

    def request_handler(self):
        # if self.address is in database for being this address alive then proceed
        # else:
        #   check the packet for valid information and add it in database.
        headers = self.data.keys()
        if "chat" in headers:
            self.chat_handler()
        elif "file-transfer" in headers:
            self.file_transfer()

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
        # or also for groups like discord.
        # But, I was thinking for peer to peer connection between clients.
        pass
