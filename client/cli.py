try:
    from Parser import *
    from settings import *
except ImportError:
    from .settings import *
import socket

username = username
settings_text = settings_text
server_IP = server_IP
server_PORT = server_PORT

help_text = """Welcome! to chat, you can try:
    /joinserver [server_IP] [server_PORT]
        --> userlist and everything will updated as per server

    /sendfile [PATH]/[FILE]
        --> Will try to send the file to mentioned user(if available).
            But, can only send small file.
    
    /set 
        --> Alter settings.
            Note:- To activate any settings you have restart the application.
            Available settings:
                username
                default_server_IP
                default_server_PORT
    
    /show
        --> By default shows all settings.
"""

def cli_run(stream, app, user_list):
    global username, server_PORT, server_IP, settings_text
    stream = stream.split(" ")
    command = stream[0]
    print("command "+command)
    if len(stream) > 1:
        options = stream[1:]
    else:
        options = [""]
    print("options" +str(options))
    if "/set" in command:
        return setting(options)
    elif "/show" in command:
        return show(options[0])
    elif "/help" in command:
        return help_text
    elif "/sendfile" in command:
        return sendfile(user_list[options[0]], options[1], app)
    elif "/joinserver" in command:
        if is_valid_ip(options[0]) and int(options[1]) > 0:
            return joinserver(app, options[0], int(options[1]), username)
        else:
            return "wrong info given."
    else:
        return f"{command} not found."

def sendfile(address, path, app):
    return "Feature Not available, right now, wait for the update."

def joinserver(app, server_IP, server_PORT, username):
    try:
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
            return "wasn't able to connect server." +"\n\t"+data['message']
        else:
            app.reset_for_server(data, headers)
    except Exception as e:
        return str(e)

def setting(params):
    global username, server_PORT, server_IP, settings_text
    if params[0].lower() == "username":
        previous = username
        username = params[1]
    elif params[0].lower() == "server_ip":
        previous = server_IP
        server_IP = params[1]
    elif params[0].lower() == "server_port":
        previous = server_PORT
        server_PORT = params[1]
    else:
        return f"{params[0]}: unknown settings."
    
    settings_text = f"username       :   {username}\nserver_IP      :   {server_IP}\nserver_PORT    :   {server_PORT}"
    print(settings_text)
    change_default_settings(settings_text)
    return f"{params[0]} changed to {params[1]} from {previous} \nNote: NEEDS RESTART!!!"

def show(params):
    if params == "":
        return settings_text
    elif params.lower().strip() == "username":
        return f"username: {username}"
    elif params.lower().strip() == "server_ip":
        return f"server_IP: {server_IP}"
    elif params.lower().strip() == "server_port":
        return f"server_PORT: {server_PORT}"
    else:
        print(params)
        return f"{params}: unknown settings."
        
