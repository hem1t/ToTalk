# This file will contain the features to work as database
from .constants.Constants import *


def groups():
    with open(channel_file, "r") as data:
        channel = data.read().slice("\n")
    return channel[:-1]


class Database:
    def __init__(self):
        self.online_user = []
        self.channels = groups()
