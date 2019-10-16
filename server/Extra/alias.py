import os


# Getters ##
def get_alias_details(alias):
    details = {}
    file = "./db/Extradb/aliases" + alias

    if not os.path.exists(file):
        return None
    else:
        with open(file, 'r') as data:
            file_data = data.read()

    for line in file_data.split("\n"):
        n = line.index(":")
        details[line[:n]] = line[n:]
    return details


# Setters ##
def set_alias_details(alias, **details):
    pass
