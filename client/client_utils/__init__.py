from mimetypes import init
from colorama import Fore, Back, Style, init
from decouple import config
import json
from os import system

HOST = config("HOST")
PORT = config("PORT", default=8000, cast=int)
URL = f"http://{HOST}:{PORT}/api/v1"


def read_json(path):
    with open(path, "r", encoding="utf-8") as file:
        jwt = json.loads(file.read())

        return jwt


init(autoreset=True)


def print_dict(dict_data):
    for k, v in dict_data.items():
        if type(v) == str:
            print(Fore.YELLOW + f"{k}:", Fore.RED + v)
        if type(v) == dict:
            print_dict(v)
