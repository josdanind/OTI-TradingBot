import json, requests
from random import choices
from client_utils import URL, read_json, print_dict

is_trader = bool(input("You are a trader?:"))

users = read_json("./users.json")
role = "trader" if is_trader else "user"
user = choices(list(users[role]))[0]

is_trader = True if role == "trader" else False
url = URL + f"/users/login?is_trader={is_trader}"

password = users[role][user]["password"]
login = {"username": user, "password": password}

session = requests.Session()
response = session.post(url, login)
content = json.loads(response.content.decode("utf-8"))

content["role"] = "Trader" if is_trader else "User"

if response.status_code == 200:
    print_dict(content)
    with open("./token.json", "w", encoding="utf-8") as file:

        file.write(json.dumps(content))
else:
    print(response.content)
