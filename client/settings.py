username = "username"
server_IP = "127.0.0.1"
server_PORT = 1234

settings_text = """username    : username
server_IP   : 127.0.0.1
server_PORT : 1234
"""
try:
    with open("settings", 'r') as data:
        strings = data.read().split("\n")
    for line in strings:
        try:
            if line[:line.index(":")].strip().lower() == "username":
                username = line[line.index(":") + 1:].strip()
            elif line[:line.index(":")].strip().lower() == "server_ip":
                server_IP = line[line.index(":") + 1:].strip()
            elif line[:line.index(":")].strip().lower() == "server_port":
                server_IP = int(line[line.index(":") + 1:].strip())
        except ValueError:
            pass
except (FileExistsError, FileNotFoundError):
    with open("settings", 'w') as data:
        data.write(settings_text)

def change_default_settings(settings):
    with open("settings", 'w') as data:
        data.write(settings)