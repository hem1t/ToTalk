username = ""
user_list = {}
address_list = []


def remove_user(user):
    user_list.pop(user)


def add_user(user, address):
    user_list[user] = address
    address_list.append(address)
